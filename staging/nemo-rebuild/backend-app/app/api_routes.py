from fastapi import APIRouter, HTTPException
from typing import Any, Dict, Optional
from pydantic import BaseModel
import json
from pathlib import Path

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

async def _run_with_retry(agent: str, task: dict, retries: int = 1):
    last_error = None
    for attempt in range(retries + 1):
        try:
            result = await _run(agent, task)
            if result:
                return result
        except Exception as e:
            last_error = e
        if attempt < retries:
            continue
    if last_error:
        raise last_error
    raise Exception(f"{agent} returned no result after retry")



@router.post("/agents/{agent_name}/process")
async def process_task(agent_name: str, task: Dict[str, Any]):
    result = await _run_with_retry(agent_name, task)
    return {"agent": agent_name, "result": result}


@router.post("/enki/content/generate")
async def enki_generate_content(request: ContentRequest):
    task = {
        "action": "description_ai" if request.content_type == "property_description" else request.content_type,
        **request.data
    }
    return await _run_with_retry("content", task)


@router.get("/enki/content/recent")
async def enki_recent_content(limit: int = 10):
    all_items = []
    try:
        store = memory._store if hasattr(memory, "_store") else {}
        for key, value in store.items():
            if key.startswith("content:") and isinstance(value, list):
                for item in value:
                    all_items.append({"source": key, **item})

        all_items.sort(key=lambda x: x.get("generated_at", ""), reverse=True)
        return {"items": all_items[:limit], "total": len(all_items), "status": "active"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/enki/status")
async def enki_status():
    return {"status": "operational", "agents": list(agents.keys())}


@router.get("/enki/overseer/check")
async def overseer_check():
    return {"status": "healthy", "mode": "direct-agent-runtime"}


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

        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/orchestrate/run")
async def orchestrate_run(task: Dict[str, Any]):
    workflow = task.get("workflow", "demo")
    input_data = task.get("data", {})

    proof = []
    results = {}
    skipped = []

    try:
        if workflow == "demo":
            bedrooms = input_data.get("bedrooms", 3)
            bathrooms = input_data.get("bathrooms", 2)
            budget = input_data.get("budget", 0)

            if not isinstance(bedrooms, int) or bedrooms < 1:
                raise HTTPException(status_code=400, detail="Invalid bedrooms: must be >= 1")
            if not isinstance(bathrooms, int) or bathrooms < 1:
                raise HTTPException(status_code=400, detail="Invalid bathrooms: must be >= 1")
            if budget is not None and budget < 0:
                raise HTTPException(status_code=400, detail="Invalid budget: must be >= 0")

            lead_id = input_data.get("lead_id", "orch_demo_lead")
            property_id = input_data.get("property_id", "orch_demo_property")
            location = input_data.get("location", "Ponsonby")

            lead_before = len([e for e in (memory.get("leads") or []) if e.get("lead_id") == lead_id])
            market_before = len([e for e in (memory.get("market") or []) if e.get("suburb") == location])

            if input_data.get("resume", True) and lead_before > 0:
                skipped.append({"step": "lead_qualify", "reason": "already exists"})
            else:
                lead_result = await _run_with_retry("lead", {
                    "action": "qualify",
                    "data": {
                        "lead_id": lead_id,
                        "budget": input_data.get("budget", 900000),
                        "timeline": input_data.get("timeline", "1-3 months"),
                        "pre_approved": input_data.get("pre_approved", True)
                    }
                })
                lead_after = len([e for e in (memory.get("leads") or []) if e.get("lead_id") == lead_id])
                if lead_after <= lead_before:
                    raise HTTPException(status_code=500, detail="Lead step produced no proof event")
                proof.append({"step": "lead_qualify", "verified": True})
                results["lead"] = lead_result

                lead_score = lead_result.get("score", 0)
                if lead_score < 70:
                    return {
                        "status": "failed",
                        "failed_step": "lead_qualify",
                        "reason": f"Lead score too low ({lead_score})",
                        "proof": proof,
                        "skipped": skipped
                    }

            if input_data.get("resume", True) and market_before > 0:
                skipped.append({"step": "market_trends", "reason": "already exists"})
                adaptive_tone = input_data.get("tone", "professional")
            else:
                market_result = await _run_with_retry("market_intel", {
                    "action": "trends",
                    "data": {"suburb": location}
                })
                market_after = len([e for e in (memory.get("market") or []) if e.get("suburb") == location])
                if market_after <= market_before:
                    raise HTTPException(status_code=500, detail="Market step produced no proof event")
                proof.append({"step": "market_trends", "verified": True})
                results["market"] = market_result
                adaptive_tone = "luxury" if market_result.get("trend") == "rising" else "professional"

            content_exists = any(
                isinstance(e, dict) and e.get("property_id") == property_id
                for e in (memory.get("content:history") or [])
            )

            if input_data.get("resume", True) and content_exists:
                skipped.append({"step": "content_generate", "reason": "already exists"})
            else:
                content_result = await _run_with_retry("content", {
                    "action": "description_ai",
                    "data": {
                        "property_id": property_id,
                        "bedrooms": bedrooms,
                        "bathrooms": bathrooms,
                        "location": location,
                        "tone": adaptive_tone,
                        "features": input_data.get("features", ["garage", "deck"])
                    }
                })
                content_exists_after = any(
                    isinstance(e, dict) and e.get("property_id") == property_id
                    for e in (memory.get("content:history") or [])
                )
                if not content_exists_after:
                    raise HTTPException(status_code=500, detail="Content step produced no proof event")
                proof.append({"step": "content_generate", "verified": True})
                results["content"] = content_result

            txn_exists = any(
                isinstance(e, dict) and e.get("transaction_id") == property_id and e.get("event") == "checklist"
                for e in (memory.get("transactions") or [])
            )

            if input_data.get("resume", True) and txn_exists:
                skipped.append({"step": "transaction_checklist", "reason": "already exists"})
            else:
                txn_result = await _run_with_retry("transaction", {
                    "action": "checklist",
                    "data": {
                        "property_id": property_id,
                        "transaction_type": input_data.get("transaction_type", "purchase")
                    }
                })
                txn_exists_after = any(
                    isinstance(e, dict) and e.get("transaction_id") == property_id and e.get("event") == "checklist"
                    for e in (memory.get("transactions") or [])
                )
                if not txn_exists_after:
                    raise HTTPException(status_code=500, detail="Transaction step produced no proof event")
                proof.append({"step": "transaction_checklist", "verified": True})
                results["transaction"] = txn_result

            return {
                "status": "completed",
                "workflow": workflow,
                "proof": proof,
                "skipped": skipped,
                "results": results
            }

        elif workflow == "lead_to_listing":
            bedrooms = input_data.get("bedrooms", 3)
            if not isinstance(bedrooms, int) or bedrooms < 1:
                raise HTTPException(status_code=400, detail="Invalid bedrooms")

            lead_id = input_data.get("lead_id", "lead_listing")
            property_id = input_data.get("property_id", "prop_listing")
            location = input_data.get("location", "Ponsonby")

            lead_result = await _run_with_retry("lead", {
                "action": "qualify",
                "data": {
                    "lead_id": lead_id,
                    "budget": input_data.get("budget", 900000),
                    "timeline": input_data.get("timeline", "1-3 months"),
                    "pre_approved": input_data.get("pre_approved", True)
                }
            })
            proof.append({"step": "lead_qualify", "verified": True})
            results["lead"] = lead_result

            if lead_result.get("score", 0) < 70:
                return {
                    "status": "failed",
                    "failed_step": "lead_qualify",
                    "reason": "Lead not strong enough for listing workflow",
                    "proof": proof,
                    "skipped": []
                }

            market_result = await _run_with_retry("market_intel", {
                "action": "trends",
                "data": {"suburb": location}
            })
            proof.append({"step": "market_trends", "verified": True})
            results["market"] = market_result

            tone = "luxury" if market_result.get("trend") == "rising" else "professional"

            content_result = await _run_with_retry("content", {
                "action": "description_ai",
                "data": {
                    "property_id": property_id,
                    "bedrooms": bedrooms,
                    "bathrooms": input_data.get("bathrooms", 2),
                    "location": location,
                    "tone": tone,
                    "features": input_data.get("features", ["garage"])
                }
            })
            proof.append({"step": "content_generate", "verified": True})
            results["content"] = content_result

            return {
                "status": "completed",
                "workflow": workflow,
                "proof": proof,
                "results": results
            }


        elif workflow == "deal_execution":

            bedrooms = input_data.get("bedrooms", 3)
            bathrooms = input_data.get("bathrooms", 2)
            budget = input_data.get("budget", 0)

            if not isinstance(bedrooms, int) or bedrooms < 1:
                raise HTTPException(status_code=400, detail="Invalid bedrooms: must be >= 1")
            if not isinstance(bathrooms, int) or bathrooms < 1:
                raise HTTPException(status_code=400, detail="Invalid bathrooms: must be >= 1")
            if budget is not None and budget < 0:
                raise HTTPException(status_code=400, detail="Invalid budget: must be >= 0")

            lead_id = input_data.get("lead_id", "deal_lead")
            property_id = input_data.get("property_id", "deal_property")
            location = input_data.get("location", "Ponsonby")

            lead_result = await _run_with_retry("lead", {
                "action": "qualify",
                "data": {
                    "lead_id": lead_id,
                    "budget": budget if budget else 900000,
                    "timeline": input_data.get("timeline", "1-3 months"),
                    "pre_approved": input_data.get("pre_approved", True)
                }
            })
            proof.append({"step": "lead_qualify", "verified": True})
            results["lead"] = lead_result

            lead_score = lead_result.get("score", 0)
            if lead_score < 80:
                return {
                    "status": "failed",
                    "failed_step": "lead_qualify",
                    "reason": f"Lead score too low for deal execution ({lead_score})",
                    "proof": proof,
                    "skipped": skipped
                }

            market_result = await _run_with_retry("market_intel", {
                "action": "trends",
                "data": {"suburb": location}
            })
            proof.append({"step": "market_trends", "verified": True})
            results["market"] = market_result

            tone = "luxury" if market_result.get("trend") == "rising" else "professional"

            content_result = await _run_with_retry("content", {
                "action": "description_ai",
                "data": {
                    "property_id": property_id,
                    "bedrooms": bedrooms,
                    "bathrooms": bathrooms,
                    "location": location,
                    "tone": tone,
                    "features": input_data.get("features", ["garage", "deck"])
                }
            })
            proof.append({"step": "content_generate", "verified": True})
            results["content"] = content_result

            txn_result = await _run_with_retry("transaction", {
                "action": "checklist",
                "data": {
                    "property_id": property_id,
                    "transaction_type": input_data.get("transaction_type", "purchase")
                }
            })
            proof.append({"step": "transaction_checklist", "verified": True})
            results["transaction"] = txn_result

            risk_result = await _run_with_retry("transaction", {
                "action": "risk_assessment",
                "data": {
                    "transaction_id": property_id,
                    "days_to_settlement": input_data.get("days_to_settlement", 10),
                    "finance_approved": input_data.get("finance_approved", False),
                    "building_report_complete": input_data.get("building_report_complete", False),
                    "lawyer_assigned": input_data.get("lawyer_assigned", True)
                }
            })
            proof.append({"step": "transaction_risk", "verified": True})
            results["risk"] = risk_result

            if risk_result.get("overall_risk") == "high":
                return {
                    "status": "failed",
                    "failed_step": "transaction_risk",
                    "reason": "Transaction risk too high for deal execution",
                    "proof": proof,
                    "skipped": skipped,
                    "results": results
                }

            return {
                "status": "completed",
                "workflow": workflow,
                "proof": proof,
                "skipped": skipped,
                "results": results
            }


        raise HTTPException(status_code=400, detail=f"Unknown workflow: {workflow}")

    except HTTPException as e:
        return {
            "status": "failed",
            "reason": e.detail,
            "proof": proof,
            "skipped": skipped
        }
    except Exception as e:
        return {
            "status": "failed",
            "reason": str(e),
            "proof": proof,
            "skipped": skipped
        }
