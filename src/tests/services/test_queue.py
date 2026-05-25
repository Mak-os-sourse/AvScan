import json
from numpy import random
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.types.queue import TaskQueue, ModeTask
from src.tests.factories.task import task_factory
from src.tests.factories.user import user_factory
from src.app.services.queue import queue
from src.tests.fake import fake

async def test_get_task(cache: Redis):
    task_id = random.randint(0, 1000)
    key = TaskQueue(id=task_id, url=fake.url(), user_id=1, mode=ModeTask.INTERVAL)
    await cache.zadd(queue.name_queue, {key.to_json(): 0.7})
    
    task = (await queue.get_task(cache)).to_dict()
    assert task["id"] == task_id

async def test_add_fast_task(cache: Redis):
    uuid = await queue.add_fast_task(cache, fake.url(), 1)
    pop = await cache.zpopmax(queue.name_queue)
    assert pop[0][1] == 0.7
    assert isinstance(uuid, int)
    
async def test_add_task(cache: Redis, session: AsyncSession):
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id)
    
    await queue.add_task(cache, task)
    
    pop = await cache.zpopmax(queue.name_queue)
    coefficient = pop[0][1]
    assert coefficient == 1
    
async def test_update_queue(cache: Redis, session: AsyncSession):
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id)
    key = json.dumps({"id": task.id, "url": task.url})
    
    await cache.zadd(queue.name_queue, {key: 0.8})
    
    await queue.update_queue(cache, [task])
    
    pop = await cache.zpopmax(queue.name_queue)
    coefficient = pop[0][1]
    assert coefficient == 1