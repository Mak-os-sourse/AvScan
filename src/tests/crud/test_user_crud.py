from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.factories.user import user_factory
from src.app.crud.user import user_crud
from src.tests.fake import fake

async def test_insert(session: AsyncSession):
    username = fake.user_name()
    result = await user_crud.create(session, username=username)
    user = await user_factory.get(session, username=username)
    assert user.id == result.id

async def test_get(session: AsyncSession):
    user = await user_factory.add(session, username=fake.user_name())
    result = await user_crud.get(session, id=user.id)
    assert user.id == result.id

async def test_get_all(session: AsyncSession):
    user = await user_factory.add(session, username=fake.user_name())
    result = await user_crud.get_all(session, id=user.id)
    assert result
    assert user.id == result[0].id
    
async def test_update(session: AsyncSession):
    username = fake.user_name()
    new_username = fake.user_name()
    user = await user_factory.add(session, username=username)
    await user_crud.update(session, id=user.id, username=new_username)
    result = await user_factory.get(session, id=user.id)
    assert result.username == new_username
    
async def test_delete(session: AsyncSession):
    username = fake.user_name()
    user = await user_factory.add(session, username=username)
    await user_crud.delete(session, id=user.id)
    result = await user_factory.get(session, id=user.id)
    assert result is None