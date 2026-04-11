from typing import Any, Dict, List
from datetime import datetime
from app.agents.base import BaseAgent
from app.core.ai_service import ai_service
from app.core.memory import memory

class MarketIntelligenceAgent(BaseAgent):
    """Enhanced Market Intelligence Agent with AI-powered analysis and investment scoring."""
    
    def __init__(self):
        super().__init__("market_intel")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action")
        data = task.get("data", {})
        
        if action == "cma":
            return await self._generate_cma(data)
        elif action == "track_competitor":
            return await self._track_competitor(data)
        elif action == "trends":
            return await self._analyze_trends(data)
        elif action == "market_report":
            return await self._market_report(data)
        elif action == "investment_score":
            return await self._investment_score(data)
        elif action == "predict_price":
            return await self._predict_price(data)
        
        return {"error": "Unknown action"}
    
    async def _generate_cma(self, data: Dict) -> Dict:
        """Generate Comparative Market Analysis with AI insights."""
        address = data.get("address", "")
        suburb = data.get("suburb", "")
        bedrooms = data.get("bedrooms", 3)
        bathrooms = data.get("bathrooms", 2)
        
        prediction = ai_service.predict_sale_price(
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            suburb=suburb,
            land_size=data.get("land_size"),
            condition=data.get("condition", "good")
        )
        
        estimate = data.get("estimated_value", 800000)
        comparables = [
            {"address": f"123 Similar St, {suburb}", "price": estimate * 0.95, "days_on_market": 12},
            {"address": f"456 Comparable Ave, {suburb}", "price": estimate * 1.05, "days_on_market": 8},
        ]
        
        return {
            "subject_property": address,
            "suburb": suburb,
            "estimated_value": estimate,
            "ai_prediction": prediction,
            "comparables": comparables,
            "confidence": prediction.get("confidence", "medium"),
            "market_days_estimate": prediction.get("market_days_estimate", "30-45 days")
        }
    
    async def _track_competitor(self, data: Dict) -> Dict:
        """Track competitor agent performance."""
        return {
            "competitor": data.get("agent_name"),
            "listings_count": 15,
            "avg_days_on_market": 21,
            "status": "tracking"
        }
    
    async def _analyze_trends(self, data: Dict) -> Dict:
        """Analyze market trends with AI insights."""
        suburb = data.get("suburb", "")
        ai_analysis = ai_service.analyze_market(suburb)
        
        return {
            "suburb": suburb,
            "median_price": 850000,
            "price_change": 2.5,
            "inventory_level": "low",
            "trend": "rising",
            "ai_insights": ai_analysis.get("analysis", ""),
            "analyzed_at": datetime.now().isoformat()
        }
    
    async def _market_report(self, data: Dict) -> Dict:
        """Generate comprehensive market report."""
        suburbs = data.get("suburbs", ["Auckland Central"])
        
        return {
            "report_id": f"RPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "suburbs_analyzed": suburbs,
            "generated_at": datetime.now().isoformat(),
            "summary": f"Market analysis for {len(suburbs)} suburbs"
        }
    
    async def _investment_score(self, data: Dict) -> Dict:
        """Calculate investment potential score."""
        suburb = data.get("suburb", "")
        price = data.get("price", 0)
        
        # Simple scoring logic
        score = 50
        if "auckland" in suburb.lower():
            score += 20
        if price < 800000:
            score += 15
        
        return {
            "suburb": suburb,
            "investment_score": score,
            "rating": "Good" if score >= 70 else "Average" if score >= 50 else "Below Average",
            "factors": ["Location", "Price point", "Market trends"]
        }
    
    async def _predict_price(self, data: Dict) -> Dict:
        """Predict sale price for a property."""
        return ai_service.predict_sale_price(
            bedrooms=data.get("bedrooms", 3),
            bathrooms=data.get("bathrooms", 2),
            suburb=data.get("suburb", ""),
            land_size=data.get("land_size"),
            condition=data.get("condition", "good")
        )
