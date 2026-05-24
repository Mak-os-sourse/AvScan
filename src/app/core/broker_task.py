from taskiq_redis import RedisStreamBroker

from src.app.core.settings import settings

broker = RedisStreamBroker(str(settings.REDIS_URL))

