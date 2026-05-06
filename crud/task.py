from typing import Literal
from crud.factory import BaseCrud
from sqlalchemy.ext.asyncio import AsyncSession

from models.task import Tasks

class TaskCRUD(BaseCrud):
    def __init__(self):
        super().__init__(Tasks)
        
    async def create(self,
        session: AsyncSession, url: str,
        mode: Literal["Interval", "Every"],
        scheduled_at: int, user_id: int,
        interval: int | None = None, last_views: int = 0,
        launches: int = 0
        ) -> Tasks:
        return await super().insert(
            session, url=url, mode=mode,
            scheduled_at=scheduled_at,
            user_id=user_id, interval=interval,
            last_views=last_views, launches=launches,
        )
    
    async def get(self, session: AsyncSession, **kargs) -> Tasks | None:
        where = super().get_where(**kargs)
        result = await super().select(session, where=where)
        return result[0] if result else None
    
    async def get_all(self, session: AsyncSession, **kargs) -> list[Tasks]:
        where = super().get_where(**kargs)
        return await super().select(session, where=where)
    
    async def update(self, session: AsyncSession, id: int, **values):
        return await super().update(session, where=[Tasks.id == id], **values)
    
    async def delete(self, session: AsyncSession, id: int, **kargs):
        where = super().get_where(**kargs, id=id)
        return await super().delete(session, where=where)
    
task_crud = TaskCRUD()