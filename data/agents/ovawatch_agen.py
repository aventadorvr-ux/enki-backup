#!/usr/bin/env python3
"""
OVAWatch_Agen - THE OVERSEER
Optimizing Vigilant Agent for Watching, Analyzing, and Generating insights
Master monitoring agent for ENKI AGENTIC ecosystem
"""

import json
import sqlite3
import requests
import subprocess
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

# Local data directory
DATA_DIR = os.getenv("ENKI_DATA", "/data/data/com.termux/files/home/.openclaw/workspace/data/agents")
os.makedirs(DATA_DIR, exist_ok=True)

class OVAWatch_Agen:
    """OVAWatch_Agen - Agent Overseer and Verification Administrator"""
    
    def __init__(self):
        self.db_path = os.path.join(DATA_DIR, "overseer.db")
        self.api_base = "http://127.0.0.1:8000/api/v1"
        self.telegram_bot = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.telegram_chat = os.getenv("TELEGRAM_CHAT_ID", "")
        self.alert_cooldown = {}
        self.init_db()
        
    def init_db(self):
        """Initialize oversight database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS agent_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT NOT NULL,
            status TEXT NOT NULL,
            last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            response_time_ms INTEGER,
            error_count INTEGER DEFAULT 0,
            success_rate REAL DEFAULT 100.0,
            alert_sent BOOLEAN DEFAULT 0
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS performance_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT NOT NULL,
            metric_type TEXT NOT NULL,
            value REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT NOT NULL,
            incident_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT,
            resolved BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP
        )''')
        
        conn.commit()
        conn.close()
    
    def check_all_agents(self) -> Dict:
        """Complete health check of entire ENKI ecosystem"""
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_status": "healthy",
            "agents": {},
            "issues": [],
            "recommendations": []
        }
        
        # Check Lead Terminator
        lead_status = self._check_agent("lead_terminator", "stats")
        results["agents"]["lead_terminator"] = lead_status
        if lead_status["status"] != "healthy":
            results["issues"].append(f"Lead Terminator: {lead_status.get('error', 'Unknown')}")
            results["overall_status"] = "degraded"
        
        # Check Content Forge
        content_status = self._check_agent("content_forge", "templates")
        results["agents"]["content_forge"] = content_status
        if content_status["status"] != "healthy":
            results["issues"].append(f"Content Forge: {content_status.get('error', 'Unknown')}")
            results["overall_status"] = "degraded"
        
        # Check AGen_Legal
        legal_status = self._check_agent("agen_legal", "checklist")
        results["agents"]["agen_legal"] = legal_status
        if legal_status["status"] != "healthy":
            results["issues"].append(f"AGen_Legal: {legal_status.get('error', 'Unknown')}")
            results["overall_status"] = "degraded"
        
        # Check Database
        db_status = self._check_database()
        results["agents"]["database"] = db_status
        if db_status["status"] != "healthy":
            results["issues"].append(f"Database: {db_status.get('error', 'Unknown')}")
        
        return results
    
    def _check_agent(self, agent_name: str, command: str) -> Dict:
        """Check if an agent is responsive"""
        script_map = {
            "lead_terminator": "lead_terminator.py",
            "content_forge": "content_forge.py",
            "agen_legal": "agen_legal.py"
        }
        
        script = script_map.get(agent_name)
        if not script:
            return {"status": "error", "error": "Unknown agent"}
        
        script_path = os.path.join(os.path.dirname(__file__), script)
        
        try:
            result = subprocess.run(
                ["python3", script_path, command],
                capture_output=True,
                text=True,
                timeout=10,
                env={**os.environ, "ENKI_DATA": DATA_DIR, "NEMO_DB": os.path.join(DATA_DIR, "leads.db")}
            )
            
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    return {"status": "healthy", "data": data}
                except:
                    return {"status": "healthy", "output": result.stdout[:200]}
            else:
                return {"status": "error", "error": result.stderr[:200]}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _check_database(self) -> Dict:
        """Check database connectivity"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM agent_status")
            count = c.fetchone()[0]
            conn.close()
            return {"status": "healthy", "status_records": count}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_full_report(self) -> Dict:
        """Generate comprehensive system report"""
        health = self.check_all_agents()
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""
            SELECT * FROM incidents
            WHERE created_at > datetime('now', '-24 hours')
            ORDER BY created_at DESC
            LIMIT 10
        """)
        incidents = [
            {
                "id": row[0],
                "agent": row[1],
                "type": row[2],
                "severity": row[3],
                "description": row[4],
                "resolved": row[5],
                "created": row[7]
            }
            for row in c.fetchall()
        ]
        
        conn.close()
        
        return {
            "health_check": health,
            "incidents_24h": incidents,
            "next_check": (datetime.utcnow() + timedelta(minutes=5)).isoformat()
        }


if __name__ == "__main__":
    import sys
    
    ovawatch = OVAWatch_Agen()
    
    if len(sys.argv) < 2:
        result = ovawatch.check_all_agents()
        print(json.dumps(result, indent=2))
    elif sys.argv[1] == "check":
        result = ovawatch.check_all_agents()
        print(json.dumps(result, indent=2))
    elif sys.argv[1] == "report":
        report = ovawatch.get_full_report()
        print(json.dumps(report, indent=2))
    else:
        print(f"Unknown command: {sys.argv[1]}")
