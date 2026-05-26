from enum import StrEnum
from typing import Literal
from pydantic import BaseModel

class ModeTask(StrEnum):
    FAST: str = "Fast"
    INTERVAL: str = "Interval"
    
class TaskQueue(BaseModel):
    id: int
    url: str
    user_id: int
    mode: Literal["Fast", "Interval"]
    completed: bool = False