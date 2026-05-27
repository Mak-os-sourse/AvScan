from aiogram import BaseMiddleware
from redis.asyncio import Redis

from src.app.core.cache import redis
from src.app.core.settings import settings

class RedisMiddleware(BaseMiddleware):
    async def __call__(self, hendler, event, data):
        data["redis"] = redis
        result = await hendler(event, data)
        return result