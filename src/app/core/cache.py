from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage

from src.app.core.settings import settings

redis = Redis.from_url(url=str(settings.REDIS_URL), decode_responses=True)

storage = RedisStorage(redis)

async def get_redis():
    async with Redis.from_url(url=str(settings.REDIS_URL)) as redis:
        yield redis