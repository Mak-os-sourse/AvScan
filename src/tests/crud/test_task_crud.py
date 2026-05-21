from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.factories.task import task_factory
from src.tests.factories.user import user_factory
from src.app.crud.task import task_crud
from src.tests.fake import fake

async def test_insert(session: AsyncSession):
    user = await user_factory.add(session)
    result = await task_crud.create(
        session,
        user_id=user.id,
        url=fake.url(),
        scheduled_at=0,
        interval=0,
    )
    task = await task_factory.get(session, user_id=user.id)
    assert task.id == result.id

async def test_get(session: AsyncSession):
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id)
    result = await task_crud.get(session, id=task.id)
    assert task.id == result.id

async def test_get_all(session: AsyncSession):
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id)
    result = await task_crud.get_all(session, id=task.id)
    assert result
    assert task.id == result[0].id
    
async def test_update(session: AsyncSession):
    url = fake.url()
    new_url = fake.url()
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id, url=url)
    await task_crud.update(session, id=task.id, url=new_url)
    result = await task_factory.get(session, id=task.id)
    assert result.url == new_url
    
async def test_delete(session: AsyncSession):
    user = await user_factory.add(session)
    task = await task_factory.add(session, user_id=user.id)
    await task_crud.delete(session, id=task.id)
    result = await task_factory.get(session, id=task.id)
    assert result is None