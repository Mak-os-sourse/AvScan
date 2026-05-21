from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.factories.product import product_factory
from src.tests.factories.user import user_factory
from src.app.crud.product import product_crud
from src.tests.fake import fake

async def test_insert(session: AsyncSession):
    user = await user_factory.add(session)
    result = await product_crud.create(
        session,
        user_id=user.id,
        url=fake.url(),
        id_product=1,
        name=fake.name(),
        description=fake.text(),
        price=1000,
        url_photo=fake.url(),
        task_id=1,
    )
    product = await product_factory.get(session, user_id=user.id)
    assert product.id == result.id

async def test_get(session: AsyncSession):
    user = await user_factory.add(session)
    product = await product_factory.add(session, user_id=user.id)
    result = await product_crud.get(session, id=product.id)
    assert product.id == result.id

async def test_get_all(session: AsyncSession):
    user = await user_factory.add(session)
    product = await product_factory.add(session, user_id=user.id)
    result = await product_crud.get_all(session, id=product.id)
    assert result
    assert product.id == result[0].id
    
async def test_update(session: AsyncSession):
    url = fake.url()
    new_url = fake.url()
    user = await user_factory.add(session)
    product = await product_factory.add(session, user_id=user.id, url=url)
    await product_crud.update(session, id=product.id, url=new_url)
    result = await product_factory.get(session, id=product.id)
    assert result.url == new_url
    
async def test_delete(session: AsyncSession):
    user = await user_factory.add(session)
    product = await product_factory.add(session, user_id=user.id)
    await product_crud.delete(session, id=product.id)
    result = await product_factory.get(session, id=user.id)
    assert result is None