import json
from enum import StrEnum
from typing import Literal
from dataclasses import dataclass, asdict

class ModeTask(StrEnum):
    FAST: str = "Fast"
    INTERVAL: str = "Interval"
    
@dataclass
class TaskQueue:
    id: int
    url: str
    user_id: int
    mode: Literal["Fast", "Interval"]
    completed: bool = False

    def to_dict(self):
        return asdict(self)
    
    def to_json(self):
        return json.dumps(self.to_dict())