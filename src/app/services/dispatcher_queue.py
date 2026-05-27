import time
from redis.asyncio import Redis
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.task import Tasks
from src.app.services.queue import queue

class DispatcherQueue:
    def __init__(self):
        self.tasks: dict[int, Tasks] = {}
        self.last_views = 0
    
    async def sync_queue(self, session: AsyncSession, redis: Redis) -> None:
        await self._add_update_tasks(session)
        await self._pop_deleted_tasks(session)
        await queue.update_queue(redis, self.tasks.values())
        self.last_views = int(time.time())
        
    async def _add_update_tasks(self, session: AsyncSession) -> None:
        stmt = select(Tasks).where(or_(Tasks.id.not_in(self.tasks.keys()), Tasks.last_update >= self.last_views))
        data = (await session.scalars(stmt)).all()
        for item in data:
            self.tasks[item.id] = item
        session.expunge_all()
            
    async def _pop_deleted_tasks(self, session: AsyncSession) -> None:
        stmt = select(Tasks.id).where(Tasks.id.in_(self.tasks.keys()))
        data = (await session.execute(stmt)).all()
        keys = list(self.tasks.keys())
        ids = [item[0] for item in data]
        for item in keys:
            if item not in ids:
                self.tasks.pop(item)

dispatcher_queue = DispatcherQueue()
            