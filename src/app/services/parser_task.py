from taskiq import TaskiqState
from sqlalchemy import select, or_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.cache import redis
from src.app.models.task import Tasks
from src.app.crud.task import task_crud
from src.app.services.queue import queue
from src.app.models.product import Products
from src.app.types.queue import TaskQueue, ModeTask
from src.app.services.parser.scraper import scraper
from src.app.exceptions.parser import ListProductError
from src.app.types.parser import Product

class ParserTask:
    async def parse(self, session: AsyncSession, task: TaskQueue) -> dict[int, Product]:
        try:
            products = await scraper.scrape(task.url)
            await self._add_products(session, products, task=task)
            await redis.zpopmax(queue.name_queue)
            return products
        except ListProductError:
            if task.mode == ModeTask.INTERVAL:
                await task_crud.delete(session, id=task.id)
            await redis.zpopmax(queue.name_queue)
    
    async def update_task(self, session: AsyncSession, id: int, state: TaskiqState):
        task = state.tasks.get(id)
        if task is None:
            task = await task_crud.get(session, id=id)
        scheduled_at = task.scheduled_at + task.interval
        launches = task.launches + 1
        await task_crud.update(session, id=id, scheduled_at=scheduled_at, launches=launches)
    
    async def sync_queue(self, session: AsyncSession, state: TaskiqState):
        stmt = select(Tasks).where(or_(Tasks.id.not_in(state.tasks.keys()), Tasks.last_update > state.last_views))
        data = (await session.scalars(stmt)).all()
        for item in data:
            state.tasks[item.id] = item
        session.expunge_all()
        await queue.update_queue(state.tasks.values())
        
    async def _add_products(self, session: AsyncSession, products: dict[int, Product], task: TaskQueue):
        for item in products.values():
            task_id = task.id if task.mode == ModeTask.INTERVAL else None
            data = {
                "name": item.name,
                "price": item.price,
                "url": item.url,
                "id_product": item.id,
                "description": item.description,
                "url_photo": item.image,
                "user_id": task.user_id,
                "task_id": task_id,
            }
            stmt = insert(Products) \
                .values(data) \
                .on_conflict_do_update(index_elements=[Products.id_product], set_=data)
            await session.execute(stmt)
        await session.commit()
    
parser_task = ParserTask()