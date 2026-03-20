#!/usr/bin/env python3
"""
ENKI API - Lead Management Endpoints
Integrates Lead Terminator with NEMO backend
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
import subprocess
import json
import os

router = APIRouter(prefix="/api/v1/enki", tags=["enki"])

# Environment setup
ENV = {
    "NEMO_DB": "/home/ubuntu/enki-agentic/data/leads.db",
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID", "")
}

class LeadInquiry(BaseModel):
    source: str
    contact_info: str
    message: str

class LeadResponse(BaseModel):
    lead_id: int
    response: str
    score: int
    hot: bool

class LeadContinue(BaseModel):
    lead_id: int
    message: str

class Lead(BaseModel):
    id: int
    source: str
    contact: str
    score: int
    message: str
    created: str

@router.post("/leads/process", response_model=LeadResponse)
async def process_lead(inquiry: LeadInquiry):
    """Process a new lead inquiry and return AI response."""
    try:
        result = subprocess.run(
            [
                "python3", 
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
            raise HTTPException(status_code=500, detail=f"Lead processing failed: {result.stderr}")
        
        return json.loads(result.stdout)
    
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Lead processing timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/leads/continue", response_model=LeadResponse)
async def continue_conversation(data: LeadContinue):
    """Continue an existing lead conversation."""
    try:
        result = subprocess.run(
            [
                "python3",
                "/home/ubuntu/enki-agentic/scripts/lead_terminator.py",
                "continue",
                str(data.lead_id),
                data.message
            ],
            capture_output=True,
            text=True,
            env={**os.environ, **ENV},
            timeout=30
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Conversation failed: {result.stderr}")
        
        return json.loads(result.stdout)
    
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Conversation timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leads/hot", response_model=List[Lead])
async def get_hot_leads():
    """Get all hot leads requiring immediate action."""
    try:
        result = subprocess.run(
            [
                "python3",
                "/home/ubuntu/enki-agentic/scripts/lead_terminator.py",
                "hot"
            ],
            capture_output=True,
            text=True,
            env={**os.environ, **ENV},
            timeout=10
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Failed to get hot leads: {result.stderr}")
        
        leads = json.loads(result.stdout)
        return [Lead(**lead) for lead in leads]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leads/stats")
async def get_lead_stats():
    """Get lead processing statistics."""
    try:
        result = subprocess.run(
            [
                "python3",
                "/home/ubuntu/enki-agentic/scripts/lead_terminator.py",
                "stats"
            ],
            capture_output=True,
            text=True,
            env={**os.environ, **ENV},
            timeout=10
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Failed to get stats: {result.stderr}")
        
        return json.loads(result.stdout)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_enki_status():
    """Get ENKI system status."""
    return {
        "status": "operational",
        "version": "1.0.0",
        "agents": {
            "lead_terminator": "active",
            "content_forge": "building",
            "market_intel": "queued",
            "scheduler": "queued",
            "transaction": "queued"
        }
    }
