from taskiq_redis import RedisStreamBroker

broker = RedisStreamBroker("redis://localhost:6379")

@broker.task
async def scraper():
    pass