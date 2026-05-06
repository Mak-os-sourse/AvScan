from sqlalchemy import select, insert, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from core.base import TModel

class Factory:
    def __init__(self, model: TModel):
        self.model = model
    
    async def get(self, session: AsyncSession, **kargs) -> TModel | None:
        return (await self._get_data(session, **kargs)).one_or_none()

    async def get_all(self, session: AsyncSession, **kargs) -> list[TModel]:
        return (await self._get_data(session, **kargs)).all()

    async def add(self, session: AsyncSession, **kargs) -> TModel:
        return (await self._add_data(session, **kargs)).one()
    
    async def _get_data(self, session: AsyncSession, **kargs) -> ScalarResult:
        where = []
        for key, value in kargs.items():
            where.append(getattr(self.model, key) == value)
        stmt = select(self.model).where(*where)
        return await session.scalars(stmt)
        
    async def _add_data(self, session: AsyncSession, **kargs) -> ScalarResult:
        stmt = insert(self.model).values(**kargs).returning(self.model)
        result = await session.scalars(stmt)
        await session.flush()
        return result