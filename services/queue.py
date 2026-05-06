import json
from uuid import uuid4, UUID
from datetime import datetime

from models.task import Tasks
from core.cache import redis

class Queue:
    async def update_queue(self, tasks: list[Tasks]) -> None:
        for item in tasks:
            priority = self._get_priority(item.scheduled_at, item.last_views)
            await redis.zadd("queue:parser", {json.dumps({"id": item.id, "url": item.url}): priority})
    
    async def add_fast_task(self, url: str) -> UUID:
        uuid = uuid4().hex
        await redis.zadd("queue:parser", {json.dumps({"id": uuid, "url": url}): 0.7})
        return uuid
    
    async def add_task(self, task: Tasks) -> None:
        priority = self._get_priority(task.scheduled_at, task.last_views)
        await redis.zadd("queue:parser", {json.dumps({"id": task.id, "url": task.id}): priority})
    
    def _get_priority(self, time_issue: int, last_views: int) -> int:
        coefficient = 0.8
        time_coefficient = self._format_time_coefficient(time_issue)
        last_views_coefficient = self._format_last_views_coefficient(last_views)
        if time_coefficient <= 0:
            priority = 1
        else:
            priority = (time_coefficient * 0.0000115) * last_views_coefficient * coefficient
        return priority
    
    def _format_time_coefficient(self, time_issue: int) -> int:
        now = time_issue - int(datetime.now().timestamp())
        if now <= 0:
            return 0
        return 86_400 - now
    
    def _format_last_views_coefficient(self, last_views: int) -> int:
        result = 1 - ((1/8) * last_views)
        if result < 0:
            return 0
        return result
        
queue = Queue()
