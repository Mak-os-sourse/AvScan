import json
from uuid import uuid4, UUID

from src.app.services.priority import priority_service
from src.app.types.queue import TaskQueue, ModeTask
from src.app.core.settings import settings
from src.app.models.task import Tasks
from src.app.core.cache import redis

class Queue:
    def __init__(self, name_queue: str = "queue:parser"):
        self.name_queue = name_queue
    
    async def get_task(self) -> TaskQueue | None:
        task = await redis.zrevrange(self.name_queue, 0, 0)
        if task:
            data = json.loads(task[0])
            return TaskQueue(**data)
    
    async def add_fast_task(self, url: str, user_id: int) -> int:
        uuid = uuid4().int
        task_queue = TaskQueue(id=uuid, url=url, user_id=user_id, mode=ModeTask.FAST)
        await redis.zadd(self.name_queue, {task_queue.to_json(): settings.FAST_COEFFICIENT})
        return uuid
    
    async def add_task(self, task: Tasks) -> None:
        priority = priority_service.get(task.scheduled_at, task.last_views)
        task_queue = TaskQueue(id=task.id, url=task.url, user_id=task.user_id, mode=ModeTask.INTERVAL)
        await redis.zadd(self.name_queue, {task_queue.to_json(): priority})

    async def update_queue(self, tasks: list[Tasks]) -> None:
        for item in tasks:
            priority = priority_service.get(item.scheduled_at, item.last_views)
            task_queue = TaskQueue(id=item.id, url=item.url, user_id=item.user_id, mode=ModeTask.INTERVAL)
            await redis.zadd(self.name_queue, {task_queue.to_json(): priority})
        
queue = Queue()
