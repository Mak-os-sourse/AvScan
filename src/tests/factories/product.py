from numpy import random
from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.fake import fake
from src.app.models.product import Products
from src.tests.factories.factory import Factory

class ProductFactory(Factory):
    def __init__(self):
        super().__init__(Products)
        
    async def add(
        self,
        session: AsyncSession,
        user_id: int,
        url: str = fake.url(),
        name: str = fake.name(),
        url_photo: str = fake.url(),
        description: str = fake.text(),
        price: str | int = random.randint(0, 10000),
        id_product: int = random.randint(0, 1000),
    ) -> Products:
        return await super().add(
            session,
            url=url,
            id_product=id_product,
            name=name, price=str(price),
            description=description,
            url_photo=url_photo,
            user_id=user_id
        )
        
product_factory = ProductFactory()