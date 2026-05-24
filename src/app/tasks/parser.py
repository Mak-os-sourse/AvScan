import asyncio, time
from taskiq import TaskiqDepends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db import db
from src.app.crud.task import task_crud
from src.app.services.queue import queue
from src.app.types.parser import Product
from src.app.tasks.bot import send_document
from src.app.core.broker_task import broker
from src.app.types.queue import ModeTask, TaskQueue
from src.app.services.parser_service import parser_service
from src.app.services.dispatcher_queue import dispatcher_queue

class ParserTask:
    @staticmethod
    @broker.task()
    async def start_polling(session: AsyncSession = TaskiqDepends(db.get_session)):
        task_queue = await ParserTask._get_task_queue(session)
        if task_queue is None:
            return
        
        products = await ParserTask._get_product(session, task_queue)
        if products is None:
            return
        
        products = list(products.values())
        
        await dispatcher_queue.sync_queue(session)
        
        await ParserTask._send_message(session, task_queue=task_queue, products=products)  
        
        await ParserTask.start_polling.kiq()
    
    @staticmethod
    async def _pass_parser(session):
        await asyncio.sleep(5)
        await ParserTask.start_polling.kiq()
        await dispatcher_queue.sync_queue(session)
    
    @staticmethod
    async def _get_task_queue(session: AsyncSession) -> TaskQueue | None:
        task_queue = await queue.get_task()
        if task_queue is None:
            await ParserTask._pass_parser(session)
            return
        if task_queue.completed == True:
            await ParserTask._pass_parser(session)
            return
        return task_queue
    
    @staticmethod
    async def _get_product(session: AsyncSession, task_queue: TaskQueue) -> list[Product] | None:
        products = await parser_service.parse(session, task_queue)
        if products is None:
            await ParserTask._pass_parser(session)
        return products
    
    @staticmethod
    async def _send_message(session: AsyncSession, task_queue: TaskQueue, products: list[Product]):
        if task_queue.mode == ModeTask.INTERVAL:
            task = dispatcher_queue.tasks.get(task_queue.id)
            if task is None:
                await ParserTask._pass_parser(session)
                return
            wait = max(0, task.scheduled_at - int(time.time()))
            scheduled_at = task.scheduled_at + task.interval
            await task_crud.update(
                session, id=task.id,
                scheduled_at=scheduled_at,
                launches=task.launches + 1,
                completed=True
            )
            await send_document.kiq(products=products, user_id=task.user_id, wait=wait)
            await update_task.kiq(task_id=task.id, wait=wait)
        else:
            await send_document.kiq(products=products, user_id=task_queue.user_id)

@broker.task
async def update_task(task_id: int, wait: int, session: AsyncSession = TaskiqDepends(db.get_session)):
    await asyncio.sleep(wait)
    await task_crud(session, id=task_id, completed=False)
