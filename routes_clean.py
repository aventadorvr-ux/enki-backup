from fastapi import APIRouter, HTTPException
from typing import Any, Dict
from pydantic import BaseModel
import subprocess
import json
import os
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

# Environment setup
ENV = {
    "NEMO_DB": "/home/ubuntu/enki-agentic/data/leads.db",
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "")
}

# Request models
class LeadInquiry(BaseModel):
    source: str
    contact_info: str
    message: str

class LeadContinue(BaseModel):
    lead_id: int
    message: str

class ContentRequest(BaseModel):
    content_type: str
    data: dict
    platform: str = None

# Original agent routes
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

# ENKI Lead Terminator Routes
@router.post("/enki/leads/process")
async def enki_process_lead(inquiry: LeadInquiry):
    """ENKI: Process lead with AI qualification"""
    try:
        result = subprocess.run(
            [
                "/home/ubuntu/enki-agentic/venv/bin/python3",
                "/home/ubuntu/enki-agentic/scripts/lead_terminator.py",
                "process",
                inquiry.source,
                inquiry.contact_info,
                inquiry.message
            ],
            capture_output=True,
            text=True,
            env={**os.environ, **ENV},
            timeout=30
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/enki/leads/hot")
async def enki_hot_leads():
    """ENKI: Get hot leads requiring immediate action"""
    try:
        result = subprocess.run(
            [
                "/home/ubuntu/enki-agentic/venv/bin/python3",
                "/home/ubuntu/enki-agentic/scripts/lead_terminator.py",
                "hot"
            ],
            capture_output=True,
            text=True,
            env={**os.environ, **ENV},
            timeout=10
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/enki/stats")
async def enki_stats():
    """ENKI: Get lead statistics"""
    try:
        result = subprocess.run(
            [
                "/home/ubuntu/enki-agentic/venv/bin/python3",
                "/home/ubuntu/enki-agentic/scripts/lead_terminator.py",
                "stats"
            ],
            capture_output=True,
            text=True,
            env={**os.environ, **ENV},
            timeout=10
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ENKI Content Forge Routes
@router.post("/enki/content/generate")
async def enki_generate_content(request: ContentRequest):
    """ENKI Content Forge: Generate marketing content"""
    try:
        cmd = [
            "/home/ubuntu/enki-agentic/venv/bin/python3",
            "/home/ubuntu/enki-agentic/scripts/content_forge.py",
            request.content_type,
            json.dumps(request.data)
        ]
        if request.platform:
            cmd.insert(3, request.platform)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env={**os.environ, **ENV},
            timeout=45
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/enki/content/templates")
async def enki_content_templates(type: str = None):
    """ENKI Content Forge: Get content templates"""
    try:
        cmd = [
            "/home/ubuntu/enki-agentic/venv/bin/python3",
            "/home/ubuntu/enki-agentic/scripts/content_forge.py",
            "templates"
        ]
        if type:
            cmd.append(type)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/enki/content/recent")
async def enki_recent_content(limit: int = 10):
    """ENKI Content Forge: Recently generated content"""
    try:
        result = subprocess.run(
            [
                "/home/ubuntu/enki-agentic/venv/bin/python3",
                "/home/ubuntu/enki-agentic/scripts/content_forge.py",
                "recent"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ENKI System Status
@router.get("/enki/status")
async def enki_status():
    """ENKI: System status"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "agents": {
            "lead_terminator": "active",
            "content_forge": "active",
            "market_intel": "queued",
            "scheduler": "queued",
            "transaction": "queued"
        }
    }

# AGen_OVACa Routes
@router.get("/enki/overseer/check")
async def overseer_check():
    """AGen_OVACa: Run health check"""
    try:
        result = subprocess.run(
            [
                "/home/ubuntu/enki-agentic/venv/bin/python3",
                "/home/ubuntu/enki-agentic/scripts/agen_ovaca.py",
                "check"
            ],
            capture_output=True,
            text=True,
            env={**os.environ, **ENV},
            timeout=30
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/enki/overseer/report")
async def overseer_report():
    """AGen_OVACa: Full system report"""
    try:
        result = subprocess.run(
            [
                "/home/ubuntu/enki-agentic/venv/bin/python3",
                "/home/ubuntu/enki-agentic/scripts/agen_ovaca.py",
                "report"
            ],
            capture_output=True,
            text=True,
            env={**os.environ, **ENV},
            timeout=30
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
