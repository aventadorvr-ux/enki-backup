# Content Agent - Property Descriptions & Marketing
# Location: EC2 3.25.170.226:/home/ubuntu/nz-realestate-ai/app/agents/content_agent.py

from typing import Any, Dict
from app.agents.base import BaseAgent
from app.core.ai_service import ai_service

class ContentAgent(BaseAgent):
    def __init__(self):
        super().__init__("content")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action")
        data = task.get("data", {})
        
        if action == "description":
            return await self._description(data)
        elif action == "description_ai":
            return await self._description_ai(data)
        elif action == "social":
            return await self._social(data)
        elif action == "social_ai":
            return await self._social_ai(data)
        elif action == "email":
            return await self._email(data)
        
        return {"error": "Unknown action"}
    
    async def _description(self, data: Dict) -> Dict:
        loc = data.get("location", "")
        beds = data.get("bedrooms", 0)
        desc = f"Stunning {beds}-bedroom home in {loc}. Modern living with premium finishes."
        return {"description": desc, "word_count": len(desc.split())}
    
    async def _description_ai(self, data: Dict) -> Dict:
        desc = ai_service.generate_property_description(
            bedrooms=data.get("bedrooms", 3),
            bathrooms=data.get("bathrooms", 2),
            location=data.get("location", "Auckland"),
            features=data.get("features", [])
        )
        return {"description": desc, "word_count": len(desc.split()), "ai_generated": True}
    
    async def _social(self, data: Dict) -> Dict:
        platform = data.get("platform", "facebook")
        listing = data.get("listing", {})
        posts = {"facebook": f"New! {listing.get('bedrooms', 3)} bed in {listing.get('location', '')}"}
        return {"post": posts.get(platform, posts["facebook"]), "platform": platform}
    
    async def _social_ai(self, data: Dict) -> Dict:
        post = ai_service.generate_social_post(
            platform=data.get("platform", "facebook"),
            bedrooms=data.get("bedrooms", 3),
            location=data.get("location", "Auckland"),
            price=data.get("price", "")
        )
        return {"post": post, "platform": data.get("platform", "facebook"), "ai_generated": True}
    
    async def _email(self, data: Dict) -> Dict:
        return {"subject": "Market Updates", "body": "Latest market insights..."}
