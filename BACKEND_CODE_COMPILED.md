# NEMO BACKEND CODE - FULL DOCUMENTATION
## Generated: 2026-03-22

---

## 00_MAIN_APP.py - FastAPI Main Application

```python
# FastAPI Main Application
# Location: EC2 3.25.170.226:/home/ubuntu/nz-realestate-ai/app/main.py
# Status: Running on port 8000

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes import router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-agent AI system for NZ Real Estate",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {
        "message": "NZ Real Estate AI API",
        "version": "1.0.0",
        "agents": ["lead", "content", "scheduling", "market_intel", "transaction"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

---

## 01_API_ROUTES.py - Agent Endpoints

```python
# API Routes
# Location: EC2 3.25.170.226:/home/ubuntu/nz-realestate-ai/app/api/routes.py

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
```

---

## AGENT ARCHITECTURE

### Available Agents:
1. **Lead Agent** - Qualifies and routes property leads
2. **Content Agent** - Generates property descriptions and marketing copy
3. **Scheduling Agent** - Manages calendar and booking
4. **Market Intelligence Agent** - Provides CMAs and market analysis
5. **Transaction Agent** - Coordinates deals and compliance

### API Endpoints:
- `GET /` - API info and status
- `GET /health` - Health check
- `GET /api/v1/agents` - List all agents
- `POST /api/v1/agents/{agent_name}/process` - Execute agent task

### Infrastructure:
- **Server:** EC2 3.25.170.226
- **Port:** 8000
- **Framework:** FastAPI
- **CORS:** Enabled for all origins

---

## END OF BACKEND DOCUMENTATION
