from datetime import datetime

from src.app.core.settings import settings

class Priority:
    def get(self, time_issue: int) -> float:
        time_coefficient = self._format_time_coefficient(time_issue)

        if time_coefficient <= 0:
            priority = 1
        else:
            priority = (time_coefficient * 0.0000115) * settings.COEFFICIENT
        return priority
    
    def _format_time_coefficient(self, time_issue: int) -> int:
        now = time_issue - int(datetime.now().timestamp())
        if now <= 0:
            return 0
        return 86_400 - now

    
priority_service = Priority()