from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

class DBMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker: AsyncSession):
        self.sessionmaker = sessionmaker
        
    async def __call__(self, handler, event, data):
        async with self.sessionmaker() as session:
            data["session"] = session
            result = await handler(event, data)
            await session.commit() 
            return result