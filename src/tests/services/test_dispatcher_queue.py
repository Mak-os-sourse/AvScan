from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.fake import fake
from src.app.models.task import Tasks
from src.app.services.queue import queue
from src.tests.factories.task import task_factory
from src.tests.factories.user import user_factory
from src.app.services.dispatcher_queue import dispatcher_queue

async def test_sync_queue(session: AsyncSession, cache: Redis):
    user = await user_factory.add(session)
    await task_factory.add(session, user_id=user.id)
    
    await dispatcher_queue.sync_queue(redis=cache, session=session)
    
    assert await cache.zpopmax(queue.name_queue)
    assert dispatcher_queue.tasks

async def test_sync_queue_delete_task(session: AsyncSession, cache: Redis):
    user = await user_factory.add(session)
    task = Tasks(
        id=1,
        user_id=user.id,
        url=fake.url(),
        interval=1,
        scheduled_at=1,
        launches=0,
    )
    
    dispatcher_queue.tasks[task.id] = task
    await dispatcher_queue.sync_queue(redis=cache, session=session)
    
    assert not await cache.zpopmax(queue.name_queue)
    assert not dispatcher_queue.tasks