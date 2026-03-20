#!/usr/bin/env python3
"""
AGen_Legal - Legal & Business Compliance Agent
Handles all legal, regulatory, and business formation matters for ENKI AGENTIC
"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

class AGen_Legal:
    """
    AGen_Legal - Legal and Business Compliance Specialist
    
    Responsibilities:
    - Business registration and licensing
    - Legal entity formation
    - Compliance monitoring
    - Contract review and management
    - Regulatory requirements tracking
    - Intellectual property protection
    """
    
    def __init__(self):
        self.db_path = "/home/ubuntu/enki-agentic/data/legal.db"
        self.jurisdiction = "New Zealand"  # Default, configurable
        self.init_db()
        
    def init_db(self):
        """Initialize legal compliance database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS legal_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            task_name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            deadline DATE,
            completed_at TIMESTAMP,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS compliance_requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jurisdiction TEXT NOT NULL,
            requirement_type TEXT NOT NULL,
            description TEXT NOT NULL,
            frequency TEXT,
            last_completed DATE,
            next_due DATE,
            status TEXT DEFAULT 'active'
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_type TEXT NOT NULL,
            filename TEXT,
            version TEXT,
            status TEXT DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Seed initial business setup tasks
        initial_tasks = [
            ("Business Formation", "Company Name Registration", "Register 'ENKI AGENTIC' as business name with NZ Companies Office", "high", "2026-03-25"),
            ("Business Formation", "Company Incorporation", "Incorporate company as legal entity (Ltd)", "high", "2026-03-30"),
            ("Licensing", "Real Estate License", "Obtain necessary real estate agency licenses", "high", "2026-04-15"),
            ("Licensing", "Software/AI Business License", "Register as software/AI service provider", "medium", "2026-04-30"),
            ("Tax", "IRD Registration", "Register with Inland Revenue for GST, PAYE if employing", "high", "2026-03-28"),
            ("Compliance", "Privacy Act Compliance", "Ensure compliance with NZ Privacy Act 2020", "high", "2026-04-10"),
            ("Compliance", "Data Protection", "Implement data protection policies for client data", "high", "2026-04-10"),
            ("Contracts", "Terms of Service", "Draft Terms of Service for platform users", "high", "2026-03-27"),
            ("Contracts", "Privacy Policy", "Draft Privacy Policy for website/app", "high", "2026-03-27"),
            ("Contracts", "Service Agreement", "Draft service agreements for real estate agents", "medium", "2026-04-05"),
            ("IP", "Trademark Search", "Search and register trademarks for ENKI brand", "medium", "2026-04-20"),
            ("IP", "Copyright Notices", "Implement copyright notices on all IP", "low", "2026-04-30"),
            ("Insurance", "Professional Indemnity", "Obtain professional indemnity insurance", "high", "2026-04-15"),
            ("Insurance", "Cyber Liability", "Obtain cyber liability insurance", "medium", "2026-04-30"),
            ("Employment", "Employment Agreements", "Draft employment contracts if hiring", "low", "2026-05-30"),
        ]
        
        for category, task, desc, priority, deadline in initial_tasks:
            c.execute('''INSERT OR IGNORE INTO legal_tasks 
                (category, task_name, description, priority, deadline, status)
                VALUES (?, ?, ?, ?, ?, 'pending')''', 
                (category, task, desc, priority, deadline))
        
        conn.commit()
        conn.close()
    
    def get_business_setup_checklist(self) -> Dict:
        """Get complete business formation checklist"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT * FROM legal_tasks ORDER BY deadline, priority")
        tasks = []
        for row in c.fetchall():
            tasks.append({
                "id": row[0],
                "category": row[1],
                "task": row[2],
                "description": row[3],
                "status": row[4],
                "priority": row[5],
                "deadline": row[6],
                "created": row[9]
            })
        
        # Calculate completion stats
        total = len(tasks)
        completed = len([t for t in tasks if t["status"] == "completed"])
        high_priority_pending = len([t for t in tasks if t["priority"] == "high" and t["status"] != "completed"])
        
        conn.close()
        
        return {
            "total_tasks": total,
            "completed": completed,
            "completion_rate": f"{(completed/total*100):.1f}%" if total > 0 else "0%",
            "high_priority_pending": high_priority_pending,
            "tasks": tasks
        }
    
    def update_task_status(self, task_id: int, status: str, notes: str = None):
        """Update task status"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        completed_at = datetime.now().isoformat() if status == "completed" else None
        
        c.execute('''UPDATE legal_tasks 
            SET status = ?, notes = ?, completed_at = ?
            WHERE id = ?''', (status, notes, completed_at, task_id))
        
        conn.commit()
        conn.close()
        return {"status": "updated", "task_id": task_id}
    
    def get_compliance_calendar(self) -> Dict:
        """Get compliance deadlines calendar"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT * FROM legal_tasks 
            WHERE status != 'completed' 
            ORDER BY deadline''')
        
        upcoming = []
        overdue = []
        today = datetime.now().date()
        
        for row in c.fetchall():
            task = {
                "id": row[0],
                "category": row[1],
                "task": row[2],
                "deadline": row[6],
                "priority": row[5]
            }
            
            if row[6]:
                deadline = datetime.strptime(row[6], "%Y-%m-%d").date()
                if deadline < today:
                    overdue.append(task)
                else:
                    upcoming.append(task)
        
        conn.close()
        
        return {
            "overdue": overdue,
            "upcoming": upcoming,
            "overdue_count": len(overdue),
            "upcoming_count": len(upcoming)
        }
    
    def generate_legal_report(self) -> Dict:
        """Generate comprehensive legal status report"""
        checklist = self.get_business_setup_checklist()
        compliance = self.get_compliance_calendar()
        
        return {
            "report_date": datetime.now().isoformat(),
            "jurisdiction": self.jurisdiction,
            "business_name": "ENKI AGENTIC",
            "formation_status": checklist,
            "compliance_status": compliance,
            "urgent_actions": self._get_urgent_actions(checklist, compliance),
            "recommendations": self._generate_recommendations(checklist, compliance)
        }
    
    def _get_urgent_actions(self, checklist: Dict, compliance: Dict) -> List[str]:
        """Get list of urgent actions needed"""
        actions = []
        
        if compliance["overdue_count"] > 0:
            actions.append(f"CRITICAL: {compliance['overdue_count']} overdue tasks require immediate action")
        
        if checklist["high_priority_pending"] > 0:
            actions.append(f"HIGH: {checklist['high_priority_pending']} high-priority tasks pending")
        
        if checklist["completion_rate"] == "0%":
            actions.append("ACTION REQUIRED: Business formation not started")
        
        return actions
    
    def _generate_recommendations(self, checklist: Dict, compliance: Dict) -> List[str]:
        """Generate legal recommendations"""
        recs = []
        
        if checklist["completion_rate"] == "0%":
            recs.append("IMMEDIATE: Begin company name registration with NZ Companies Office")
            recs.append("WEEK 1: Incorporate company as limited liability entity")
            recs.append("WEEK 1: Register with IRD for tax obligations")
        
        if compliance["overdue_count"] == 0 and checklist["completion_rate"] == "0%":
            recs.append("You're on track - begin with business formation tasks")
        
        return recs
    
    def get_document_templates(self) -> Dict:
        """Get legal document templates needed"""
        templates = {
            "business_formation": [
                "Company Registration Form",
                "Constitution (if custom)",
                "Director/Shareholder Consents",
                "Share Register"
            ],
            "contracts": [
                "Terms of Service",
                "Privacy Policy",
                "Service Level Agreement",
                "Client Engagement Letter",
                "Employment Agreement Template"
            ],
            "compliance": [
                "Data Protection Policy",
                "Privacy Impact Assessment",
                "Information Security Policy",
                "Incident Response Plan"
            ],
            "ip": [
                "Trademark Application",
                "Copyright Assignment",
                "IP Assignment (contractors)"
            ]
        }
        return templates


if __name__ == "__main__":
    import sys
    
    legal = AGen_Legal()
    
    if len(sys.argv) < 2:
        print("AGen_Legal - Legal & Business Compliance Agent")
        print("\nUsage: agen_legal.py <command>")
        print("\nCommands:")
        print("  checklist          - Show business setup checklist")
        print("  compliance         - Show compliance calendar")
        print("  report             - Generate full legal report")
        print("  templates          - List document templates needed")
        print("  update <id> <status> [notes] - Update task status")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "checklist":
        result = legal.get_business_setup_checklist()
        print(json.dumps(result, indent=2))
    
    elif command == "compliance":
        result = legal.get_compliance_calendar()
        print(json.dumps(result, indent=2))
    
    elif command == "report":
        result = legal.generate_legal_report()
        print(json.dumps(result, indent=2))
    
    elif command == "templates":
        result = legal.get_document_templates()
        print(json.dumps(result, indent=2))
    
    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: agen_legal.py update <task_id> <status> [notes]")
            sys.exit(1)
        task_id = int(sys.argv[2])
        status = sys.argv[3]
        notes = sys.argv[4] if len(sys.argv) > 4 else None
        result = legal.update_task_status(task_id, status, notes)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
