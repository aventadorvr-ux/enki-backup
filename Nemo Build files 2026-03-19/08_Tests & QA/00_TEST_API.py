# API Tests
# Location: EC2 3.25.170.226:/home/ubuntu/nz-realestate-ai/tests/test_api.py
# Status: 4/4 tests passing

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "NZ Real Estate AI API"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_list_agents():
    response = client.get("/api/v1/agents")
    assert response.status_code == 200
    agents = response.json()["agents"]
    assert len(agents) == 5
    assert agents[0]["name"] == "lead"

def test_lead_agent_qualify():
    response = client.post(
        "/api/v1/agents/lead/process",
        json={
            "action": "qualify",
            "data": {
                "budget": 900000,
                "timeline": "immediate",
                "pre_approved": True
            }
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert result["result"]["qualified"] == True
    assert result["result"]["priority"] == "high"

# ⚠️ MISSING TESTS:
# - AI service integration tests
# - Database CRUD tests
# - Authentication tests
# - External API tests
# - Load tests
# - End-to-end tests
