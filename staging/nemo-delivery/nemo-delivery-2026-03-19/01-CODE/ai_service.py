import os
import requests
import json
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class AIService:
    """Enhanced OpenRouter AI service with advanced capabilities and intelligent fallbacks."""
    
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
        
        # Enhanced fallback sentiment analysis
        return self._fallback_sentiment_analysis(text)
    
    def _fallback_sentiment_analysis(self, text: str) -> Dict:
        """Rule-based sentiment analysis as fallback."""
        text_lower = text.lower()
        
        # Positive indicators
        positive_words = ['love', 'great', 'excellent', 'amazing', 'perfect', 'interested', 
                         'excited', 'beautiful', 'wonderful', 'fantastic', 'ready', 'keen',
                         'definitely', 'absolutely', 'please', 'thank', 'happy', 'ideal']
        
        # Negative indicators
        negative_words = ['bad', 'terrible', 'awful', 'disappointed', 'problem', 'issue',
                         'concerned', 'worried', 'expensive', 'overpriced', 'not', "don't",
                         "won't", "can't", 'delay', 'cancel']
        
        # Urgency indicators
        urgent_words = ['asap', 'urgent', 'immediately', 'today', 'tomorrow', 'now',
                       'quickly', 'hurry', 'deadline', 'limited', 'rush']
        
        # Intent indicators
        buying_words = ['buy', 'purchase', 'offer', 'bid', 'mortgage', 'deposit', 'finance']
        selling_words = ['sell', 'listing', 'agent', 'valuation', 'appraisal', 'market value']
        
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        urg_count = sum(1 for w in urgent_words if w in text_lower)
        
        # Determine sentiment
        if pos_count > neg_count:
            sentiment = "positive"
            score = min(0.5 + (pos_count * 0.1), 0.95)
        elif neg_count > pos_count:
            sentiment = "negative"
            score = max(0.5 - (neg_count * 0.1), 0.1)
        else:
            sentiment = "neutral"
            score = 0.5
        
        # Determine urgency
        if urg_count >= 2 or 'asap' in text_lower or 'urgent' in text_lower:
            urgency = "high"
        elif urg_count == 1:
            urgency = "medium"
        else:
            urgency = "low"
        
        # Determine intent
        if any(w in text_lower for w in buying_words):
            intent = "buying"
        elif any(w in text_lower for w in selling_words):
            intent = "selling"
        else:
            intent = "general"
        
        # Extract keywords (simple approach)
        words = text_lower.split()
        keywords = list(set([w for w in words if len(w) > 4][:5]))
        
        return {
            "sentiment": sentiment,
            "score": round(score, 2),
            "urgency": urgency,
            "intent": intent,
            "keywords": keywords,
            "method": "rule_based_fallback"
        }

    def generate_property_description(self, bedrooms: int, bathrooms: int, location: str,
                                     features: list = None, tone: str = "professional") -> str:
        """Generate compelling property description using AI with intelligent fallback."""
        features = features or []
        
        # Try AI first
        result = self._generate_ai_description(bedrooms, bathrooms, location, features, tone)
        if result and len(result.split()) > 50:  # Ensure substantial content
            return result
        
        # Fallback to enhanced template
        return self._generate_enhanced_description(bedrooms, bathrooms, location, features, tone)
    
    def _generate_ai_description(self, bedrooms, bathrooms, location, features, tone):
        """Attempt AI generation."""
        features_text = ", ".join(features) if features else "modern features"
        
        prompt = f"""Write a compelling {tone} property description for a real estate listing:

Property Details:
- {bedrooms} bedrooms, {bathrooms} bathrooms
- Location: {location}
- Features: {features_text}

Requirements:
- 100-150 words
- Engaging and persuasive
- Highlight location benefits
- Emphasize unique features
- End with a call to action

Description:"""
        
        return self.generate(prompt, max_tokens=350, temperature=0.7)
    
    def _generate_enhanced_description(self, bedrooms, bathrooms, location, features, tone) -> str:
        """Generate sophisticated description using templates and vocabulary banks."""
        vocab = self.tone_vocabulary.get(tone, self.tone_vocabulary["professional"])
        location_lower = location.lower()
        
        # Get location insight
        location_desc = "a sought-after location"
        for suburb, desc in self.location_insights.items():
            if suburb in location_lower:
                location_desc = desc
                break
        
        # Build description components
        opener = random.choice(vocab["openers"])
        adj1 = random.choice(vocab["adjectives"])
        adj2 = random.choice([a for a in vocab["adjectives"] if a != adj1])
        verb = random.choice(vocab["verbs"])
        closing = random.choice(vocab["closings"])
        
        # Format features
        feature_sentences = []
        if features:
            if len(features) >= 1:
                feature_sentences.append(f"The {features[0]} provides both style and functionality.")
            if len(features) >= 2:
                feature_sentences.append(f"Additional highlights include {features[1]}.")
            if len(features) >= 3:
                feature_sentences.append(f"The property also boasts {features[2]}.")
        
        feature_text = " ".join(feature_sentences)
        
        # Construct description
        bedroom_word = "bedroom" if bedrooms == 1 else "bedrooms"
        bathroom_word = "bathroom" if bathrooms == 1 else "bathrooms"
        
        description = f"""{opener} {bedrooms}-{bedroom_word}, {bathrooms}-{bathroom_word} residence in {location} {verb} {adj1} living in {location_desc}.

This {adj2} home {verb} generous accommodation perfect for modern living. {feature_text}

Situated in {location_desc.split(' known')[0] if ' known' in location_desc else location_desc}, this property provides easy access to local amenities, schools, and transport links. The thoughtful layout maximizes space and natural light throughout.

{closing}. Contact us today to arrange a viewing and make this exceptional property yours."""
        
        return description
    
    def generate_social_post(self, platform: str, bedrooms: int, location: str,
                            price: str = "", features: list = None,
                            include_cta: bool = True) -> str:
        """Generate platform-optimized social media post with enhanced fallback."""
        features = features or []
        
        # Try AI first
        features_text = ", ".join(features[:3]) if features else "great features"
        price_text = f" | {price}" if price else ""
        
        platform_guidance = {
            "facebook": "Engaging, emoji-friendly, community-focused",
            "instagram": "Visual, trendy hashtags, aspirational",
            "linkedin": "Professional, market insights, investment angle",
            "twitter": "Concise, punchy, under 280 characters"
        }
        
        cta = " Include a compelling call-to-action." if include_cta else ""
        
        prompt = f"""Write a {platform} post for this property:
- {bedrooms} bed in {location}{price_text}
- Features: {features_text}
Style: {platform_guidance.get(platform, 'Engaging')}
{cta}

Post:"""
        
        result = self.generate(prompt, max_tokens=200, temperature=0.8)
        if result:
            return result
        
        # Enhanced fallback templates
        return self._generate_template_social_post(platform, bedrooms, location, price, features, include_cta)
    
    def _generate_template_social_post(self, platform, bedrooms, location, price, features, include_cta) -> str:
        """Generate platform-specific posts using enhanced templates."""
        bedroom_word = "bed" if bedrooms == 1 else "beds"
        feature = features[0] if features else "amazing features"
        price_display = f" 💰 {price}" if price else ""
        
        ctas = {
            "facebook": "🏡 Open home this weekend - don't miss out!",
            "instagram": "✨ DM for private viewing",
            "linkedin": "📊 Contact us for investment analysis",
            "twitter": "🏠 Viewing this weekend!"
        }
        
        posts = {
            "facebook": f"🏡 JUST LISTED! {bedrooms} {bedroom_word} in {location}{price_display}\n\n✨ {feature}\n📍 Prime location\n🌟 Move-in ready\n\n{ctas['facebook'] if include_cta else ''}\n\n#NZRealEstate #Property #AucklandHomes",
            "instagram": f"✨ {bedrooms} {bedroom_word} • {location}{price_display}\n\n{feature}\nPrime location 📍\nYour dream home awaits 🏠\n\n{ctas['instagram'] if include_cta else ''}\n\n#NZRealEstate #Property #HomeGoals #InteriorDesign",
            "linkedin": f"New Listing: {bedrooms}-{bedroom_word} property in {location}{price_display}\n\nThis well-presented home offers:\n• {feature}\n• Prime location\n• Strong investment potential\n\n{ctas['linkedin'] if include_cta else ''}\n\n#RealEstate #Investment #PropertyMarket",
            "twitter": f"NEW: {bedrooms} {bedroom_word} {location}{price_display} | {feature} | {ctas['twitter'] if include_cta else 'Available now!'} #NZRealEstate"
        }
        
        return posts.get(platform, posts["facebook"])
    
    def qualify_lead_intelligent(self, budget: float, timeline: str, pre_approved: bool,
                                  notes: str = "", interaction_history: list = None) -> dict:
        """AI-powered lead qualification with enhanced rule-based fallback."""
        # Try AI first
        ai_result = self._ai_qualify_lead(budget, timeline, pre_approved, notes, interaction_history)
        if ai_result and ai_result.get("score", 0) != 50:  # Not default
            return ai_result
        
        # Use enhanced rule-based scoring
        return self._enhanced_rule_qualify(budget, timeline, pre_approved, notes, interaction_history)
    
    def _ai_qualify_lead(self, budget, timeline, pre_approved, notes, interaction_history):
        """Attempt AI qualification."""
        history_text = f"Previous interactions: {len(interaction_history)}" if interaction_history else ""
        
        prompt = f"""Analyze this real estate lead and respond in JSON format:

Lead Information:
- Budget: ${budget:,.0f}
- Timeline: {timeline}
- Pre-approved: {"Yes" if pre_approved else "No"}
- Notes: {notes}
{history_text}

Score based on:
1. Budget strength (Auckland median ~$1M)
2. Timeline urgency
3. Finance readiness
4. Intent signals from notes
5. Engagement level

Respond ONLY with valid JSON:
{{
    "qualified": true/false,
    "score": 0-100,
    "priority": "high/medium/low",
    "persona": "First-time buyer/Investor/Luxury/Upgrader/General",
    "hot_lead": "Yes/Maybe/No",
    "reasoning": "explanation",
    "next_actions": ["action1", "action2"]
}}"""
        
        result = self.generate(prompt, max_tokens=400, temperature=0.3)
        if result:
            try:
                json_str = result.strip()
                if "```json" in json_str:
                    json_str = json_str.split("```json")[1].split("```")[0]
                elif "```" in json_str:
                    json_str = json_str.split("```")[1].split("```")[0]
                parsed = json.loads(json_str.strip())
                parsed["method"] = "ai_analysis"
                return parsed
            except Exception:
                pass
        return None
    
    def _enhanced_rule_qualify(self, budget, timeline, pre_approved, notes, interaction_history) -> dict:
        """Enhanced rule-based lead qualification with persona detection."""
        notes_lower = (notes or "").lower()
        score = 0
        signals = []
        
        # Budget scoring (relative to Auckland market)
        if budget >= 2000000:
            score += 35
            signals.append("luxury_budget")
        elif budget >= 1000000:
            score += 30
            signals.append("strong_budget")
        elif budget >= 700000:
            score += 20
            signals.append("good_budget")
        elif budget >= 500000:
            score += 10
            signals.append("moderate_budget")
        else:
            score += 5
        
        # Timeline scoring
        timeline_scores = {
            "immediate": 30,
            "1-3 months": 25,
            "3-6 months": 15,
            "6-12 months": 10,
            "just browsing": 5
        }
        timeline_score = timeline_scores.get(timeline.lower(), 10)
        score += timeline_score
        if timeline_score >= 25:
            signals.append("high_urgency")
        
        # Finance readiness
        if pre_approved:
            score += 20
            signals.append("pre_approved")
        elif any(w in notes_lower for w in ["cash", "cash buyer", "no mortgage"]):
            score += 25
            signals.append("cash_buyer")
        elif any(w in notes_lower for w in ["finance", "mortgage", "bank", "approval"]):
            score += 15
            signals.append("finance_ready")
        
        # Intent signals from notes
        intent_signals = {
            "investor": ["investment", "rental", "yield", "roi", "return", "cash flow"],
            "luxury": ["luxury", "prestige", "exclusive", "high-end", "premium"],
            "first_time": ["first home", "starter", "beginning", "getting into", "first time"],
            "upgrader": ["bigger", "upgrade", "growing family", "more space", "upsizing"],
            "downsizer": ["downsize", "smaller", "retirement", "empty nest", "single level"]
        }
        
        detected_persona = "General"
        for persona, keywords in intent_signals.items():
            if any(kw in notes_lower for kw in keywords):
                detected_persona = persona.replace("_", "-").title()
                if persona == "investor":
                    score += 10
                elif persona == "luxury":
                    score += 5
                signals.append(f"persona:{persona}")
                break
        
        # Engagement history bonus
        if interaction_history:
            engagement_count = len(interaction_history)
            if engagement_count >= 5:
                score += 15
                signals.append("highly_engaged")
            elif engagement_count >= 3:
                score += 10
                signals.append("moderately_engaged")
            elif engagement_count >= 1:
                score += 5
                signals.append("some_engagement")
        
        # Contact method preference bonus
        if any(w in notes_lower for w in ["call me", "phone", "mobile", "contact me"]):
            score += 5
            signals.append("wants_contact")
        
        # Cap score at 100
        score = min(score, 100)
        
        # Determine qualification
        qualified = score >= 60
        priority = "high" if score >= 80 else "medium" if score >= 60 else "low"
        hot_lead = "Yes" if score >= 80 else "Maybe" if score >= 65 else "No"
        
        # Generate reasoning
        reasoning_parts = []
        if "luxury_budget" in signals or "strong_budget" in signals:
            reasoning_parts.append(f"Strong budget position (${budget:,.0f})")
        if "high_urgency" in signals:
            reasoning_parts.append(f"Urgent timeline ({timeline})")
        if "pre_approved" in signals or "cash_buyer" in signals:
            reasoning_parts.append("Finance ready")
        if detected_persona != "General":
            reasoning_parts.append(f"{detected_persona} buyer profile")
        
        reasoning = "; ".join(reasoning_parts) if reasoning_parts else "Standard buyer inquiry"
        
        # Next actions
        next_actions = []
        if score >= 80:
            next_actions = ["Call within 2 hours", "Send premium listings", "Schedule viewing"]
        elif score >= 65:
            next_actions = ["Call within 24 hours", "Send relevant properties", "Email market report"]
        elif score >= 50:
            next_actions = ["Send welcome email", "Add to nurture campaign", "Follow up in 1 week"]
        else:
            next_actions = ["Add to database", "Send monthly newsletter", "Long-term nurture"]
        
        return {
            "qualified": qualified,
            "score": score,
            "priority": priority,
            "persona": detected_persona,
            "hot_lead": hot_lead,
            "reasoning": reasoning,
            "signals": signals,
            "next_actions": next_actions,
            "method": "enhanced_rule_based"
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