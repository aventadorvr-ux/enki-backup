from fastapi import APIRouter, HTTPException
from typing import Any, Dict
from app.agents.lead_agent import LeadAgent
from app.agents.content_agent import ContentAgent
from app.agents.scheduling_agent import SchedulingAgent
from app.agents.market_agent import MarketIntelligenceAgent
from app.agents.transaction_agent import TransactionCoordinatorAgent

router = APIRouter()

agents = {
    "lead": LeadAgent(),
    "content": ContentAgent(),
    "scheduling": SchedulingAgent(),
    "market_intel": MarketIntelligenceAgent(),
    "transaction": TransactionCoordinatorAgent()
}

@router.post("/agents/{agent_name}/process")
async def process_task(agent_name: str, task: Dict[str, Any]):
    if agent_name not in agents:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    try:
        result = await agents[agent_name].process(task)
        return {"agent": agent_name, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents")
async def list_agents():
    return {
        "agents": [
            {"name": "lead", "description": "Lead qualification and routing"},
            {"name": "content", "description": "Property descriptions and marketing"},
            {"name": "scheduling", "description": "Calendar and booking management"},
            {"name": "market_intel", "description": "CMAs and market analysis"},
            {"name": "transaction", "description": "Deal coordination and compliance"}
        ]
    }
