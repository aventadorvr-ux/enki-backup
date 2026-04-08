from fastapi import APIRouter, HTTPException
from typing import Any, Dict, Optional
from pydantic import BaseModel

from app.agents.lead_agent import LeadAgent
from app.agents.content_agent import ContentAgent
from app.agents.scheduling_agent import SchedulingAgent
from app.agents.market_agent import MarketIntelligenceAgent
from app.agents.transaction_agent import TransactionCoordinatorAgent
from app.core.memory import memory

router = APIRouter()

agents = {
    "lead": LeadAgent(),
    "content": ContentAgent(),
    "scheduling": SchedulingAgent(),
    "market_intel": MarketIntelligenceAgent(),
    "transaction": TransactionCoordinatorAgent(),
}

class ContentRequest(BaseModel):
    content_type: str
    data: dict
    platform: Optional[str] = None


def _normalize(task: Dict[str, Any]):
    if "action" in task and "data" not in task:
        return {
            "action": task["action"],
            "data": {k: v for k, v in task.items() if k != "action"},
        }
    return task


async def _run(agent: str, task: Dict[str, Any]):
    if agent not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    return await agents[agent].process(_normalize(task))


# ========================
# CORE AGENT ROUTES
# ========================

@router.post("/agents/{agent_name}/process")
async def process_task(agent_name: str, task: Dict[str, Any]):
    result = await _run(agent_name, task)
    return {"agent": agent_name, "result": result}


# ========================
# ENKI WRAPPERS (REAL)
# ========================

@router.post("/enki/content/generate")
async def enki_generate_content(request: ContentRequest):
    task = {
        "action": "description_ai" if request.content_type == "property_description" else request.content_type,
        **request.data
    }
    return await _run("content", task)


@router.get("/enki/content/recent")
async def enki_recent_content(limit: int = 10):
    all_items = []

    try:
        store = memory._store if hasattr(memory, "_store") else {}

        for key, value in store.items():
            if key.startswith("content:") and isinstance(value, list):
                for item in value:
                    all_items.append({
                        "source": key,
                        **item
                    })

        all_items.sort(key=lambda x: x.get("generated_at", ""), reverse=True)

        return {
            "items": all_items[:limit],
            "total": len(all_items),
            "status": "active"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/enki/status")
async def enki_status():
    return {
        "status": "operational",
        "agents": list(agents.keys())
    }


@router.get("/enki/overseer/check")
async def overseer_check():
    return {
        "status": "healthy",
        "mode": "direct-agent-runtime"
    }

# ========================
# PROPERTY SEARCH (NEW)
# ========================

import json
from pathlib import Path

@router.post("/enki/property/search")
async def property_search(filters: Dict[str, Any]):
    try:
        data_path = Path(__file__).parent / "data" / "properties.json"
        with open(data_path) as f:
            properties = json.load(f)

        results = []

        for p in properties:
            if filters.get("suburb") and filters["suburb"].lower() not in p["suburb"].lower():
                continue
            if filters.get("max_price") and p["price"] > filters["max_price"]:
                continue
            if filters.get("bedrooms") and p["bedrooms"] != filters["bedrooms"]:
                continue

            results.append(p)

        return {
            "results": results,
            "count": len(results)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
