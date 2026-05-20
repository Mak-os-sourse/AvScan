from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.app.core.settings import settings

class DB:
    def __init__(self, url: str):
        self.engine = create_async_engine(url, echo=True)
        self.sessionmaker = async_sessionmaker(self.engine)
    
    async def get_session(self):
        async with self.sessionmaker() as session:
            yield session
            await session.commit()
    
    async def metadata_create_all(self, base):
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)
    
    async def metadata_drop_all(self, base):
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.drop_all)

db = DB(url=settings.DB_URL)