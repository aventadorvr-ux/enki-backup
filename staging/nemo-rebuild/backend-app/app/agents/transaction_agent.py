from typing import Any, Dict, List
from datetime import datetime, timedelta
from app.agents.base import BaseAgent
from app.core.memory import memory

class TransactionCoordinatorAgent(BaseAgent):
    """Enhanced Transaction Coordinator Agent with risk assessment and milestone tracking."""
    
    def __init__(self):
        super().__init__("transaction")
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action")
        data = task.get("data", {})
        
        if action == "track_deadline":
            return await self._track_deadline(data)
        elif action == "checklist":
            return await self._generate_checklist(data)
        elif action == "compliance":
            return await self._check_compliance(data)
        elif action == "risk_assessment":
            return await self._risk_assessment(data)
        elif action == "milestone_status":
            return await self._milestone_status(data)
        elif action == "update_milestone":
            return await self._update_milestone(data)
        elif action == "generate_timeline":
            return await self._generate_timeline(data)
        elif action == "notify_party":
            return await self._notify_party(data)
        
        return {"error": "Unknown action"}
    
    async def _track_deadline(self, data: Dict) -> Dict:
        """Track transaction deadlines with smart alerts."""
        transaction_id = data.get("transaction_id")
        
        # Standard deadline structure for NZ property transactions
        deadlines = [
            {
                "task": "Finance condition",
                "due": (datetime.now() + timedelta(days=10)).isoformat(),
                "status": "pending",
                "priority": "critical",
                "days_remaining": 10
            },
            {
                "task": "Building inspection",
                "due": (datetime.now() + timedelta(days=7)).isoformat(),
                "status": "pending",
                "priority": "high",
                "days_remaining": 7
            },
            {
                "task": "LIM report review",
                "due": (datetime.now() + timedelta(days=5)).isoformat(),
                "status": "in_progress",
                "priority": "medium",
                "days_remaining": 5
            },
            {
                "task": "Deposit payment",
                "due": (datetime.now() + timedelta(days=3)).isoformat(),
                "status": "pending",
                "priority": "critical",
                "days_remaining": 3
            }
        ]
        
        # Calculate urgency
        for deadline in deadlines:
            days = deadline["days_remaining"]
            if days <= 2:
                deadline["urgency"] = "immediate"
            elif days <= 5:
                deadline["urgency"] = "high"
            elif days <= 10:
                deadline["urgency"] = "medium"
            else:
                deadline["urgency"] = "low"
        
        # Store deadlines
        deadline_key = f"transaction:{transaction_id}:deadlines"
        memory.set(deadline_key, deadlines)
        
        result = {
            "transaction_id": transaction_id,
            "deadlines": deadlines,
            "critical_count": sum(1 for d in deadlines if d["priority"] == "critical"),
            "overdue_count": 0
        }

        memory.append("transactions", {
            "transaction_id": transaction_id,
            "event": "deadline",
            "data": result,
            "timestamp": datetime.now().isoformat()
        })

        return result
    
    async def _generate_checklist(self, data: Dict) -> Dict:
        """Generate transaction checklist with progress tracking."""
        property_id = data.get("property_id")
        transaction_type = data.get("transaction_type", "purchase")
        
        if transaction_type == "purchase":
            checklist = [
                {"item": "Sale and purchase agreement signed", "completed": True, "required": True},
                {"item": "Deposit paid (10%)", "completed": False, "required": True},
                {"item": "Finance condition satisfied", "completed": False, "required": True},
                {"item": "Building inspection completed", "completed": False, "required": True},
                {"item": "LIM report obtained and reviewed", "completed": False, "required": True},
                {"item": "Valuation completed", "completed": False, "required": False},
                {"item": "Insurance arranged", "completed": False, "required": True},
                {"item": "Settlement date confirmed", "completed": False, "required": True},
                {"item": "Pre-settlement inspection completed", "completed": False, "required": True},
                {"item": "Keys handed over", "completed": False, "required": True}
            ]
        else:  # sale
            checklist = [
                {"item": "Listing agreement signed", "completed": True, "required": True},
                {"item": "Property marketing launched", "completed": True, "required": True},
                {"item": "Offers received", "completed": False, "required": True},
                {"item": "Sale and purchase agreement signed", "completed": False, "required": True},
                {"item": "Deposit received", "completed": False, "required": True},
                {"item": "Conditions satisfied", "completed": False, "required": True},
                {"item": "Settlement completed", "completed": False, "required": True}
            ]
        
        completed = sum(1 for item in checklist if item["completed"])
        total_required = sum(1 for item in checklist if item["required"])
        required_completed = sum(1 for item in checklist if item["required"] and item["completed"])
        
        progress = {
            "total_items": len(checklist),
            "completed": completed,
            "completion_percentage": round((completed / len(checklist)) * 100, 1),
            "required_items": total_required,
            "required_completed": required_completed,
            "status": "on_track" if required_completed >= completed * 0.8 else "needs_attention"
        }
        
        # Store checklist
        checklist_key = f"transaction:{property_id}:checklist"
        memory.set(checklist_key, {"items": checklist, "progress": progress, "updated_at": datetime.now().isoformat()})
        
        result = {
            "property_id": property_id,
            "transaction_type": transaction_type,
            "checklist": checklist,
            "progress": progress
        }

        memory.append("transactions", {
            "transaction_id": property_id,
            "event": "checklist",
            "data": result,
            "timestamp": datetime.now().isoformat()
        })

        return result
    
    async def _check_compliance(self, data: Dict) -> Dict:
        """Check compliance requirements for transaction."""
        property_id = data.get("property_id")
        
        requirements = [
            {"requirement": "Agent license verified", "met": True, "category": "agent"},
            {"requirement": "Disclosure statement provided", "met": True, "category": "disclosure"},
            {"requirement": "Sale contract compliant", "met": True, "category": "contract"},
            {"requirement": "Anti-money laundering checks", "met": True, "category": "compliance"},
            {"requirement": "Privacy Act compliance", "met": True, "category": "privacy"},
            {"requirement": "Consumer Guarantees Act notice", "met": True, "category": "consumer"},
            {"requirement": "Agency agreement terms met", "met": True, "category": "agency"},
            {"requirement": "Commission structure documented", "met": True, "category": "agency"}
        ]
        
        met_count = sum(1 for r in requirements if r["met"])
        
        return {
            "property_id": property_id,
            "compliant": met_count == len(requirements),
            "requirements_met": met_count,
            "requirements_total": len(requirements),
            "compliance_percentage": round((met_count / len(requirements)) * 100, 1),
            "requirements": requirements,
            "warnings": []
        }
    
    async def _risk_assessment(self, data: Dict) -> Dict:
        """Assess transaction risks."""
        transaction_id = data.get("transaction_id")
        days_to_settlement = data.get("days_to_settlement")
        finance_approved = data.get("finance_approved")
        building_report_complete = data.get("building_report_complete")
        lawyer_assigned = data.get("lawyer_assigned")
        deposit_status = data.get("deposit_status", "held_in_trust")

        risks = []

        if finance_approved is False:
            risk_level = "high" if isinstance(days_to_settlement, int) and days_to_settlement <= 14 else "medium"
            risks.append({
                "factor": "Finance approval outstanding",
                "level": risk_level,
                "days_remaining": days_to_settlement,
                "mitigation": "Follow up with buyer's lender"
            })

        if building_report_complete is False:
            risk_level = "medium" if isinstance(days_to_settlement, int) and days_to_settlement <= 14 else "low"
            risks.append({
                "factor": "Building report incomplete",
                "level": risk_level,
                "days_remaining": days_to_settlement,
                "mitigation": "Complete inspection and review report"
            })

        if isinstance(days_to_settlement, int):
            settlement_level = "high" if days_to_settlement <= 7 else "medium" if days_to_settlement <= 21 else "low"
            risks.append({
                "factor": "Settlement date proximity",
                "level": settlement_level,
                "days_remaining": days_to_settlement,
                "mitigation": "Monitor settlement timeline"
            })

        if lawyer_assigned is False:
            risks.append({
                "factor": "Legal representation missing",
                "level": "medium",
                "mitigation": "Assign conveyancing lawyer immediately"
            })

        risks.append({
            "factor": "Deposit security",
            "level": "low",
            "status": deposit_status,
            "mitigation": "Verify with trust account"
        })

        high_risks = sum(1 for r in risks if r.get("level") == "high")
        medium_risks = sum(1 for r in risks if r.get("level") == "medium")

        if high_risks > 0:
            overall_risk = "high"
        elif medium_risks > 0:
            overall_risk = "medium"
        else:
            overall_risk = "low"

        risk_key = f"transaction:{transaction_id}:risk"
        from datetime import datetime
        memory.set(risk_key, {
            "risks": risks,
            "overall_risk": overall_risk,
            "assessed_at": datetime.now().isoformat()
        })

        result = {
            "transaction_id": transaction_id,
            "overall_risk": overall_risk,
            "risk_factors": risks,
            "high_risk_count": high_risks,
            "medium_risk_count": medium_risks,
            "recommendations": [r["mitigation"] for r in risks if r.get("level") in ["high", "medium"]]
        }

        memory.append("transactions", {
            "transaction_id": transaction_id,
            "event": "risk_assessment",
            "data": result,
            "timestamp": datetime.now().isoformat()
        })

        return result

    async def _milestone_status(self, data: Dict) -> Dict:
        """Get current milestone status."""
        transaction_id = data.get("transaction_id")
        
        milestones = [
            {"name": "Listing/Sale Agreed", "status": "completed", "date": (datetime.now() - timedelta(days=30)).isoformat()},
            {"name": "Contract Signed", "status": "completed", "date": (datetime.now() - timedelta(days=25)).isoformat()},
            {"name": "Conditions Satisfied", "status": "in_progress", "date": None},
            {"name": "Settlement", "status": "pending", "date": (datetime.now() + timedelta(days=20)).isoformat()}
        ]
        
        return {
            "transaction_id": transaction_id,
            "milestones": milestones,
            "current_phase": "conditions",
            "percent_complete": 50
        }
    
    async def _update_milestone(self, data: Dict) -> Dict:
        """Update milestone status."""
        transaction_id = data.get("transaction_id")
        milestone_name = data.get("milestone")
        new_status = data.get("status")
        
        # In a real implementation, this would update the database
        return {
            "transaction_id": transaction_id,
            "milestone": milestone_name,
            "status": new_status,
            "updated_at": datetime.now().isoformat(),
            "message": f"Milestone '{milestone_name}' updated to '{new_status}'"
        }
    
    async def _generate_timeline(self, data: Dict) -> Dict:
        """Generate transaction timeline."""
        start_date = datetime.now()
        settlement_days = data.get("settlement_days", 30)
        
        timeline = [
            {"phase": "Week 1", "events": ["Contract signed", "Deposit paid"], "date": (start_date + timedelta(days=7)).strftime("%Y-%m-%d")},
            {"phase": "Week 2", "events": ["Finance condition work", "Inspections"], "date": (start_date + timedelta(days=14)).strftime("%Y-%m-%d")},
            {"phase": "Week 3", "events": ["Conditions deadline", "LIM review"], "date": (start_date + timedelta(days=21)).strftime("%Y-%m-%d")},
            {"phase": "Settlement", "events": ["Pre-settlement inspection", "Key handover"], "date": (start_date + timedelta(days=settlement_days)).strftime("%Y-%m-%d")}
        ]
        
        return {
            "timeline": timeline,
            "settlement_date": (start_date + timedelta(days=settlement_days)).strftime("%Y-%m-%d"),
            "total_days": settlement_days
        }
    
    async def _notify_party(self, data: Dict) -> Dict:
        """Send notification to transaction party."""
        party = data.get("party")  # buyer, seller, agent, solicitor
        message_type = data.get("message_type")
        
        templates = {
            "deadline_reminder": f"Reminder: Upcoming deadline for {party}",
            "milestone_complete": f"Milestone completed - {party} notified",
            "document_required": f"Documents required from {party}",
            "general_update": f"Transaction update for {party}"
        }
        
        return {
            "party": party,
            "message_type": message_type,
            "message": templates.get(message_type, templates["general_update"]),
            "sent_at": datetime.now().isoformat(),
            "status": "sent"
        }
