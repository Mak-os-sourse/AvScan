from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage

from core.settings import settings

redis = Redis(host=settings.CACHE_HOST, port=settings.CACHE_PORT)

storage = RedisStorage(redis)