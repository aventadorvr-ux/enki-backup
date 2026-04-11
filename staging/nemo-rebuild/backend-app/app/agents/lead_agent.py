from typing import Any, Dict, List
from datetime import datetime
from app.agents.base import BaseAgent
from app.core.ai_service import ai_service
from app.core.memory import memory

class LeadAgent(BaseAgent):
    """Enhanced Lead Agent with AI-powered qualification, sentiment analysis, and conversation memory."""
    
    def __init__(self):
        super().__init__("lead")
        self.system_prompt = """You are a professional real estate assistant for a New Zealand real estate agency. 
You help qualify leads, answer questions, and guide potential buyers and sellers.
Be helpful, professional, and knowledgeable about the NZ property market.
Always aim to move the conversation forward toward a consultation or property viewing."""
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action")
        data = task.get("data", {})
        
        if action == "qualify":
            return await self._qualify(data)
        elif action == "qualify_ai":
            return await self._qualify_ai(data)
        elif action == "respond":
            return await self._respond(data)
        elif action == "route":
            return await self._route(data)
        elif action == "chat":
            return await self._chat(data)
        elif action == "analyze_sentiment":
            return await self._analyze_sentiment(data)
        elif action == "analyze_conversation":
            return await self._analyze_conversation(data)
        elif action == "get_follow_up_recommendations":
            return await self._get_follow_up(data)
        elif action == "get_conversation_history":
            return await self._get_history(data)
        
        return {"error": "Unknown action"}
    
    async def _qualify(self, data: Dict) -> Dict:
        """Basic rule-based lead qualification."""
        score = 0
        if data.get("budget", 0) > 500000: score += 30
        if data.get("timeline") in ["immediate", "1-3 months"]: score += 40
        if data.get("pre_approved"): score += 20
        if data.get("contact_method"): score += 10
        
        result = {
            "qualified": score >= 60,
            "score": score,
            "priority": "high" if score >= 80 else "medium" if score >= 60 else "low"
        }

        memory.append("leads", {
            "lead_id": data.get("lead_id", "unknown"),
            "event": "qualify",
            "data": result,
            "timestamp": datetime.now().isoformat()
        })

        return result
    
    async def _qualify_ai(self, data: Dict) -> Dict:
        """AI-powered lead qualification with persona detection."""
        # Get conversation history if available
        lead_id = data.get("lead_id", "unknown")
        history_key = f"lead:{lead_id}:conversations"
        conversation_history = memory.get(history_key) or []
        
        result = ai_service.qualify_lead_intelligent(
            budget=data.get("budget", 0),
            timeline=data.get("timeline", ""),
            pre_approved=data.get("pre_approved", False),
            notes=data.get("notes", ""),
            interaction_history=conversation_history
        )
        
        # Store qualification result
        qual_key = f"lead:{lead_id}:qualification"
        memory.set(qual_key, {
            **result,
            "qualified_at": datetime.now().isoformat()
        })
        
        return {
            "ai_analysis": result,
            "method": "openrouter_enhanced",
            "lead_id": lead_id
        }
    
    async def _respond(self, data: Dict) -> Dict:
        """Generate contextual response based on inquiry type."""
        inquiry_type = data.get("type", "general")
        lead_id = data.get("lead_id", "unknown")
        
        # Check if we have previous context
        history_key = f"lead:{lead_id}:conversations"
        history = memory.get(history_key) or []
        
        templates = {
            "viewing": {
                "response": "Thanks for your interest in viewing this property! I'll check availability and get back to you within 2 hours.",
                "next_step": "Schedule viewing",
                "priority": "high"
            },
            "valuation": {
                "response": "Thank you for requesting a property valuation. One of our agents will contact you within 24 hours to arrange a convenient time.",
                "next_step": "Schedule valuation",
                "priority": "high"
            },
            "selling": {
                "response": "Thinking of selling? Great timing! We'd love to help you achieve the best possible price. Let's discuss your property and the current market conditions.",
                "next_step": "Listing consultation",
                "priority": "high"
            },
            "buying": {
                "response": "Exciting times! Finding the right home is a journey. Let me understand your needs better so we can find properties that match your criteria.",
                "next_step": "Buyer consultation",
                "priority": "medium"
            },
            "general": {
                "response": "Thanks for contacting us! How can we help you with your real estate needs today?",
                "next_step": "Gather requirements",
                "priority": "medium"
            }
        }
        
        response_data = templates.get(inquiry_type, templates["general"])
        
        # If we have history, personalize the response
        if len(history) > 0:
            last_interaction = history[-1]
            response_data["context"] = "Personalized based on previous interaction"
        
        result = {
            "response": response_data["response"],
            "type": inquiry_type,
            "next_step": response_data["next_step"],
            "priority": response_data["priority"],
            "lead_id": lead_id
        }

        memory.append("leads", {
            "lead_id": lead_id,
            "event": "respond",
            "data": result,
            "timestamp": datetime.now().isoformat()
        })

        return result
    
    async def _chat(self, data: Dict) -> Dict:
        """Handle conversational interaction with memory."""
        lead_id = data.get("lead_id", f"anonymous_{datetime.now().timestamp()}")
        message = data.get("message", "")
        
        # Get or create conversation history
        history_key = f"lead:{lead_id}:conversations"
        
        # Use AI service with memory
        response = ai_service.chat_with_memory(
            session_id=lead_id,
            message=message,
            system_prompt=self.system_prompt
        )
        
        # Also store in our memory system for cross-session persistence
        history = memory.get(history_key) or []
        history.append({
            "user": message,
            "assistant": response,
            "timestamp": datetime.now().isoformat()
        })
        memory.set(history_key, history)
        
        # Analyze sentiment of the message
        sentiment = ai_service.analyze_sentiment(message)
        
        return {
            "response": response,
            "lead_id": lead_id,
            "sentiment": sentiment,
            "conversation_length": len(history)
        }
    
    async def _analyze_sentiment(self, data: Dict) -> Dict:
        """Analyze sentiment of lead communication."""
        text = data.get("text", "")
        lead_id = data.get("lead_id")
        
        sentiment = ai_service.analyze_sentiment(text)
        
        # Store sentiment analysis
        if lead_id:
            sentiment_key = f"lead:{lead_id}:sentiment_history"
            history = memory.get(sentiment_key) or []
            history.append({
                "text_preview": text[:100],
                "sentiment": sentiment,
                "timestamp": datetime.now().isoformat()
            })
            memory.set(sentiment_key, history)
        
        result = {
            "sentiment_analysis": sentiment,
            "lead_id": lead_id,
            "recommended_action": self._get_action_from_sentiment(sentiment)
        }

        memory.append("leads", {
            "lead_id": lead_id,
            "event": "sentiment",
            "data": result,
            "timestamp": datetime.now().isoformat()
        })

        return result
    
    def _get_action_from_sentiment(self, sentiment: Dict) -> str:
        """Determine next action based on sentiment."""
        if sentiment["sentiment"] == "positive" and sentiment["urgency"] == "high":
            return "Contact immediately - hot lead showing strong interest"
        elif sentiment["sentiment"] == "positive":
            return "Follow up within 24 hours with relevant listings"
        elif sentiment["urgency"] == "high":
            return "Address concerns urgently - may be at risk"
        elif sentiment["sentiment"] == "negative":
            return "Handle with care - schedule call to address concerns"
        else:
            return "Continue nurturing with regular content"
    
    async def _analyze_conversation(self, data: Dict) -> Dict:
        """Analyze full conversation to determine intent and next steps."""
        lead_id = data.get("lead_id")
        
        if not lead_id:
            return {"error": "lead_id required"}
        
        history_key = f"lead:{lead_id}:conversations"
        history = memory.get(history_key) or []
        
        if len(history) < 2:
            return {
                "lead_id": lead_id,
                "message": "Not enough conversation history for analysis",
                "conversation_count": len(history)
            }
        
        # Extract all messages
        messages = []
        for h in history:
            messages.append(h.get("user", ""))
        
        intent_analysis = ai_service.analyze_conversation_intent(messages)
        
        # Store analysis
        analysis_key = f"lead:{lead_id}:intent_analysis"
        memory.set(analysis_key, {
            **intent_analysis,
            "analyzed_at": datetime.now().isoformat()
        })
        
        return {
            "lead_id": lead_id,
            "intent_analysis": intent_analysis,
            "conversation_count": len(history)
        }
    
    async def _get_follow_up(self, data: Dict) -> Dict:
        """Get AI-powered follow-up recommendations."""
        lead_id = data.get("lead_id")
        
        if not lead_id:
            return {"error": "lead_id required"}
        
        # Gather all available data
        qual_key = f"lead:{lead_id}:qualification"
        sentiment_key = f"lead:{lead_id}:sentiment_history"
        history_key = f"lead:{lead_id}:conversations"
        
        qualification = memory.get(qual_key) or {}
        sentiment_history = memory.get(sentiment_key) or []
        conversations = memory.get(history_key) or []
        
        # Generate recommendations based on collected data
        recommendations = {
            "lead_id": lead_id,
            "generated_at": datetime.now().isoformat(),
            "follow_up_sequence": [],
            "best_contact_method": self._determine_contact_method(conversations),
            "optimal_timing": self._determine_timing(sentiment_history),
            "messaging_strategy": self._get_messaging_strategy(qualification, sentiment_history)
        }
        
        # Build follow-up sequence
        if qualification.get("hot_lead") == "Yes":
            recommendations["follow_up_sequence"] = [
                {"day": 0, "action": "Call within 2 hours", "channel": "phone"},
                {"day": 1, "action": "Send personalized property list", "channel": "email"},
                {"day": 2, "action": "Follow-up call", "channel": "phone"}
            ]
        elif qualification.get("priority") == "High":
            recommendations["follow_up_sequence"] = [
                {"day": 0, "action": "Send welcome email", "channel": "email"},
                {"day": 1, "action": "Call to discuss requirements", "channel": "phone"},
                {"day": 3, "action": "Send relevant listings", "channel": "email"}
            ]
        else:
            recommendations["follow_up_sequence"] = [
                {"day": 0, "action": "Send welcome email", "channel": "email"},
                {"day": 7, "action": "Market update email", "channel": "email"},
                {"day": 14, "action": "Check-in call", "channel": "phone"}
            ]
        
        return recommendations
    
    def _determine_contact_method(self, conversations: List[Dict]) -> str:
        """Determine best contact method based on history."""
        if not conversations:
            return "email"
        # Simple heuristic - could be enhanced
        return "phone" if len(conversations) > 3 else "email"
    
    def _determine_timing(self, sentiment_history: List[Dict]) -> str:
        """Determine optimal contact timing."""
        if not sentiment_history:
            return "business_hours"
        
        # Look at most recent sentiment
        latest = sentiment_history[-1] if sentiment_history else None
        if latest and latest.get("sentiment", {}).get("urgency") == "high":
            return "immediate"
        return "business_hours"
    
    def _get_messaging_strategy(self, qualification: Dict, sentiment_history: List[Dict]) -> Dict:
        """Determine messaging strategy."""
        persona = qualification.get("persona", "General")
        
        strategies = {
            "First-time buyer": {
                "tone": "educational and supportive",
                "focus": "process guidance and affordability",
                "content_type": "buying guides and market education"
            },
            "Investor": {
                "tone": "data-driven and analytical",
                "focus": "ROI and rental yields",
                "content_type": "market reports and investment analysis"
            },
            "Luxury": {
                "tone": "exclusive and sophisticated",
                "focus": "lifestyle and prestige",
                "content_type": "premium listings and off-market opportunities"
            },
            "Upgrader": {
                "tone": "excited and opportunity-focused",
                "focus": "space and features",
                "content_type": "family homes and neighborhood highlights"
            }
        }
        
        return strategies.get(persona, {
            "tone": "professional and helpful",
            "focus": "properties matching criteria",
            "content_type": "general listings"
        })
    
    async def _get_history(self, data: Dict) -> Dict:
        """Retrieve conversation history for a lead."""
        lead_id = data.get("lead_id")
        if not lead_id:
            return {"error": "lead_id required"}
        
        history_key = f"lead:{lead_id}:conversations"
        conversations = memory.get(history_key) or []
        
        return {
            "lead_id": lead_id,
            "conversation_count": len(conversations),
            "history": conversations
        }
    
    async def _route(self, data: Dict) -> Dict:
        """Smart lead routing based on qualification and agent expertise."""
        lead_id = data.get("lead_id")
        
        # Get qualification data if available
        qual_key = f"lead:{lead_id}:qualification"
        qualification = memory.get(qual_key) or {}
        
        available_agents = data.get("available_agents", [
            {"name": "Default Agent", "id": "agent_001", "specialties": ["general"]}
        ])
        
        # Simple routing logic based on persona
        persona = qualification.get("persona", "General")
        
        # Find best matching agent
        assigned_agent = available_agents[0]
        for agent in available_agents:
            specialties = agent.get("specialties", [])
            if persona.lower() in [s.lower() for s in specialties]:
                assigned_agent = agent
                break
        
        routing_reason = f"Matched {persona} lead with {assigned_agent.get('name')}"
        
        return {
            "assigned_agent": assigned_agent,
            "routing_reason": routing_reason,
            "lead_id": lead_id,
            "priority": qualification.get("priority", "medium")
        }
