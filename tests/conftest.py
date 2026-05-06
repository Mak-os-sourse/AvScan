import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import models
from core.db import db
from core.base import Base
from core.cache import redis
from core.settings import settings

db.engine = create_async_engine(settings.DB_URL, poolclass=NullPool)
db.sessionmaker = async_sessionmaker(db.engine)

@pytest_asyncio.fixture(autouse=True, scope="session")
async def setup_db():
    await db.metadata_drop_all(Base)
    await db.metadata_create_all(Base)
    yield
    await db.metadata_drop_all(Base)

@pytest_asyncio.fixture
async def session():
    async with db.sessionmaker() as session:
        yield session
        for table in Base.metadata.tables:
            await session.execute(delete(table))
        await session.commit()

@pytest_asyncio.fixture
async def cache():
    yield redis
    await redis.flushall()
    await redis.aclose()