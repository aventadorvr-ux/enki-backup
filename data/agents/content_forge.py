#!/usr/bin/env python3
"""
CONTENT FORGE - ENKI AGENTIC
AI-powered content generation for real estate
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional

# Local data directory
DATA_DIR = os.getenv("ENKI_DATA", "/data/data/com.termux/files/home/.openclaw/workspace/data/agents")
os.makedirs(DATA_DIR, exist_ok=True)

class ContentForge:
    """The Content Forge - AI content generation engine"""
    
    def __init__(self):
        self.db_path = os.path.join(DATA_DIR, "content.db")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.init_db()
        
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
        # Simplified without AI for now
        content = f"""Welcome to this stunning {property_data.get('type', 'home')} in {property_data.get('location', '')}.

Featuring {property_data.get('bedrooms', 'spacious')} bedrooms and {property_data.get('bathrooms', 'modern')} bathrooms, 
this property offers everything you've been looking for. {', '.join(property_data.get('features', ['Great location', 'Modern design']))}.

Priced at {property_data.get('price', 'Contact for price')}. Don't miss this opportunity!

Contact us today to arrange a viewing."""
        
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


if __name__ == "__main__":
    import sys
    
    forge = ContentForge()
    
    if len(sys.argv) < 2:
        templates = forge.get_templates()
        print(json.dumps(templates, indent=2))
    elif sys.argv[1] == "templates":
        content_type = sys.argv[2] if len(sys.argv) > 2 else None
        templates = forge.get_templates(content_type)
        print(json.dumps(templates, indent=2))
    elif sys.argv[1] == "property":
        data = json.loads(sys.argv[2])
        result = forge.generate_property_description(data)
        print(json.dumps(result, indent=2))
    elif sys.argv[1] == "recent":
        content = forge.get_recent_content()
        print(json.dumps(content, indent=2))
    else:
        print(f"Unknown command: {sys.argv[1]}")
