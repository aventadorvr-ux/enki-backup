# Scheduling Agent - Calendar & Bookings
# Location: EC2 3.25.170.226:/home/ubuntu/nz-realestate-ai/app/agents/scheduling_agent.py

from typing import Any, Dict
from datetime import datetime, timedelta
from app.agents.base import BaseAgent

class SchedulingAgent(BaseAgent):
    def __init__(self):
        super().__init__("scheduling")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action")
        if action == "book_showing":
            return await self._book_showing(task.get("data", {}))
        elif action == "inspection":
            return await self._inspection(task.get("data", {}))
        elif action == "availability":
            return await self._availability(task.get("data", {}))
        return {"error": "Unknown action"}
    
    async def _book_showing(self, data: Dict) -> Dict:
        booking = {
            "id": f"BK_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "property_id": data.get("property_id"),
            "datetime": data.get("datetime"),
            "status": "confirmed"
        }
        return {"success": True, "booking": booking}
    
    async def _inspection(self, data: Dict) -> Dict:
        slots = [
            {
                "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "times": ["09:00", "11:00", "14:00"]
            } for i in range(3, 8)
        ]
        return {"property_id": data.get("property_id"), "available_slots": slots}
    
    async def _availability(self, data: Dict) -> Dict:
        return {
            "date": data.get("date"),
            "available": True,
            "slots": ["09:00", "10:00", "11:00", "14:00", "15:00"]
        }
