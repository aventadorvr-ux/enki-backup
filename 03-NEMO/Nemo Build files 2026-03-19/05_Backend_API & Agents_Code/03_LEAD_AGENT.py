# Lead Agent - Qualification & Routing
# Location: EC2 3.25.170.226:/home/ubuntu/nz-realestate-ai/app/agents/lead_agent.py

from typing import Any, Dict
from app.agents.base import BaseAgent
from app.core.ai_service import ai_service

class LeadAgent(BaseAgent):
    def __init__(self):
        super().__init__("lead")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action")
        data = task.get("data", {})
        
        if action == "qualify":
            return await self._qualify(data)
        elif action == "qualify_ai":
            return await self._qualify_ai(data)
        elif action == "respond":
            return await self._respond(data)
        elif action == "route":
            return await self._route(data)
        
        return {"error": "Unknown action"}
    
    async def _qualify(self, data: Dict) -> Dict:
        score = 0
        if data.get("budget", 0) > 500000: score += 30
        if data.get("timeline") in ["immediate", "1-3 months"]: score += 40
        if data.get("pre_approved"): score += 20
        if data.get("contact_method"): score += 10
        
        return {
            "qualified": score >= 60,
            "score": score,
            "priority": "high" if score >= 80 else "medium" if score >= 60 else "low"
        }
    
    async def _qualify_ai(self, data: Dict) -> Dict:
        result = ai_service.qualify_lead_intelligent(
            budget=data.get("budget", 0),
            timeline=data.get("timeline", ""),
            pre_approved=data.get("pre_approved", False),
            notes=data.get("notes", "")
        )
        return {"ai_analysis": result, "method": "openrouter_claude"}
    
    async def _respond(self, data: Dict) -> Dict:
        t = data.get("type", "general")
        templates = {
            "viewing": "Thanks for your interest. Checking availability...",
            "valuation": "Thanks! Agent will contact within 24h.",
            "general": "Thanks for contacting us!"
        }
        return {"response": templates.get(t, templates["general"]), "type": t}
    
    async def _route(self, data: Dict) -> Dict:
        agents = self.get_state().get("available_agents", [{"name": "Default Agent", "id": "agent_001"}])
        return {"assigned_agent": agents[0], "routing_reason": "Availability match"}
