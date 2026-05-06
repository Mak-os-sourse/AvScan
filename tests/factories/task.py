from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from tests.fake import fake
from models.task import Tasks
from tests.factories.factory import Factory

class TaskFactory(Factory):
    def __init__(self):
        super().__init__(Tasks)
        
    async def add(
        self,
        session: AsyncSession,
        user_id: int,
        url: str = fake.url(),
        interval: int = 0,
        last_views: int = 0,
        scheduled_at: int = 0,
        launches: int = 0,
        mode: Literal["Interval", "Every"] = "Every",
    ) -> Tasks:
        return await super().add(
            session,
            url=url,
            user_id=user_id,
            interval=interval,
            last_views=last_views,
            scheduled_at=scheduled_at,
            launches=launches,
            mode=mode,
        )
        
task_factory = TaskFactory()