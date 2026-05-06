from crud.factory import BaseCrud
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import Users

class UserCRUD(BaseCrud):
    def __init__(self):
        super().__init__(Users)
        
    async def create(self,
        session: AsyncSession,
        username: str,
        is_admin: bool  = False,
        ) -> Users:
        return await super().insert(
            session,
            username=username,
            is_admin=is_admin
        )
    
    async def get(self, session: AsyncSession, **kargs) -> Users | None:
        where = super().get_where(**kargs)
        result = await super().select(session, where=where)
        return result[0] if result else None
    
    async def get_all(self, session: AsyncSession, **kargs) -> list[Users]:
        where = super().get_where(**kargs)
        return await super().select(session, where=where)
    
    async def update(self, session: AsyncSession, id: int, **values):
        return await super().update(session, where=[Users.id == id], **values)
    
    async def delete(self, session: AsyncSession, id: int, **kargs):
        where = super().get_where(**kargs, id=id)
        return await super().delete(session, where=where)

user_crud = UserCRUD()