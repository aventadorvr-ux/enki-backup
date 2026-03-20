#!/usr/bin/env python3
"""
ENKI LEAD TERMINATOR
Auto-qualification engine for real estate leads
Zero pain tolerance. Maximum conversion.
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional
import sqlite3
import requests

# Configuration
DB_PATH = os.getenv('NEMO_DB', '/home/ubuntu/nz-realestate-ai/data/leads.db')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
TELEGRAM_BOT = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT = os.getenv('TELEGRAM_CHAT_ID')
TRademe_WEBHOOK = os.getenv('TRADEME_WEBHOOK_URL')

class LeadTerminator:
    """The machine that never sleeps."""
    
    def __init__(self):
        self.db = self._init_db()
        self.qualification_prompt = """You are a senior real estate agent with 20 years experience.
Your job is to qualify leads through conversation.

QUALIFICATION CRITERIA (Score 1-10 each):
1. TIMELINE: When do they want to buy/sell? (10 = <30 days, 1 = >12 months)
2. BUDGET: Do they have financing ready? (10 = pre-approved, 1 = dreaming)
3. AUTHORITY: Are they decision makers? (10 = yes, 1 = tire kicker)
4. MOTIVATION: How urgent is their need? (10 = must move, 1 = curious)

CONVERSATION RULES:
- Ask ONE question at a time
- Be friendly but efficient
- Get to the point fast
- Don't waste time on unqualified leads
- Hot leads (score >30) → Request phone call immediately

Current conversation:
{conversation}

Respond as the agent. One question or statement only."""

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
        # Store lead
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO leads (source, contact_info, initial_message) VALUES (?, ?, ?)",
            (source, contact, message)
        )
        lead_id = cursor.lastrowid
        self.db.commit()
        
        # Generate first response
        conversation = [{"role": "lead", "content": message}]
        response = self._generate_response(conversation)
        
        # Update conversation
        conversation.append({"role": "agent", "content": response})
        cursor.execute(
            "UPDATE leads SET conversation = ? WHERE id = ?",
            (json.dumps(conversation), lead_id)
        )
        self.db.commit()
        
        # Score the lead
        score = self._score_lead(conversation)
        cursor.execute(
            "UPDATE leads SET score = ? WHERE id = ?",
            (score, lead_id)
        )
        self.db.commit()
        
        # HOT LEAD ALERT
        if score >= 30:
            cursor.execute("UPDATE leads SET hot_lead = 1, status = 'hot' WHERE id = ?", (lead_id,))
            self.db.commit()
            self._alert_human(f"🔥 HOT LEAD ALERT!\n\nSource: {source}\nContact: {contact}\nScore: {score}/40\nMessage: {message[:200]}...\n\nRespond immediately!")
        
        return {
            "lead_id": lead_id,
            "response": response,
            "score": score,
            "hot": score >= 30
        }

    def _generate_response(self, conversation: List[Dict]) -> str:
        """Generate AI response to lead."""
        if not OPENAI_KEY:
            return "Thanks for your inquiry! I'll get back to you shortly."
        
        try:
            conv_text = "\n".join([f"{'Lead' if c['role'] == 'lead' else 'Agent'}: {c['content']}" for c in conversation])
            
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_KEY}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": self.qualification_prompt.format(conversation=conv_text)},
                        {"role": "user", "content": "Respond to this lead."}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 150
                },
                timeout=10
            )
            return resp.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            return "Thanks for reaching out! I'd love to help. What's your timeline?"

    def _score_lead(self, conversation: List[Dict]) -> int:
        """Score lead quality based on conversation."""
        if not OPENAI_KEY:
            return 20  # Default mid-score
        
        try:
            conv_text = "\n".join([f"{'Lead' if c['role'] == 'lead' else 'Agent'}: {c['content']}" for c in conversation])
            
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_KEY}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "Score this real estate lead 0-40 based on: timeline (0-10), budget/financing (0-10), decision authority (0-10), motivation (0-10). Return ONLY a number."},
                        {"role": "user", "content": conv_text}
                    ],
                    "temperature": 0,
                    "max_tokens": 5
                },
                timeout=10
            )
            score_text = resp.json()['choices'][0]['message']['content'].strip()
            return int(''.join(filter(str.isdigit, score_text)) or 20)
        except:
            return 20

    def _alert_human(self, message: str):
        """Send alert to human agent."""
        print(f"ALERT: {message}")
        
        if TELEGRAM_BOT and TELEGRAM_CHAT:
            try:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
                    json={
                        "chat_id": TELEGRAM_CHAT,
                        "text": message,
                        "parse_mode": "HTML"
                    },
                    timeout=5
                )
            except:
                pass

    def continue_conversation(self, lead_id: int, lead_message: str) -> Dict:
        """Continue an existing conversation."""
        cursor = self.db.cursor()
        cursor.execute("SELECT conversation, score FROM leads WHERE id = ?", (lead_id,))
        row = cursor.fetchone()
        
        if not row:
            return {"error": "Lead not found"}
        
        conversation = json.loads(row[0])
        conversation.append({"role": "lead", "content": lead_message})
        
        response = self._generate_response(conversation)
        conversation.append({"role": "agent", "content": response})
        
        new_score = self._score_lead(conversation)
        
        cursor.execute(
            "UPDATE leads SET conversation = ?, score = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (json.dumps(conversation), new_score, lead_id)
        )
        self.db.commit()
        
        # Alert if just became hot
        if new_score >= 30 and row[1] < 30:
            cursor.execute("SELECT contact_info FROM leads WHERE id = ?", (lead_id,))
            contact = cursor.fetchone()[0]
            self._alert_human(f"🔥 LEAD ESCALATED TO HOT!\n\nContact: {contact}\nNew Score: {new_score}/40\n\nTAKE ACTION NOW!")
            cursor.execute("UPDATE leads SET hot_lead = 1, status = 'hot' WHERE id = ?", (lead_id,))
            self.db.commit()
        
        return {
            "lead_id": lead_id,
            "response": response,
            "score": new_score,
            "hot": new_score >= 30
        }

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
        print("Usage: lead_terminator.py <command> [args]")
        print("Commands: process, continue, hot, stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "process":
        # lead_terminator.py process <source> <contact> <message>
        result = terminator.process_inquiry(sys.argv[2], sys.argv[3], sys.argv[4])
        print(json.dumps(result, indent=2))
    
    elif command == "continue":
        # lead_terminator.py continue <lead_id> <message>
        result = terminator.continue_conversation(int(sys.argv[2]), sys.argv[3])
        print(json.dumps(result, indent=2))
    
    elif command == "hot":
        leads = terminator.get_hot_leads()
        print(json.dumps(leads, indent=2))
    
    elif command == "stats":
        stats = terminator.get_stats()
        print(json.dumps(stats, indent=2))
