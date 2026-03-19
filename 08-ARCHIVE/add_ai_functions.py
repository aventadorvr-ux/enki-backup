#!/usr/bin/env python3
"""Add missing AI service functions to ai_service.py"""

new_functions = '''
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
'''

# Read current file
with open("/home/ubuntu/nz-realestate-ai/app/core/ai_service.py", "r") as f:
    content = f.read()

# Find the line "ai_service = AIService()" and insert the functions before it
marker = "ai_service = AIService()"
if marker in content:
    content = content.replace(marker, new_functions + marker)
else:
    # Append at end if marker not found
    content = content.rstrip() + "\n" + new_functions + "\n" + marker + "\n"

# Write back
with open("/home/ubuntu/nz-realestate-ai/app/core/ai_service.py", "w") as f:
    f.write(content)

print("AI service functions added successfully!")
