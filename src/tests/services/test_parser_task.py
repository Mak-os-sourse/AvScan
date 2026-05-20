from redis.asyncio import Redis
from unittest.mock import patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.fake import fake
from src.app.services.queue import queue
from src.app.types.parser import Product
from src.tests.factories.task import task_factory
from src.tests.factories.user import user_factory
from src.app.types.queue import TaskQueue, ModeTask
from src.tests.factories.product import product_factory
from src.app.services.parser_task import parser_task
from src.app.exceptions.parser import ListProductError

class State:
    last_views = 0
    tasks = {}

@patch("src.app.services.parser.scraper.scraper.scrape", new_callable=AsyncMock)
async def test_start(mock: AsyncMock, session: AsyncSession, cache: Redis):
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id, interval=10)
    
    task_queue = TaskQueue(id=task.id, url=fake.url(), user_id=1, mode=ModeTask.INTERVAL)
    await cache.zadd(queue.name_queue, {task_queue.to_json(): 0.8})
    mock.return_value = []
    
    await parser_task.parse(session=session, task=task_queue)
    
    assert await cache.zrevrange(queue.name_queue, 1, 0) == []
    
@patch("src.app.services.parser.scraper.scraper.scrape", new_callable=AsyncMock)
async def test_start_add_product(mock: AsyncMock, session: AsyncSession, cache: Redis):
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id, interval=10)
    url = task.url
    
    task_queue = TaskQueue(id=task.id, url=url, user_id=user.id, mode=ModeTask.INTERVAL)
    await cache.zadd(queue.name_queue, {task_queue.to_json(): 0.8})
    mock.return_value = [Product(
        id=1,
        name=fake.name(),
        price=100,
        description=fake.text(),
        url=fake.url(),
        image=fake.url(),
    )]
    
    await parser_task.parse(session=session, task=task_queue)

    mock.assert_awaited_once_with(url)
    assert await product_factory.get_all(session)
    
async def test_start_update_task(session: AsyncSession):
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id, interval=10)
    scheduled_old = task.scheduled_at

    await parser_task.update_task(session=session, id=task.id, state=State)

    result = await task_factory.get(session, id=task.id)
    
    assert result.scheduled_at != scheduled_old

@patch("src.app.services.parser.scraper.scraper.scrape", new_callable=AsyncMock)
async def test_start_fail_parsing(mock: AsyncMock, session: AsyncSession, cache: Redis):
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id, interval=10)
    
    task_queue = TaskQueue(id=task.id, url=task.url, user_id=1, mode=ModeTask.INTERVAL)
    await cache.zadd(queue.name_queue, {task_queue.to_json(): 0.8})
    mock.side_effect = ListProductError()
    
    await parser_task.parse(session=session, task=task_queue)

    mock.assert_awaited_once_with(task.url)
    assert await task_factory.get(session, id=task.id) is None