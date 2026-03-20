#!/usr/bin/env python3
"""
OVAWatch_Agen - THE OVERSEER
Optimizing Vigilant Agent for Watching, Analyzing, and Generating insights

Master monitoring agent for ENKI AGENTIC ecosystem
Ensures 100% performance, 100% efficiency, 0% tolerance for failure
"""

import json
import sqlite3
import requests
import subprocess
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

class OVAWatch_Agen:
    """
    OVAWatch_Agen - Agent Overseer and Verification Administrator
    
    Mission: Monitor all ENKI agents, detect failures, enforce performance,
    escalate issues, maintain 100% operational status
    """
    
    def __init__(self):
        self.db_path = "/home/ubuntu/enki-agentic/data/overseer.db"
        self.api_base = "http://127.0.0.1:8000/api/v1"
        self.telegram_bot = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.telegram_chat = os.getenv("TELEGRAM_CHAT_ID", "")
        self.alert_cooldown = {}  # Prevent spam
        self.init_db()
        
    def init_db(self):
        """Initialize oversight database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Agent status tracking
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
        
        # Performance metrics
        c.execute('''CREATE TABLE IF NOT EXISTS performance_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT NOT NULL,
            metric_type TEXT NOT NULL,
            value REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Incident log
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
        
        # 1. Check Lead Terminator
        lead_status = self._check_lead_terminator()
        results["agents"]["lead_terminator"] = lead_status
        if lead_status["status"] != "healthy":
            results["issues"].append(f"Lead Terminator: {lead_status['error']}")
            results["overall_status"] = "degraded"
        
        # 2. Check ENKI API
        api_status = self._check_enki_api()
        results["agents"]["enki_api"] = api_status
        if api_status["status"] != "healthy":
            results["issues"].append(f"ENKI API: {api_status.get('error', 'Unknown')}")
            results["overall_status"] = "critical"
        
        # 3. Check Database
        db_status = self._check_database()
        results["agents"]["database"] = db_status
        if db_status["status"] != "healthy":
            results["issues"].append(f"Database: {db_status['error']}")
            results["overall_status"] = "critical"
        
        # 4. Check System Resources
        resource_status = self._check_resources()
        results["agents"]["system_resources"] = resource_status
        if resource_status["status"] != "healthy":
            results["issues"].append(f"System: {resource_status.get('warning', 'Resource issue')}")
        
        # 5. Check nginx
        nginx_status = self._check_nginx()
        results["agents"]["nginx"] = nginx_status
        
        # Performance metrics
        results["performance"] = self._get_performance_metrics()
        
        # Critical alert if overall degraded
        if results["overall_status"] != "healthy":
            self._escalate_critical(results)
        
        return results
    
    def _check_lead_terminator(self) -> Dict:
        """Check Lead Terminator agent"""
        start = time.time()
        try:
            result = subprocess.run(
                [
                    "/home/ubuntu/enki-agentic/venv/bin/python3",
                    "/home/ubuntu/enki-agentic/scripts/lead_terminator.py",
                    "stats"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            elapsed = int((time.time() - start) * 1000)
            
            if result.returncode == 0:
                stats = json.loads(result.stdout)
                self._log_performance("lead_terminator", "response_time", elapsed)
                return {
                    "status": "healthy",
                    "response_time_ms": elapsed,
                    "stats": stats
                }
            else:
                return {"status": "error", "error": result.stderr}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _check_enki_api(self) -> Dict:
        """Check ENKI API endpoints"""
        start = time.time()
        try:
            resp = requests.get(f"{self.api_base}/enki/status", timeout=5)
            elapsed = int((time.time() - start) * 1000)
            
            if resp.status_code == 200:
                data = resp.json()
                self._log_performance("enki_api", "response_time", elapsed)
                return {
                    "status": "healthy",
                    "response_time_ms": elapsed,
                    "agents": data.get("agents", {})
                }
            else:
                return {"status": "error", "error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _check_database(self) -> Dict:
        """Check database connectivity"""
        try:
            conn = sqlite3.connect("/home/ubuntu/enki-agentic/data/leads.db")
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM leads")
            count = c.fetchone()[0]
            conn.close()
            return {"status": "healthy", "lead_count": count}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _check_resources(self) -> Dict:
        """Check system resources"""
        try:
            result = subprocess.run(
                ["free", "-m"],
                capture_output=True,
                text=True
            )
            
            disk = subprocess.run(
                ["df", "-h", "/home"],
                capture_output=True,
                text=True
            )
            
            status = "healthy"
            warning = None
            
            if result.stdout:
                lines = result.stdout.split('\n')
                if len(lines) > 1:
                    mem_info = lines[1].split()
                    if len(mem_info) > 3:
                        mem_used_percent = int(mem_info[2]) / int(mem_info[1]) * 100 if mem_info[1] != '0' else 0
                        if mem_used_percent > 90:
                            status = "warning"
                            warning = f"Memory usage at {mem_used_percent:.1f}%"
            
            return {
                "status": status,
                "warning": warning,
                "memory": result.stdout[:200] if result.stdout else "N/A",
                "disk": disk.stdout[:200] if disk.stdout else "N/A"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _check_nginx(self) -> Dict:
        """Check nginx status"""
        try:
            result = subprocess.run(
                ["systemctl", "is-active", "nginx"],
                capture_output=True,
                text=True
            )
            return {
                "status": "healthy" if result.stdout.strip() == "active" else "error",
                "state": result.stdout.strip()
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _log_performance(self, agent: str, metric: str, value: float):
        """Log performance metric"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO performance_log (agent_name, metric_type, value) VALUES (?, ?, ?)",
            (agent, metric, value)
        )
        conn.commit()
        conn.close()
    
    def _get_performance_metrics(self) -> Dict:
        """Get recent performance metrics"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""
            SELECT agent_name, AVG(value) as avg_value, COUNT(*) as count
            FROM performance_log
            WHERE metric_type = 'response_time' 
            AND timestamp > datetime('now', '-1 hour')
            GROUP BY agent_name
        """)
        
        metrics = {}
        for row in c.fetchall():
            metrics[row[0]] = {
                "avg_response_ms": round(row[1], 2),
                "requests_count": row[2]
            }
        
        conn.close()
        return metrics
    
    def _escalate_critical(self, results: Dict):
        """Escalate critical issues to human"""
        alert_key = "critical_" + datetime.utcnow().strftime("%Y%m%d%H")
        
        if alert_key in self.alert_cooldown:
            return
        self.alert_cooldown[alert_key] = True
        
        old_keys = [k for k in self.alert_cooldown.keys() if k < alert_key]
        for k in old_keys:
            del self.alert_cooldown[k]
        
        message = f"""🚨 OVAWatch_Agen CRITICAL ALERT 🚨

Status: {results['overall_status'].upper()}
Time: {results['timestamp']}

ISSUES DETECTED:
"""
        for issue in results['issues']:
            message += f"• {issue}\n"
        
        message += "\nIMMEDIATE ACTION REQUIRED"
        
        print(message)
        
        if self.telegram_bot and self.telegram_chat:
            try:
                requests.post(
                    f"https://api.telegram.org/bot{self.telegram_bot}/sendMessage",
                    json={
                        "chat_id": self.telegram_chat,
                        "text": message,
                        "parse_mode": "HTML"
                    },
                    timeout=5
                )
            except:
                pass
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        for issue in results['issues']:
            c.execute(
                "INSERT INTO incidents (agent_name, incident_type, severity, description) VALUES (?, ?, ?, ?)",
                ("system", "health_check_failure", "critical" if results['overall_status'] == 'critical' else 'warning', issue)
            )
        conn.commit()
        conn.close()
    
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
            "recommendations": self._generate_recommendations(health),
            "next_check": (datetime.utcnow() + timedelta(minutes=5)).isoformat()
        }
    
    def _generate_recommendations(self, health: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recs = []
        
        if health["overall_status"] != "healthy":
            recs.append("IMMEDIATE: Address critical system issues")
        
        for agent, perf in health.get("performance", {}).items():
            if perf.get("avg_response_ms", 0) > 5000:
                recs.append(f"Optimize {agent}: Response time >5s (current: {perf['avg_response_ms']}ms)")
        
        if health["agents"].get("lead_terminator", {}).get("stats", {}).get("hot_leads", 0) > 0:
            recs.append("ACTION: Hot leads waiting - follow up immediately")
        
        if not recs:
            recs.append("All systems operating at optimal performance")
        
        return recs
    
    def auto_repair(self) -> Dict:
        """Attempt automatic repairs"""
        repairs = []
        
        nginx_status = self._check_nginx()
        if nginx_status["status"] != "healthy":
            subprocess.run(["sudo", "systemctl", "restart", "nginx"], timeout=30)
            repairs.append("nginx restarted")
        
        api_status = self._check_enki_api()
        if api_status["status"] != "healthy":
            subprocess.run(["pkill", "-f", "uvicorn"], timeout=10)
            time.sleep(2)
            subprocess.run([
                "bash", "-c",
                "cd ~/nz-realestate-ai && source venv/bin/activate && nohup uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2 > /tmp/uvicorn.log 2>&1 &"
            ], timeout=30)
            repairs.append("API service restarted")
        
        return {
            "repairs_made": repairs,
            "status_after": self.check_all_agents()
        }


if __name__ == "__main__":
    import sys
    
    ovawatch = OVAWatch_Agen()
    
    if len(sys.argv) < 2:
        print("Usage: ovawatch_agen.py <command>")
        print("Commands: check, report, repair")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        result = ovawatch.check_all_agents()
        print(json.dumps(result, indent=2))
    
    elif command == "report":
        report = ovawatch.get_full_report()
        print(json.dumps(report, indent=2))
    
    elif command == "repair":
        result = ovawatch.auto_repair()
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
