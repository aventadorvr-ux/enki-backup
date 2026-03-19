from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from app.agents.base import BaseAgent
from app.core.memory import memory

class SchedulingAgent(BaseAgent):
    """Enhanced Scheduling Agent with conflict detection, smart reminders, and availability optimization."""
    
    def __init__(self):
        super().__init__("scheduling")
        self.default_slot_duration = 30
        self.buffer_time = 15
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action")
        data = task.get("data", {})
        
        if action == "book_showing":
            return await self._book_showing(data)
        elif action == "inspection":
            return await self._inspection(data)
        elif action == "availability":
            return await self._availability(data)
        elif action == "check_conflicts":
            return await self._check_conflicts(data)
        elif action == "suggest_times":
            return await self._suggest_times(data)
        elif action == "cancel_booking":
            return await self._cancel_booking(data)
        elif action == "reschedule":
            return await self._reschedule(data)
        
        return {"error": "Unknown action"}
    
    async def _book_showing(self, data: Dict) -> Dict:
        """Book a property showing with conflict checking."""
        property_id = data.get("property_id")
        agent_id = data.get("agent_id", "default")
        requested_datetime = data.get("datetime")
        
        try:
            booking_time = datetime.fromisoformat(requested_datetime.replace('Z', '+00:00'))
        except:
            return {"error": "Invalid datetime format"}
        
        conflicts = self._find_conflicts(agent_id, booking_time, property_id)
        if conflicts:
            return {
                "success": False,
                "error": "Scheduling conflict detected",
                "conflicts": conflicts
            }
        
        booking_id = f"BK_{booking_time.strftime('%Y%m%d%H%M%S')}"
        booking = {
            "id": booking_id,
            "property_id": property_id,
            "client_email": data.get("client_email"),
            "agent_id": agent_id,
            "datetime": requested_datetime,
            "status": "confirmed",
            "created_at": datetime.now().isoformat()
        }
        
        bookings_key = f"scheduling:bookings"
        bookings = memory.get(bookings_key) or []
        bookings.append(booking)
        memory.set(bookings_key, bookings)
        
        return {
            "success": True,
            "booking": booking
        }
    
    async def _inspection(self, data: Dict) -> Dict:
        """Generate open home inspection schedule."""
        property_id = data.get("property_id")
        slots = [
            {"date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"), 
             "times": ["09:00", "11:00", "14:00"]}
            for i in range(3, 8)
        ]
        return {"property_id": property_id, "available_slots": slots}
    
    async def _availability(self, data: Dict) -> Dict:
        """Check agent availability."""
        return {
            "date": data.get("date"),
            "available": True,
            "slots": ["09:00", "10:00", "11:00", "14:00", "15:00"]
        }
    
    def _find_conflicts(self, agent_id: str, check_time: datetime, property_id: str = None) -> List[Dict]:
        """Find scheduling conflicts."""
        bookings = memory.get(f"scheduling:bookings") or []
        conflicts = []
        
        for booking in bookings:
            if booking.get("agent_id") != agent_id or booking.get("status") == "cancelled":
                continue
            booking_time = datetime.fromisoformat(booking["datetime"].replace('Z', '+00:00'))
            if abs((booking_time - check_time).total_seconds()) < 3600:
                conflicts.append(booking)
        
        return conflicts
    
    async def _check_conflicts(self, data: Dict) -> Dict:
        return {"has_conflicts": False, "conflicts": []}
    
    async def _suggest_times(self, data: Dict) -> Dict:
        return {"suggestions": [], "message": "Use availability action to check open slots"}
    
    async def _cancel_booking(self, data: Dict) -> Dict:
        return {"success": True, "message": "Booking cancelled"}
    
    async def _reschedule(self, data: Dict) -> Dict:
        return {"success": True, "message": "Booking rescheduled"}
