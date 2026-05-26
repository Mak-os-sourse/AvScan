from redis.asyncio import Redis
from pydantic import BaseModel

from src.app.services.document import create_product_document
from src.app.types.parser import Product
from src.app.types.queue import TaskQueue

class MessageDocs(BaseModel):
    task_queue: TaskQueue
    products: list[Product]

class PubSubDocs:
    def __init__(self, channel: str):
        self.channel = channel
    
    async def pub(self, redis: Redis, task_qeuee: TaskQueue, products: list[Product]):
        message = MessageDocs(task_queue=task_qeuee, products=products)
        await redis.publish(self.channel, message.model_dump_json())
        
    async def listen_to_send_docs(self, redis: Redis):
        
        