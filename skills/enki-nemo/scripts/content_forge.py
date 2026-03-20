#!/usr/bin/env python3
"""
CONTENT FORGE - ENKI AGENTIC
AI-powered content generation for real estate
Produces descriptions, social posts, emails that convert
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional
import requests

class ContentForge:
    """
    The Content Forge - AI content generation engine
    Creates compelling real estate marketing content
    """
    
    def __init__(self):
        self.db_path = "/home/ubuntu/enki-agentic/data/content.db"
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.init_db()
        
        # Brand voice settings
        self.brand_voice = {
            "tone": "professional yet warm",
            "style": "benefit-focused, evocative, urgency without pressure",
            "avoid": ["cliché", "generic", "pushy sales language"]
        }
    
    def init_db(self):
        """Initialize content database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS content_templates (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            template TEXT NOT NULL,
            usage_count INTEGER DEFAULT 0,
            avg_engagement REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS generated_content (
            id INTEGER PRIMARY KEY,
            content_type TEXT NOT NULL,
            input_data TEXT,
            output_content TEXT NOT NULL,
            platform TEXT,
            engagement_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Seed default templates
        templates = [
            ("property_description_luxury", "property", 
             "Write a compelling property description for a {property_type} in {location}. "
             "Key features: {features}. Price: {price}. Target buyer: {target}. "
             "Make it evocative, benefit-focused, and create urgency."),
            ("social_instagram", "social",
             "Create an Instagram caption for: {property_type} in {location}. "
             "Include relevant hashtags. Keep it under 150 words. Add emojis."),
            ("email_new_listing", "email",
             "Write an email announcing a new listing: {property_type} in {location}, {price}. "
             "Target: {target}. Subject line and body. Professional but exciting."),
            ("market_update", "market",
             "Write a market update for {location} real estate. "
             "Data: {market_data}. Tone: informative but optimistic.")
        ]
        
        for name, typ, template in templates:
            c.execute("INSERT OR IGNORE INTO content_templates (name, type, template) VALUES (?, ?, ?)",
                     (name, typ, template))
        
        conn.commit()
        conn.close()
    
    def generate_property_description(self, property_data: Dict) -> Dict:
        """Generate compelling property description"""
        
        prompt = f"""You are an expert real estate copywriter with 20 years experience.
Your descriptions sell properties faster and for more money.

PROPERTY DETAILS:
- Type: {property_data.get('type', 'Home')}
- Location: {property_data.get('location', '')}
- Price: {property_data.get('price', '')}
- Bedrooms: {property_data.get('bedrooms', '')}
- Bathrooms: {property_data.get('bathrooms', '')}
- Size: {property_data.get('size', '')}
- Key Features: {', '.join(property_data.get('features', []))}
- Unique Selling Points: {property_data.get('highlights', '')}

WRITE A PROPERTY DESCRIPTION THAT:
1. Hooks the reader in the first sentence
2. Paints a lifestyle picture, not just features
3. Uses sensory language (imagine, picture, feel)
4. Creates subtle urgency
5. Ends with a clear call-to-action

Format: 3-4 short paragraphs. Professional but warm. No clichés."""

        content = self._generate_with_ai(prompt)
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO generated_content (content_type, input_data, output_content, platform) VALUES (?, ?, ?, ?)",
            ("property_description", json.dumps(property_data), content, "listing")
        )
        conn.commit()
        conn.close()
        
        return {
            "type": "property_description",
            "content": content,
            "word_count": len(content.split()),
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_social_post(self, platform: str, property_data: Dict, post_type: str = "listing") -> Dict:
        """Generate social media content"""
        
        platform_prompts = {
            "instagram": f"""Create an Instagram post for this property:
{property_data.get('type')} in {property_data.get('location')} - {property_data.get('price')}

Requirements:
- Hook in first line
- Emoji-appropriate but not overdone
- 5-8 relevant hashtags
- Call-to-action
- Keep under 200 words
- Make it scroll-stopping""",
            
            "facebook": f"""Write a Facebook post for:
{property_data.get('type')} in {property_data.get('location')} - {property_data.get('price')}

- More detailed than Instagram
- Tell a mini-story
- Include price (Facebook allows this)
- Ask engagement question
- Professional but friendly""",
            
            "linkedin": f"""Professional LinkedIn post about:
{property_data.get('type')} in {property_data.get('location')} - {property_data.get('price')}

- Market insights angle
- Professional tone
- Investment perspective
- No emojis
- 2-3 paragraphs max"""
        }
        
        prompt = platform_prompts.get(platform, platform_prompts["instagram"])
        content = self._generate_with_ai(prompt)
        
        # Save
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO generated_content (content_type, input_data, output_content, platform) VALUES (?, ?, ?, ?)",
            (f"social_{post_type}", json.dumps(property_data), content, platform)
        )
        conn.commit()
        conn.close()
        
        return {
            "platform": platform,
            "content": content,
            "char_count": len(content),
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_email_campaign(self, campaign_type: str, data: Dict) -> Dict:
        """Generate email marketing content"""
        
        email_prompts = {
            "new_listing": f"""Write an email announcing a new listing:

Property: {data.get('property_type')} in {data.get('location')}
Price: {data.get('price')}
Target Audience: {data.get('audience', 'buyers')}

Include:
1. Compelling subject line (open-worthy)
2. Opening hook
3. Property highlights (3-4 bullet points)
4. Why this opportunity matters
5. Clear CTA
6. Professional sign-off

Length: 200-300 words""",
            
            "market_update": f"""Write a market update newsletter:

Area: {data.get('location')}
Key Stats: {data.get('stats', '')}
Trend: {data.get('trend', 'stable')}

Structure:
1. Subject line about market insights
2. Brief market summary
3. 2-3 key data points
4. What this means for buyers/sellers
5. CTA to contact for personalized advice

Tone: Informative, authoritative, optimistic""",
            
            "nurture": f"""Write a nurture email for leads who inquired {data.get('days_ago', 7)} days ago:

Lead Interest: {data.get('interest', 'general')}

Purpose: Stay top-of-mind, provide value
Include:
1. Friendly check-in
2. Market insight or tip
3. New listing they might like
4. Soft invitation to connect

Not pushy. Relationship-building."""
        }
        
        prompt = email_prompts.get(campaign_type, email_prompts["new_listing"])
        
        # For subject line + body separation
        full_content = self._generate_with_ai(prompt)
        
        # Try to extract subject line
        lines = full_content.split('\n')
        subject = "New Property Opportunity"
        body = full_content
        
        for line in lines[:5]:
            if "subject" in line.lower() or line.startswith("Subject:"):
                subject = line.replace("Subject:", "").replace("Subject Line:", "").strip()
                body = '\n'.join(lines[lines.index(line)+1:]).strip()
                break
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO generated_content (content_type, input_data, output_content, platform) VALUES (?, ?, ?, ?)",
            (f"email_{campaign_type}", json.dumps(data), full_content, "email")
        )
        conn.commit()
        conn.close()
        
        return {
            "campaign_type": campaign_type,
            "subject_line": subject,
            "body": body,
            "full_content": full_content,
            "generated_at": datetime.now().isoformat()
        }
    
    def get_templates(self, content_type: str = None) -> List[Dict]:
        """Get content templates"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        if content_type:
            c.execute("SELECT * FROM content_templates WHERE type = ? ORDER BY usage_count DESC", (content_type,))
        else:
            c.execute("SELECT * FROM content_templates ORDER BY usage_count DESC")
        
        templates = [
            {
                "id": row[0],
                "name": row[1],
                "type": row[2],
                "template": row[3],
                "usage_count": row[4],
                "avg_engagement": row[5]
            }
            for row in c.fetchall()
        ]
        
        conn.close()
        return templates
    
    def get_recent_content(self, limit: int = 10) -> List[Dict]:
        """Get recently generated content"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""
            SELECT * FROM generated_content 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        content = [
            {
                "id": row[0],
                "type": row[1],
                "platform": row[4],
                "content_preview": row[3][:100] + "..." if len(row[3]) > 100 else row[3],
                "created": row[6]
            }
            for row in c.fetchall()
        ]
        
        conn.close()
        return content
    
    def _generate_with_ai(self, prompt: str) -> str:
        """Generate content using OpenAI"""
        if not self.openai_key:
            return "[AI generation requires OpenAI API key]"
        
        try:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.openai_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are an expert real estate marketing copywriter. Create compelling, authentic content that converts."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.75,
                    "max_tokens": 800
                },
                timeout=30
            )
            return resp.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"[Generation error: {str(e)}]"


if __name__ == "__main__":
    import sys
    
    forge = ContentForge()
    
    if len(sys.argv) < 2:
        print("Usage: content_forge.py <command>")
        print("Commands:")
        print("  property <json_data> - Generate property description")
        print("  social <platform> <json_data> - Generate social post")
        print("  email <type> <json_data> - Generate email campaign")
        print("  templates - List templates")
        print("  recent - Recent content")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "property":
        data = json.loads(sys.argv[2])
        result = forge.generate_property_description(data)
        print(json.dumps(result, indent=2))
    
    elif command == "social":
        platform = sys.argv[2]
        data = json.loads(sys.argv[3])
        result = forge.generate_social_post(platform, data)
        print(json.dumps(result, indent=2))
    
    elif command == "email":
        email_type = sys.argv[2]
        data = json.loads(sys.argv[3])
        result = forge.generate_email_campaign(email_type, data)
        print(json.dumps(result, indent=2))
    
    elif command == "templates":
        content_type = sys.argv[2] if len(sys.argv) > 2 else None
        templates = forge.get_templates(content_type)
        print(json.dumps(templates, indent=2))
    
    elif command == "recent":
        content = forge.get_recent_content()
        print(json.dumps(content, indent=2))
