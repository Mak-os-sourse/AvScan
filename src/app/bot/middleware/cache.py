from aiogram import BaseMiddleware
from redis.asyncio import Redis

from src.app.core.settings import settings

class RedisMiddleware(BaseMiddleware):
    async def __call__(self, hendler, event, data):
        async with Redis.from_url(str(settings.REDIS_URL)) as redis:
            data["redis"] = redis
            result = await hendler(event, data)
            return result