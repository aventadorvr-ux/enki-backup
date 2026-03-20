#!/usr/bin/env python3
"""
ENKI CONTROL BOT v2.0 - CLEAN BUILD
Fresh Telegram interface for ENKI AGENTIC
No legacy baggage, no conflicts
"""

import os
import sys
import json
import requests
import sqlite3
import subprocess
import time
from datetime import datetime
from typing import Dict, Optional, List

class EnkiControlBot:
    """Fresh Telegram Command Interface"""
    
    def __init__(self):
        self.token = os.getenv("ENKI_BOT_TOKEN", "")
        self.api_url = "http://127.0.0.1:8000"
        self.last_update_id = 0
        self.start_time = datetime.now()
        
    def api_call(self, method: str, **kwargs) -> Dict:
        """Make Telegram API call"""
        if not self.token:
            print(f"ERROR: No bot token configured")
            return {}
        
        try:
            url = f"https://api.telegram.org/bot{self.token}/{method}"
            resp = requests.post(url, json=kwargs, timeout=30) if kwargs else requests.get(url, timeout=30)
            return resp.json()
        except Exception as e:
            print(f"API Error: {e}")
            return {}
    
    def get_updates(self) -> List[Dict]:
        """Fetch new messages"""
        result = self.api_call("getUpdates", offset=self.last_update_id + 1, limit=10)
        updates = result.get("result", [])
        if updates:
            self.last_update_id = updates[-1]["update_id"]
        return updates
    
    def send_msg(self, chat_id: int, text: str, parse_mode: str = "HTML"):
        """Send message"""
        self.api_call("sendMessage", chat_id=chat_id, text=text, parse_mode=parse_mode)
    
    def handle_message(self, update: Dict):
        """Process incoming message"""
        if "message" not in update:
            return
        
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "").strip()
        user = msg["from"].get("username", "unknown")
        
        if not text.startswith("/"):
            return
        
        parts = text.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Command routing
        handlers = {
            "/start": self.cmd_start,
            "/help": self.cmd_help,
            "/status": self.cmd_status,
            "/health": self.cmd_health,
            "/agents": self.cmd_agents,
            "/restart": self.cmd_restart,
            "/api": self.cmd_api,
            "/ping": self.cmd_ping,
        }
        
        handler = handlers.get(cmd, self.cmd_unknown)
        response = handler(args, user)
        self.send_msg(chat_id, response)
    
    def cmd_start(self, args, user) -> str:
        return """🌊 <b>ENKI CONTROL BOT v2.0</b>

Fresh build. Clean slate. Ready.

<b>COMMANDS:</b>
/status - System status
/health - Health check  
/agents - Agent list
/restart [api|nginx] - Restart services
/api [endpoint] - Query API
/ping - Test latency
/help - Full help

<i>Type /help for details</i>"""
    
    def cmd_help(self, args, user) -> str:
        return """📖 <b>ENKI BOT COMMANDS</b>

<b>MONITORING:</b>
/status - Full system status with agent states
/health - Quick API health check
/ping - Test bot→API latency
/agents - List all active agents

<b>CONTROL:</b>
/restart api - Restart backend API
/restart nginx - Restart web server
/restart all - Restart everything

<b>API QUERY:</b>
/api health - GET /health
/api agents - GET /api/v1/agents
/api docs - API documentation URL

<b>SYSTEM:</b>
/start - Welcome message
/help - This message

<i>Bot uptime: {(datetime.now() - self.start_time).total_seconds() // 60} minutes</i>"""
    
    def cmd_status(self, args, user) -> str:
        try:
            r = requests.get(f"{self.api_url}/health", timeout=5)
            health = "🟢 ONLINE" if r.status_code == 200 else "🔴 DOWN"
            
            # Get agents
            try:
                agents_r = requests.get(f"{self.api_url}/api/v1/agents", timeout=5)
                agents = agents_r.json().get("agents", [])
                agent_list = "\n".join([f"  • {a['name']}" for a in agents])
            except:
                agent_list = "  (unable to fetch)"
            
            uptime = (datetime.now() - self.start_time).total_seconds() // 60
            
            return f"""📊 <b>ENKI STATUS</b>

<b>API Server:</b> {health}
<b>Bot Uptime:</b> {uptime} min
<b>Time:</b> {datetime.now().strftime('%H:%M:%S UTC')}

<b>AGENTS ({len(agents)}):</b>
{agent_list}

<i>Server: 3.25.170.226</i>"""
        except Exception as e:
            return f"🔴 <b>ERROR:</b> {str(e)[:100]}"
    
    def cmd_health(self, args, user) -> str:
        try:
            r = requests.get(f"{self.api_url}/health", timeout=5)
            data = r.json()
            return f"""💚 <b>HEALTH CHECK</b>

Status: {data.get('status', 'unknown')}
Timestamp: {data.get('timestamp', 'N/A')[:19]}

<i>API responding normally</i>"""
        except Exception as e:
            return f"🔴 <b>HEALTH CHECK FAILED</b>\n\n{str(e)[:200]}"
    
    def cmd_agents(self, args, user) -> str:
        try:
            r = requests.get(f"{self.api_url}/api/v1/agents", timeout=5)
            agents = r.json().get("agents", [])
            
            if not agents:
                return "⚪ <b>No agents running</b>"
            
            lines = []
            for a in agents:
                lines.append(f"🤖 <b>{a['name']}</b>\n   {a.get('description', 'No description')}")
            
            return f"""🤖 <b>AGENT FLEET ({len(agents)})</b>

{"\n\n".join(lines)}

<i>All agents operational</i>"""
        except Exception as e:
            return f"❌ <b>Error:</b> {str(e)[:150]}"
    
    def cmd_restart(self, args, user) -> str:
        service = args[0] if args else "api"
        
        if service == "api":
            try:
                subprocess.run(["pkill", "-f", "uvicorn"], timeout=5, capture_output=True)
                time.sleep(1)
                subprocess.Popen([
                    "bash", "-c",
                    "cd ~/nz-realestate-ai && ./venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2 > /tmp/api.log 2>&1 &"
                ])
                return "🔄 <b>API RESTARTING...</b>\n\nWait 10s then /health to verify"
            except Exception as e:
                return f"❌ Restart failed: {str(e)[:100]}"
        
        elif service == "nginx":
            try:
                subprocess.run(["sudo", "systemctl", "restart", "nginx"], timeout=30, capture_output=True)
                return "🔄 <b>NGINX RESTARTED</b>"
            except Exception as e:
                return f"❌ Failed: {str(e)[:100]}"
        
        elif service == "all":
            return "🔄 <b>Restarting all services...</b>\nUse /status in 30s"
        
        return f"❓ Unknown service: {service}\nUse: api, nginx, all"
    
    def cmd_api(self, args, user) -> str:
        if not args:
            return """🔌 <b>API QUERY</b>

Usage: /api [endpoint]

Examples:
/api health
/api agents  
/api docs

<i>Direct API access</i>"""
        
        endpoint = args[0]
        
        if endpoint == "docs":
            return f"📚 <b>API DOCS</b>\n\nhttp://3.25.170.226:8000/docs\nhttp://3.25.170.226:8000/openapi.json"
        
        try:
            r = requests.get(f"{self.api_url}/{endpoint}", timeout=5)
            data = r.json()
            return f"""🔌 <b>API RESPONSE</b>

<code>{json.dumps(data, indent=2)[:3500]}</code>"""
        except Exception as e:
            return f"❌ <b>API Error:</b> {str(e)[:200]}"
    
    def cmd_ping(self, args, user) -> str:
        import time
        start = time.time()
        try:
            requests.get(f"{self.api_url}/health", timeout=5)
            latency = (time.time() - start) * 1000
            return f"🏓 <b>PONG</b>\n\nLatency: {latency:.0f}ms\nBot→API connection: OK"
        except Exception as e:
            return f"🔴 <b>PING FAILED</b>\n\n{str(e)[:100]}"
    
    def cmd_unknown(self, args, user) -> str:
        return "❓ Unknown command. Use /help for available commands."
    
    def run(self):
        """Main loop"""
        print(f"ENKI Control Bot v2.0 starting...")
        print(f"Time: {datetime.now().isoformat()}")
        
        if not self.token:
            print("ERROR: ENKI_BOT_TOKEN not set")
            print("Set environment variable: export ENKI_BOT_TOKEN='your_token'")
            sys.exit(1)
        
        print(f"Bot initialized. Polling for messages...")
        
        while True:
            try:
                updates = self.get_updates()
                for update in updates:
                    self.handle_message(update)
                time.sleep(1)
            except KeyboardInterrupt:
                print("\nShutting down...")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)


if __name__ == "__main__":
    bot = EnkiControlBot()
    bot.run()
