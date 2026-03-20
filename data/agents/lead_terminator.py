#!/usr/bin/env python3
"""
ENKI LEAD TERMINATOR
Auto-qualification engine for real estate leads
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional
import sqlite3
import requests

# Local data directory
DATA_DIR = os.getenv("ENKI_DATA", "/data/data/com.termux/files/home/.openclaw/workspace/data/agents")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "leads.db")

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT_ID")

class LeadTerminator:
    """The machine that never sleeps."""
    
    def __init__(self):
        self.db = self._init_db()
    
    def _init_db(self):
        """Initialize the lead database."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY,
            source TEXT NOT NULL,
            contact_info TEXT NOT NULL,
            initial_message TEXT,
            conversation TEXT DEFAULT '[]',
            score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'new',
            hot_lead BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        return conn

    def process_inquiry(self, source: str, contact: str, message: str) -> Dict:
        """Process a new lead inquiry."""
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO leads (source, contact_info, initial_message) VALUES (?, ?, ?)",
            (source, contact, message)
        )
        lead_id = cursor.lastrowid
        self.db.commit()
        
        # Score the lead (simplified without AI)
        score = self._basic_score(message)
        cursor.execute(
            "UPDATE leads SET score = ? WHERE id = ?",
            (score, lead_id)
        )
        self.db.commit()
        
        # HOT LEAD ALERT
        if score >= 30:
            cursor.execute("UPDATE leads SET hot_lead = 1, status = 'hot' WHERE id = ?", (lead_id,))
            self.db.commit()
            self._alert_human(f"🔥 HOT LEAD ALERT!\n\nSource: {source}\nContact: {contact}\nScore: {score}/40")
        
        return {
            "lead_id": lead_id,
            "response": "Thanks for your inquiry! I'll get back to you shortly.",
            "score": score,
            "hot": score >= 30
        }
    
    def _basic_score(self, message: str) -> int:
        """Basic scoring without AI."""
        score = 20  # Default
        msg_lower = message.lower()
        
        # Timeline indicators
        if any(w in msg_lower for w in ["urgent", "asap", "immediately", "this week"]):
            score += 10
        if any(w in msg_lower for w in ["ready", "pre-approved", "cash"]):
            score += 8
        if any(w in msg_lower for w in ["just looking", "curious", "maybe"]):
            score -= 5
            
        return min(max(score, 0), 40)

    def _alert_human(self, message: str):
        """Send alert to human agent."""
        print(f"ALERT: {message}")

    def get_hot_leads(self) -> List[Dict]:
        """Get all hot leads requiring immediate action."""
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT id, source, contact_info, score, initial_message, created_at FROM leads WHERE hot_lead = 1 AND status = 'hot' ORDER BY score DESC"
        )
        return [
            {
                "id": row[0],
                "source": row[1],
                "contact": row[2],
                "score": row[3],
                "message": row[4],
                "created": row[5]
            }
            for row in cursor.fetchall()
        ]

    def get_stats(self) -> Dict:
        """Get lead statistics."""
        cursor = self.db.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM leads")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM leads WHERE hot_lead = 1")
        hot = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM leads WHERE DATE(created_at) = DATE('now')")
        today = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(score) FROM leads")
        avg_score = cursor.fetchone()[0] or 0
        
        return {
            "total_leads": total,
            "hot_leads": hot,
            "today_leads": today,
            "average_score": round(avg_score, 1)
        }


if __name__ == "__main__":
    terminator = LeadTerminator()
    
    if len(sys.argv) < 2:
        stats = terminator.get_stats()
        print(json.dumps(stats, indent=2))
    elif sys.argv[1] == "stats":
        stats = terminator.get_stats()
        print(json.dumps(stats, indent=2))
    elif sys.argv[1] == "hot":
        leads = terminator.get_hot_leads()
        print(json.dumps(leads, indent=2))
    elif sys.argv[1] == "process":
        result = terminator.process_inquiry(sys.argv[2], sys.argv[3], sys.argv[4])
        print(json.dumps(result, indent=2))
    else:
        print(f"Unknown command: {sys.argv[1]}")
