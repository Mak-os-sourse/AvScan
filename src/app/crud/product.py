from src.app.crud.factory import BaseCrud
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.product import Products

class ProductCRUD(BaseCrud):
    def __init__(self):
        super().__init__(Products)
        
    async def create(self,
        session: AsyncSession, url: str,
        id_product: int, name: str,
        description: str, price: str | int,
        url_photo: str, user_id: int,
        task_id: int
        ) -> Products:
        return await super().insert(
            session, url=url,
            id_product=id_product,
            name=name, price=str(price),
            description=description,
            url_photo=url_photo,
            user_id=user_id,
            task_id=task_id
        )
    
    async def get(self, session: AsyncSession, **kargs) -> Products | None:
        where = super().get_where(**kargs)
        result = await super().select(session, where=where)
        return result[0] if result else None
    
    async def get_all(self, session: AsyncSession, **kargs) -> list[Products]:
        where = super().get_where(**kargs)
        return await super().select(session, where=where)
    
    async def update(self, session: AsyncSession, id: int, **values):
        return await super().update(session, where=[Products.id == id], **values)
    
    async def delete(self, session: AsyncSession, id: int, **kargs):
        where = super().get_where(**kargs, id=id)
        return await super().delete(session, where=where)
    
product_crud = ProductCRUD()