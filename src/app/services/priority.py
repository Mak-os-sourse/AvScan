from datetime import datetime

from src.app.core.settings import settings

class Priority:
    def get(self, time_issue: int, last_views: int) -> int:
        print(settings.COEFFICIENT, time_issue)
        time_coefficient = self._format_time_coefficient(time_issue)
        last_views_coefficient = self._format_last_views_coefficient(last_views)
        if time_coefficient <= 0:
            priority = 1
        else:
            priority = (time_coefficient * 0.0000115) * last_views_coefficient * settings.COEFFICIENT
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
    
priority_service = Priority()