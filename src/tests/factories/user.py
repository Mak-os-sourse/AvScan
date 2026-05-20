from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.fake import fake
from src.app.models.user import Users
from src.tests.factories.factory import Factory

class UserFactory(Factory):
    def __init__(self):
        super().__init__(Users)
        
    async def add(
        self,
        session: AsyncSession,
        username: str = fake.user_name(),
        is_admin: bool = False,
    ) -> Users:
        return await super().add(
            session,
            username=username,
            is_admin=is_admin,
        )
        
user_factory = UserFactory()