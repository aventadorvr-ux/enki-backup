from typing import Any, Dict, List
from datetime import datetime
from app.agents.base import BaseAgent
from app.core.ai_service import ai_service
from app.core.memory import memory

class ContentAgent(BaseAgent):
    """Enhanced Content Agent with SEO optimization, campaign management, and multi-platform support."""
    
    def __init__(self):
        super().__init__("content")
        self.tone_options = ["professional", "luxury", "friendly", "modern"]
        self.platforms = ["facebook", "instagram", "linkedin", "twitter"]
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action")
        data = task.get("data", {})
        
        if action == "description":
            return await self._description(data)
        elif action == "description_ai":
            return await self._description_ai(data)
        elif action == "social":
            return await self._social(data)
        elif action == "social_ai":
            return await self._social_ai(data)
        elif action == "social_multi_platform":
            return await self._social_multi_platform(data)
        elif action == "email":
            return await self._email(data)
        elif action == "email_campaign":
            return await self._email_campaign(data)
        elif action == "seo_optimize":
            return await self._seo_optimize(data)
        elif action == "generate_campaign":
            return await self._generate_full_campaign(data)
        elif action == "get_content_calendar":
            return await self._content_calendar(data)
        
        return {"error": "Unknown action"}
    
    async def _description(self, data: Dict) -> Dict:
        """Basic property description generation."""
        loc = data.get("location", "")
        beds = data.get("bedrooms", 0)
        desc = f"Stunning {beds}-bedroom home in {loc}. Modern living with premium finishes."
        return {
            "description": desc,
            "word_count": len(desc.split()),
            "method": "template"
        }
    
    async def _description_ai(self, data: Dict) -> Dict:
        """AI-powered property description with tone control."""
        desc = ai_service.generate_property_description(
            bedrooms=data.get("bedrooms", 3),
            bathrooms=data.get("bathrooms", 2),
            location=data.get("location", "Auckland"),
            features=data.get("features", []),
            tone=data.get("tone", "professional")
        )
        
        # Store for campaign tracking
        property_id = data.get("property_id", f"prop_{datetime.now().timestamp()}")
        content_key = f"content:{property_id}:descriptions"
        descriptions = memory.get(content_key) or []
        descriptions.append({
            "description": desc,
            "tone": data.get("tone", "professional"),
            "generated_at": datetime.now().isoformat()
        })
        memory.set(content_key, descriptions)
        
        desc = desc.replace("-bedrooms", "-bedroom").replace("-bathrooms", "-bathroom")

        return {
            "description": desc,
            "word_count": len(desc.split()),
            "ai_generated": True,
            "tone": data.get("tone", "professional"),
            "property_id": property_id
        }
    
    async def _social(self, data: Dict) -> Dict:
        """Basic social post generation."""
        platform = data.get("platform", "facebook")
        listing = data.get("listing", {})
        posts = {
            "facebook": f"New listing! {listing.get('bedrooms', 3)} bed in {listing.get('location', '')}. Contact us for details!",
            "instagram": f"🏡 {listing.get('bedrooms', 3)} bed | {listing.get('location', '')} | DM for details #NZRealEstate",
            "linkedin": f"New property listing: {listing.get('bedrooms', 3)} bedroom home in {listing.get('location', '')}. Professional real estate services.",
            "twitter": f"New! {listing.get('bedrooms', 3)} bed {listing.get('location', '')} 🏡 #Auckland #RealEstate"
        }
        return {
            "post": posts.get(platform, posts["facebook"]),
            "platform": platform,
            "method": "template"
        }
    
    async def _social_ai(self, data: Dict) -> Dict:
        """AI-powered social post optimized for platform."""
        post = ai_service.generate_social_post(
            platform=data.get("platform", "facebook"),
            bedrooms=data.get("bedrooms", 3),
            location=data.get("location", "Auckland"),
            price=data.get("price", ""),
            features=data.get("features", []),
            include_cta=data.get("include_cta", True)
        )
        
        # Track social content
        campaign_id = data.get("campaign_id", f"camp_{datetime.now().timestamp()}")
        content_key = f"content:{campaign_id}:social"
        posts = memory.get(content_key) or []
        posts.append({
            "platform": data.get("platform", "facebook"),
            "post": post,
            "generated_at": datetime.now().isoformat()
        })
        memory.set(content_key, posts)
        
        return {
            "post": post,
            "platform": data.get("platform", "facebook"),
            "ai_generated": True,
            "campaign_id": campaign_id
        }
    
    async def _social_multi_platform(self, data: Dict) -> Dict:
        """Generate optimized posts for multiple platforms at once."""
        platforms = data.get("platforms", ["facebook", "instagram", "linkedin"])
        property_data = {
            "bedrooms": data.get("bedrooms", 3),
            "location": data.get("location", "Auckland"),
            "price": data.get("price", ""),
            "features": data.get("features", [])
        }
        
        posts = {}
        for platform in platforms:
            post = ai_service.generate_social_post(
                platform=platform,
                **property_data
            )
            posts[platform] = post
        
        # Store campaign
        campaign_id = data.get("campaign_id", f"multi_{datetime.now().timestamp()}")
        memory.set(f"content:{campaign_id}:multi_platform", {
            "posts": posts,
            "property": property_data,
            "created_at": datetime.now().isoformat()
        })
        
        return {
            "campaign_id": campaign_id,
            "platforms": platforms,
            "posts": posts,
            "status": "generated"
        }
    
    async def _email(self, data: Dict) -> Dict:
        """Basic email template."""
        email_type = data.get("type", "general")
        
        templates = {
            "welcome": {
                "subject": "Welcome to NZ Real Estate AI",
                "body": "Thank you for joining us! We'll help you find your perfect property."
            },
            "market_update": {
                "subject": "Your Weekly Market Update",
                "body": "Here are the latest market trends and new listings in your area."
            },
            "viewing_confirmation": {
                "subject": "Viewing Confirmed",
                "body": "Your property viewing has been confirmed. We look forward to seeing you!"
            },
            "general": {
                "subject": "Market Updates",
                "body": "Latest market insights and property opportunities."
            }
        }
        
        template = templates.get(email_type, templates["general"])
        return {
            "subject": template["subject"],
            "body": template["body"],
            "type": email_type
        }
    
    async def _email_campaign(self, data: Dict) -> Dict:
        """AI-powered email campaign generation."""
        campaign_type = data.get("campaign_type", "new_listings")
        target_audience = data.get("target_audience", "buyers")
        properties = data.get("properties", [])
        
        campaign = ai_service.generate_email_campaign(
            campaign_type=campaign_type,
            target_audience=target_audience,
            properties=properties
        )
        
        # Store campaign
        campaign_id = data.get("campaign_id", f"email_{datetime.now().timestamp()}")
        memory.set(f"content:{campaign_id}:email_campaign", {
            **campaign,
            "campaign_type": campaign_type,
            "target_audience": target_audience,
            "created_at": datetime.now().isoformat()
        })
        
        return {
            "campaign_id": campaign_id,
            "email": campaign,
            "ai_generated": True
        }
    
    async def _seo_optimize(self, data: Dict) -> Dict:
        """SEO optimization for property descriptions."""
        content = data.get("content", "")
        target_keywords = data.get("keywords", [])
        
        # Analyze and suggest improvements
        word_count = len(content.split())
        
        suggestions = []
        if word_count < 100:
            suggestions.append("Add more descriptive content (aim for 150-200 words)")
        if word_count > 300:
            suggestions.append("Consider shortening for better readability")
        
        # Check keyword density
        content_lower = content.lower()
        keyword_analysis = {}
        for keyword in target_keywords:
            count = content_lower.count(keyword.lower())
            density = (count / word_count) * 100 if word_count > 0 else 0
            keyword_analysis[keyword] = {
                "count": count,
                "density": f"{density:.1f}%",
                "status": "good" if 0.5 <= density <= 2.5 else "needs_adjustment"
            }
        
        # Generate SEO-optimized version
        prompt = f"""Optimize this property description for SEO:

Original: {content}

Target keywords: {', '.join(target_keywords)}

Requirements:
- Include all target keywords naturally
- Add location-based keywords
- Include a compelling meta description (max 160 chars)
- Suggest 5 relevant tags/hashtags

Respond in this format:
OPTIMIZED_DESCRIPTION: [SEO-optimized text]
META_DESCRIPTION: [Meta description]
TITLE_TAG: [SEO title tag]
TAGS: [tag1, tag2, tag3, tag4, tag5]"""
        
        result = ai_service.generate(prompt, max_tokens=400)
        
        return {
            "original_word_count": word_count,
            "keyword_analysis": keyword_analysis,
            "suggestions": suggestions,
            "optimized": result,
            "readability_score": self._calculate_readability(content)
        }
    
    def _calculate_readability(self, text: str) -> Dict:
        """Calculate basic readability metrics."""
        sentences = text.split('.')
        words = text.split()
        
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Simple heuristic
        if avg_sentence_length < 10:
            level = "Easy"
        elif avg_sentence_length < 20:
            level = "Medium"
        else:
            level = "Complex"
        
        return {
            "avg_sentence_length": round(avg_sentence_length, 1),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "readability_level": level
        }
    
    async def _generate_full_campaign(self, data: Dict) -> Dict:
        """Generate a complete marketing campaign for a property."""
        property_id = data.get("property_id", f"prop_{datetime.now().timestamp()}")
        property_data = {
            "bedrooms": data.get("bedrooms", 3),
            "bathrooms": data.get("bathrooms", 2),
            "location": data.get("location", "Auckland"),
            "price": data.get("price", ""),
            "features": data.get("features", [])
        }
        
        # Generate all content types
        description = ai_service.generate_property_description(**property_data)
        
        social_posts = {}
        for platform in ["facebook", "instagram", "linkedin"]:
            social_posts[platform] = ai_service.generate_social_post(
                platform=platform, **property_data
            )
        
        # Create campaign structure
        campaign = {
            "campaign_id": f"campaign_{property_id}",
            "property": property_data,
            "assets": {
                "description": description,
                "social_posts": social_posts,
                "email_subject": f"New Listing: {property_data['bedrooms']} bed in {property_data['location']}",
                "email_preview": f"Don't miss this stunning {property_data['bedrooms']}-bedroom property!"
            },
            "schedule": self._generate_campaign_schedule(),
            "created_at": datetime.now().isoformat()
        }
        
        # Store campaign
        memory.set(f"content:{property_id}:campaign", campaign)
        
        return campaign
    
    def _generate_campaign_schedule(self) -> List[Dict]:
        """Generate recommended posting schedule."""
        return [
            {"day": 0, "platform": "all", "content": "Launch post", "time": "09:00"},
            {"day": 1, "platform": "facebook", "content": "Property highlight", "time": "18:00"},
            {"day": 2, "platform": "instagram", "content": "Photo feature", "time": "12:00"},
            {"day": 3, "platform": "linkedin", "content": "Market context", "time": "08:00"},
            {"day": 7, "platform": "all", "content": "Week recap/reminder", "time": "10:00"}
        ]
    
    async def _content_calendar(self, data: Dict) -> Dict:
        """Generate content calendar for upcoming period."""
        days = data.get("days", 30)
        properties = data.get("properties", [])
        
        calendar = []
        for day in range(days):
            date = datetime.now() + __import__('datetime').timedelta(days=day)
            
            # Rotate content types
            if day % 7 == 0:
                content_type = "market_update"
            elif day % 3 == 0 and properties:
                content_type = "property_feature"
            elif day % 2 == 0:
                content_type = "engagement_post"
            else:
                content_type = "educational"
            
            calendar.append({
                "date": date.strftime("%Y-%m-%d"),
                "day_of_week": date.strftime("%A"),
                "content_type": content_type,
                "suggested_platforms": self._get_platforms_for_content(content_type),
                "status": "planned"
            })
        
        return {
            "calendar": calendar,
            "total_days": days,
            "generated_at": datetime.now().isoformat()
        }
    
    def _get_platforms_for_content(self, content_type: str) -> List[str]:
        """Determine best platforms for content type."""
        mapping = {
            "market_update": ["linkedin", "facebook"],
            "property_feature": ["instagram", "facebook"],
            "engagement_post": ["facebook", "instagram"],
            "educational": ["linkedin", "facebook"]
        }
        return mapping.get(content_type, ["facebook"])
