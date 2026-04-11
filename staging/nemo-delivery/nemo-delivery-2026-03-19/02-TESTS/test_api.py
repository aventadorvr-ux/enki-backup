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
    assert len(response.json()["agents"]) == 5

def test_lead_agent_qualify():
    response = client.post("/api/v1/agents/lead/process", json={
        "action": "qualify",
        "data": {"budget": 900000, "timeline": "immediate", "pre_approved": True}
    })
    assert response.status_code == 200
    result = response.json()["result"]
    assert result["qualified"] == True
    assert result["score"] >= 80
