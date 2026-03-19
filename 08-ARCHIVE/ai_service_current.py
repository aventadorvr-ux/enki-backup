import os
import requests
import json
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class AIService:
    """Enhanced OpenRouter AI service with advanced capabilities."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.base_url = "https://openrouter.ai/api/v1"
        self.conversation_history = {}
        
        # NZ suburbs with characteristics for better descriptions
        self.location_insights = {
            "remuera": "prestigious suburb known for elegant homes and tree-lined streets",
            "ponsonby": "vibrant inner-city suburb with cafes, boutiques and Victorian villas",
            "grey lynn": "trendy neighborhood with artisan shops and strong community feel",
            "takapuna": "coastal gem with beach access and excellent dining",
            "devonport": "charming seaside village with heritage architecture",
            "herne bay": "exclusive waterfront suburb with stunning harbour views",
            "mission bay": "popular beachside suburb perfect for families",
            "epsom": "leafy suburb close to top schools and Cornwall Park",
            "auckland": "New Zealand's largest city with diverse neighborhoods",
            "wellington": "vibrant capital city with stunning harbor views",
            "christchurch": "Garden City with modern architecture and English heritage"
        }
        
        # Tone-specific vocabulary banks for enhanced descriptions
        self.tone_vocabulary = {
            "luxury": {
                "openers": ["An exquisite", "A magnificent", "An exceptional", "A prestigious", "An elegant"],
                "adjectives": ["stunning", "impeccable", "luxurious", "bespoke", "refined", "premium"],
                "verbs": ["indulge", "savor", "experience", "enjoy", "relish"],
                "closings": ["A rare opportunity", "Truly exceptional", "Unparalleled luxury"]
            },
            "professional": {
                "openers": ["A well-presented", "A quality", "An attractive", "A superb", "A desirable"],
                "adjectives": ["spacious", "modern", "well-maintained", "quality", "functional"],
                "verbs": ["offers", "provides", "features", "includes", "presents"],
                "closings": ["Priced to sell", "Great value", "Move-in ready"]
            },
            "friendly": {
                "openers": ["A lovely", "A charming", "A delightful", "A warm", "A cozy"],
                "adjectives": ["welcoming", "sunny", "bright", "comfortable", "inviting"],
                "verbs": ["welcomes", "offers", "has", "includes", "boasts"],
                "closings": ["Perfect for families", "Great first home", "Warm and inviting"]
            },
            "modern": {
                "openers": ["A sleek", "A contemporary", "A cutting-edge", "An architectural", "A designer"],
                "adjectives": ["minimalist", "stylish", "innovative", "sustainable", "smart"],
                "verbs": ["showcases", "delivers", "integrates", "combines", "features"],
                "closings": ["Architecturally designed", "Contemporary living", "Modern sophistication"]
            }
        }
        
    def generate(self, prompt: str, model: str = "anthropic/claude-3.5-sonnet", 
                 max_tokens: int = 500, temperature: float = 0.7,
                 system_prompt: str = None) -> Optional[str]:
        """Generate AI response using OpenRouter."""
        if not self.api_key:
            return None
            
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "https://nz-realestate-ai.com",
                    "X-Title": "NZ Real Estate AI",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenRouter error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"AI service error: {e}")
            return None
    
    def chat_with_memory(self, session_id: str, message: str, 
                         system_prompt: str = None, max_history: int = 10) -> str:
        """Chat with conversation memory for multi-turn dialogues."""
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        history = self.conversation_history[session_id]
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        for h in history[-max_history:]:
            messages.append({"role": "user", "content": h["user"]})
            messages.append({"role": "assistant", "content": h["assistant"]})
        
        messages.append({"role": "user", "content": message})
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "https://nz-realestate-ai.com",
                    "X-Title": "NZ Real Estate AI",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "anthropic/claude-3.5-sonnet",
                    "messages": messages,
                    "max_tokens": 500,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
                history.append({"user": message, "assistant": reply, "timestamp": datetime.now().isoformat()})
                return reply
            return "I'm sorry, I couldn't process that."
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return "I'm experiencing technical difficulties. Please try again."
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text for lead engagement."""
        prompt = f"""Analyze the sentiment of this text and respond in JSON format:

Text: "{text}"

Respond with ONLY valid JSON:
{{
    "sentiment": "positive|neutral|negative",
    "score": 0.0-1.0,
    "urgency": "high|medium|low",
    "intent": "buying|selling|inquiry|complaint|general",
    "keywords": ["keyword1", "keyword2"]
}}"""
        
        result = self.generate(prompt, max_tokens=200, temperature=0.3)
        if result:
            try:
                json_str = result.strip()
                if "```json" in json_str:
                    json_str = json_str.split("```json")[1].split("```")[0]
                elif "```" in json_str:
                    json_str = json_str.split("```")[1].split("```")[0]
                return json.loads(json_str.strip())
            except Exception:
                pass
        
        return {
            "sentiment": "neutral",
            "score": 0.5,
            "urgency": "medium",
            "intent": "general",
            "keywords": []
        }


    def generate_property_description(self, bedrooms: int, bathrooms: int, location: str,
                                     features: list = None, tone: str = "professional") -> str:
        """Generate compelling property description using AI."""
        features_text = ", ".join(features) if features else "modern features"
        
        prompt = f"""Write a compelling {tone} property description for a real estate listing:

Property Details:
- {bedrooms} bedrooms, {bathrooms} bathrooms
- Location: {location}
- Features: {features_text}

Write an engaging description (100-150 words)."""
        
        result = self.generate(prompt, max_tokens=300, temperature=0.7)
        return result or f"Beautiful {bedrooms}-bedroom home in {location} with {features_text}."
    
    def generate_social_post(self, platform: str, bedrooms: int, location: str,
                            price: str = "", features: list = None,
                            include_cta: bool = True) -> str:
        """Generate platform-optimized social media post."""
        features_text = ", ".join(features[:3]) if features else "amazing features"
        price_text = f" | {price}" if price else ""
        cta = " Include a call-to-action." if include_cta else ""
        
        prompt = f"""Write a {platform} post for a {bedrooms}-bedroom home in {location}{price_text}.
Highlight: {features_text}.{cta}"""
        
        result = self.generate(prompt, max_tokens=200, temperature=0.8)
        if not result:
            result = f"New listing! {bedrooms}-bedroom home in {location}{price_text}. Contact us to view!"
        return result
    
    def qualify_lead_intelligent(self, budget: float, timeline: str, pre_approved: bool,
                                  notes: str = "", interaction_history: list = None) -> dict:
        """AI-powered lead qualification with persona detection."""
        history_text = ""
        if interaction_history:
            history_text = f"Previous Interactions: {len(interaction_history)}"
        
        prompt = f"""Analyze this real estate lead:
- Budget: ${budget:,.0f}
- Timeline: {timeline}
- Pre-approved: {"Yes" if pre_approved else "No"}
- Notes: {notes}
{history_text}

Respond with JSON: qualified (bool), score (0-100), priority, persona, hot_lead, reasoning."""
        
        result = self.generate(prompt, max_tokens=300, temperature=0.3)
        
        if result:
            try:
                import json
                return json.loads(result.strip())
            except Exception:
                pass
        
        score = 30 if budget > 500000 else 0
        score += 40 if timeline in ["immediate", "1-3 months"] else 0
        score += 20 if pre_approved else 0
        
        return {
            "qualified": score >= 60,
            "score": score,
            "priority": "high" if score >= 80 else "medium" if score >= 60 else "low",
            "persona": "General",
            "hot_lead": "Yes" if score >= 80 else "Maybe",
            "reasoning": "Rule-based fallback"
        }
    
    def generate_email_campaign(self, campaign_type: str, target_audience: str,
                                 properties: list = None) -> dict:
        """Generate AI-powered email campaign content."""
        props_text = str(len(properties)) + " properties" if properties else ""
        
        prompt = f"""Create an email campaign:
Type: {campaign_type}
Audience: {target_audience}
Properties: {props_text}

Generate JSON with: subject, preview, body, cta, tone"""
        
        result = self.generate(prompt, max_tokens=400, temperature=0.7)
        
        if result:
            try:
                import json
                return json.loads(result.strip())
            except Exception:
                pass
        
        return {
            "subject": f"New {campaign_type} Properties",
            "preview": "Check out these properties!",
            "body": "We have new properties available. Contact us!",
            "cta": "View Properties",
            "tone": "professional"
        }
    
    def analyze_conversation_intent(self, messages: list) -> dict:
        """Analyze conversation messages to determine intent."""
        messages_text = " | ".join(messages[-3:]) if messages else ""
        
        prompt = f"""Analyze intent from: {messages_text}

Respond with JSON: primary_intent, confidence, property_interest, timeline_urgency."""
        
        result = self.generate(prompt, max_tokens=250, temperature=0.3)
        
        if result:
            try:
                import json
                return json.loads(result.strip())
            except Exception:
                pass
        
        return {
            "primary_intent": "general",
            "confidence": 0.5,
            "property_interest": "medium",
            "timeline_urgency": "unknown"
        }
ai_service = AIService()
