import json
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories.task import task_factory
from tests.factories.user import user_factory
from services.queue import queue
from tests.fake import fake

async def test_add_fast_task(cache: Redis):
    uuid = await queue.add_fast_task(fake.url())
    pop = await cache.zpopmax("queue:parser")
    assert pop[0][1] == 0.7
    assert isinstance(uuid, str)
    
async def test_add_task(cache: Redis, session: AsyncSession):
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id)
    
    await queue.add_task(task)
    pop = await cache.zpopmax("queue:parser")
    coefficient = pop[0][1]
    assert coefficient == 1
    
async def test_update_queue(cache: Redis, session: AsyncSession):
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id)
    key = json.dumps({"id": task.id, "url": task.url})
    
    await cache.zadd("queue:parser", {key: 0.8})
    await queue.update_queue([task])
    pop = await cache.zpopmax("queue:parser")
    coefficient = pop[0][1]
    assert coefficient == 1