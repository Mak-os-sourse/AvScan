from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.fake import fake
from src.app.models.task import Tasks
from src.tests.factories.factory import Factory

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
    ) -> Tasks:
        return await super().add(
            session,
            url=url,
            user_id=user_id,
            interval=interval,
            last_views=last_views,
            scheduled_at=scheduled_at,
            launches=launches,
        )
        
task_factory = TaskFactory()