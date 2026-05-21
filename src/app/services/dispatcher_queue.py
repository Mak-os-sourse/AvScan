from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.task import Tasks
from src.app.crud.task import task_crud
from src.app.services.queue import queue

class DispatcherQueue:
    def __init__(self):
        self.tasks = {}
        self.last_views = 0
    
    async def update_task(self, session: AsyncSession, id: int):
        task = self.tasks.get(id)
        if task is None:
            task = await task_crud.get(session, id=id)
        scheduled_at = task.scheduled_at + task.interval
        launches = task.launches + 1
        await task_crud.update(session, id=id, scheduled_at=scheduled_at, launches=launches)
    
    async def sync_queue(self, session: AsyncSession):
        stmt = select(Tasks).where(or_(Tasks.id.not_in(self.tasks.keys()), Tasks.last_update > self.last_views))
        data = (await session.scalars(stmt)).all()
        for item in data:
            self.tasks[item.id] = item
        session.expunge_all()
        await queue.update_queue(self.tasks.values())
        
    async def get_all_id(self, session: AsyncSession):
        stmt = select(Tasks.id).where(Tasks.id.in_(self.tasks.keys()))
        data = (await session.execute(stmt)).all()