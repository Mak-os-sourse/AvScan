import asyncio, time
from aiogram.types import BufferedInputFile
from taskiq import TaskiqDepends, TaskiqState, TaskiqEvents
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq_redis import RedisStreamBroker

from src.app.core.db import db
from src.app.core.bot import bot
from src.app.core.text import text
from src.app.types.parser import Product
from src.app.types.queue import ModeTask
from src.app.services.queue import queue
from src.app.core.settings import settings
from src.app.services.parser_task import parser_task
from src.app.services.document import create_product_document

broker = RedisStreamBroker(settings.BROKER_URL)

@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def setup(state: TaskiqState):
    state.last_views = 0
    state.tasks = {}

@broker.task
async def send_document(products: list[Product], user_id: int, wait: int = 0):
    await asyncio.sleep(wait)
    document = create_product_document(products)
    file = BufferedInputFile(document, filename="document.xlsx")
    await bot.send_document(user_id, document=file, caption=text.get_document)

@broker.task
async def start_parsing(session: AsyncSession = TaskiqDepends(db.get_session), state: TaskiqState = TaskiqDepends()):
    task_queue = await queue.get_task()
    if task_queue is None:
        await asyncio.sleep(5)
        await start_parsing.kiq()
        return
    
    products = await parser_task.parse(session, task_queue)
    if products is None:
        await asyncio.sleep(5)
        await start_parsing.kiq()
        return
    
    products = list(products.values())
    
    await parser_task.sync_queue(session, state)
    
    if task_queue.mode == ModeTask.INTERVAL:
        task = state.tasks.get(task_queue.id)
        if task is None:
            await start_parsing.kiq()
            return
        wait = max(0, task.scheduled_at - int(time.time()))
        await parser_task.update_task(session, id=task.id, state=state)
        await send_document.kiq(products=products, user_id=task.user_id, wait=wait)
    else:
        await send_document.kiq(products=products, user_id=task_queue.user_id)
    
    await start_parsing.kiq()
