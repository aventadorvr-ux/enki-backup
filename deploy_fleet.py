#!/usr/bin/env python3
"""
AGENT FLEET DEPLOYMENT SCRIPT
Deploys all 4 agents: AGen_OVAWatch, Lead_Terminator, Content_Forge, AGen_Legal
"""

import os
import sys
import subprocess
import json
from datetime import datetime

# Set up environment for local paths
DATA_DIR = "/data/data/com.termux/files/home/.openclaw/workspace/data/agents"
os.makedirs(DATA_DIR, exist_ok=True)
os.environ["NEMO_DB"] = f"{DATA_DIR}/leads.db"
os.environ["ENKI_DATA"] = DATA_DIR

AGENTS = {
    "AGen_OVAWatch": {
        "script": "ovawatch_agen.py",
        "db": "overseer.db",
        "desc": "Overseer - Monitors all agents and system health"
    },
    "Lead_Terminator": {
        "script": "lead_terminator.py",
        "db": "leads.db",
        "desc": "Lead Qualification - AI-powered lead scoring and conversation"
    },
    "Content_Forge": {
        "script": "content_forge.py",
        "db": "content.db",
        "desc": "Marketing Content - Property descriptions, social posts, emails"
    },
    "AGen_Legal": {
        "script": "agen_legal.py",
        "db": "legal.db",
        "desc": "Legal & Compliance - Business setup, contracts, regulatory"
    }
}

SCRIPT_DIR = "/data/data/com.termux/files/home/.openclaw/workspace/skills/enki-nemo/scripts"

def deploy_agent(name, config):
    """Deploy a single agent"""
    result = {
        "agent": name,
        "status": "unknown",
        "timestamp": datetime.now().isoformat(),
        "errors": []
    }
    
    script_path = os.path.join(SCRIPT_DIR, config["script"])
    
    # Check if script exists
    if not os.path.exists(script_path):
        result["status"] = "error"
        result["errors"].append(f"Script not found: {script_path}")
        return result
    
    # Test agent with stats/check command
    try:
        if name == "AGen_OVAWatch":
            cmd = ["python3", script_path, "check"]
        elif name == "Lead_Terminator":
            cmd = ["python3", script_path, "stats"]
        elif name == "Content_Forge":
            cmd = ["python3", script_path, "templates"]
        elif name == "AGen_Legal":
            cmd = ["python3", script_path, "checklist"]
        else:
            cmd = ["python3", script_path]
        
        env = os.environ.copy()
        env["NEMO_DB"] = f"{DATA_DIR}/leads.db"
        
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
            cwd=SCRIPT_DIR
        )
        
        if proc.returncode == 0:
            result["status"] = "active"
            try:
                result["data"] = json.loads(proc.stdout)
            except:
                result["output"] = proc.stdout[:500]
        else:
            result["status"] = "error"
            result["errors"].append(proc.stderr[:500])
            
    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["errors"].append("Agent startup timed out")
    except Exception as e:
        result["status"] = "error"
        result["errors"].append(str(e))
    
    return result

def main():
    print("=" * 60)
    print("ENKI AGENT FLEET DEPLOYMENT")
    print("=" * 60)
    print(f"Data Directory: {DATA_DIR}")
    print(f"Time: {datetime.now().isoformat()}")
    print()
    
    results = {}
    active_count = 0
    
    for name, config in AGENTS.items():
        print(f"\n🚀 Deploying {name}...")
        print(f"   Purpose: {config['desc']}")
        
        result = deploy_agent(name, config)
        results[name] = result
        
        if result["status"] == "active":
            print(f"   ✅ ACTIVE")
            active_count += 1
        else:
            print(f"   ❌ {result['status'].upper()}")
            if result["errors"]:
                for err in result["errors"]:
                    print(f"      Error: {err}")
    
    print("\n" + "=" * 60)
    print("DEPLOYMENT SUMMARY")
    print("=" * 60)
    print(f"Total Agents: {len(AGENTS)}")
    print(f"Active: {active_count}")
    print(f"Failed: {len(AGENTS) - active_count}")
    
    # Save deployment report
    report_path = f"{DATA_DIR}/deployment_report.json"
    with open(report_path, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_agents": len(AGENTS),
            "active_count": active_count,
            "results": results
        }, f, indent=2)
    
    print(f"\nReport saved: {report_path}")
    
    return active_count == len(AGENTS)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
