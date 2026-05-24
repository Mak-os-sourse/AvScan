from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.task import task_crud
from src.app.models.product import Products
from src.app.services.parser.scraper import scraper
from src.app.types.queue import TaskQueue, ModeTask
from src.app.exceptions.parser import ListProductError
from src.app.types.parser import Product

class ParserService:
    async def parse(self, session: AsyncSession, task: TaskQueue) -> dict[int, Product]:
        try:
            products = await scraper.scrape(task.url)
            await self._add_products(session, products, task=task)
            return products
        except ListProductError:
            if task.mode == ModeTask.INTERVAL:
                await task_crud.delete(session, id=task.id)
        
    async def _add_products(self, session: AsyncSession, products: dict[int, Product], task: TaskQueue):
        for item in products.values():
            task_id = task.id if task.mode == ModeTask.INTERVAL else None
            data = {
                "name": item.name,
                "price": str(item.price),
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
    
parser_service = ParserService()