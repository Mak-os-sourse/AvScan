import pytest_asyncio
from sqlalchemy import delete
from redis.asyncio import Redis
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.app.models import *
from src.app.core.db import db
from src.app.core.base import Base
from src.app.core.settings import settings

db.engine = create_async_engine(str(settings.DB_URL), poolclass=NullPool)
db.sessionmaker = async_sessionmaker(db.engine)

@pytest_asyncio.fixture(autouse=True, scope="session")
async def setup_db():
    await db.metadata_drop_all(Base)
    await db.metadata_create_all(Base)
    yield

@pytest_asyncio.fixture
async def session():
    async with db.sessionmaker() as session:
        yield session
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(delete(table))
        await session.commit()

@pytest_asyncio.fixture
async def cache():
    redis = Redis.from_url(str(settings.REDIS_URL))
    yield redis
    await redis.flushall()
    await redis.aclose()