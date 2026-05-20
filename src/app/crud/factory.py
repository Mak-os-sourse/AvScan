from sqlalchemy import select, delete, update, insert, BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.base import TModel

class BaseCrud:
    def __init__(self, model: TModel):
        self.model = model
    
    async def insert(self, session: AsyncSession, **values) -> TModel | None:
        stmt = insert(self.model).values(**values).returning(self.model)
        result = await session.scalars(stmt)
        return result.one_or_none()
    
    async def select(self, session: AsyncSession, where: list[BinaryExpression]) -> list[TModel]:
        stmt = select(self.model).where(*where)
        result = await session.scalars(stmt)
        return result.all()
    
    async def update(self, session: AsyncSession, where: list[BinaryExpression], **values) -> TModel | None:
        stmt = update(self.model).values(**values).where(*where).returning(self.model)
        result = await session.scalars(stmt)
        return result.one_or_none()
        
    async def delete(self, session: AsyncSession, where: list[BinaryExpression]) -> None:
        stmt = delete(self.model).where(*where)
        await session.execute(stmt)
    
    def get_where(self, **kargs) -> list[BinaryExpression]:
        where = []
        for key, value in kargs.items():
            where.append(getattr(self.model, key) == value)
        return where