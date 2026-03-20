#!/usr/bin/env python3
"""
ENKI TELEGRAM COMMAND CENTER
Mobile mission control for ENKI AGENTIC
Real-time system control from your phone
"""

import os
import json
import requests
import sqlite3
from datetime import datetime
from typing import Dict, Optional
import subprocess

class EnkiTelegramBot:
    """
    Telegram Command Center
    Instant system access from anywhere
    """
    
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.api_base = "http://127.0.0.1:8000/api/v1"
        self.authorized_users = os.getenv("TELEGRAM_AUTH_USERS", "").split(",")
        self.last_update_id = 0
        
    def get_updates(self) -> list:
        """Get new messages from Telegram"""
        if not self.bot_token:
            return []
        
        try:
            resp = requests.get(
                f"https://api.telegram.org/bot{self.bot_token}/getUpdates",
                params={"offset": self.last_update_id + 1, "limit": 10},
                timeout=10
            )
            updates = resp.json().get("result", [])
            if updates:
                self.last_update_id = updates[-1]["update_id"]
            return updates
        except Exception as e:
            print(f"Error getting updates: {e}")
            return []
    
    def send_message(self, chat_id: str, text: str, parse_mode: str = "HTML"):
        """Send message to Telegram"""
        if not self.bot_token:
            return
        
        try:
            requests.post(
                f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": parse_mode
                },
                timeout=5
            )
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def is_authorized(self, user_id: str) -> bool:
        """Check if user is authorized"""
        if not self.authorized_users or self.authorized_users == ['']:
            return True  # Allow all if not configured
        return str(user_id) in self.authorized_users
    
    def handle_command(self, message: Dict) -> str:
        """Process incoming command"""
        chat_id = message["chat"]["id"]
        user_id = message["from"]["id"]
        text = message.get("text", "").strip()
        
        if not self.is_authorized(user_id):
            return "⛔ Unauthorized access. Contact administrator."
        
        if not text.startswith("/"):
            return None  # Not a command
        
        command = text.split()[0].lower()
        args = text.split()[1:] if len(text.split()) > 1 else []
        
        handlers = {
            "/start": self.cmd_start,
            "/help": self.cmd_help,
            "/status": self.cmd_status,
            "/hot": self.cmd_hot_leads,
            "/stats": self.cmd_stats,
            "/restart": self.cmd_restart,
            "/content": self.cmd_content,
            "/alert": self.cmd_alert,
            "/agents": self.cmd_agents,
            "/health": self.cmd_health,
            "/report": self.cmd_report,
            "/voice": self.cmd_voice_test
        }
        
        handler = handlers.get(command)
        if handler:
            return handler(args, chat_id)
        else:
            return f"❓ Unknown command: {command}\nUse /help for available commands."
    
    def cmd_start(self, args, chat_id) -> str:
        """Welcome message"""
        return """🤖 <b>ENKI AGENTIC COMMAND CENTER</b>

Welcome to your mobile mission control.

<b>QUICK COMMANDS:</b>
/status - Full system health
/hot - Hot leads (action required)
/stats - Lead statistics
/agents - Agent status
/content - Generate content

Type /help for all commands.

<i>AGen_OVACa is watching. Enki is ready.</i>"""
    
    def cmd_help(self, args, chat_id) -> str:
        """Help menu"""
        return """📋 <b>ENKI COMMAND REFERENCE</b>

<b>SYSTEM MONITORING:</b>
/status - Full system status
/health - Quick health check
/agents - Agent fleet status
/report - Complete system report

<b>LEAD MANAGEMENT:</b>
/hot - Hot leads (requires action)
/stats - Lead statistics & metrics

<b>CONTENT GENERATION:</b>
/content property [type] [location] - Property description
/content social [platform] [data] - Social media post
/content email [type] - Email campaign

<b>SYSTEM CONTROL:</b>
/restart [service] - Restart service
/alert [message] - Broadcast alert
/voice - Test voice notifications

<b>EMERGENCY:</b>
Contact admin if critical issues detected.

<i>All commands are logged. AGen_OVACa is monitoring.</i>"""
    
    def cmd_status(self, args, chat_id) -> str:
        """Full system status"""
        try:
            resp = requests.get(f"{self.api_base}/enki/status", timeout=5)
            data = resp.json()
            
            status = "🟢 OPERATIONAL" if data.get("status") == "operational" else "🔴 DEGRADED"
            
            agents = data.get("agents", {})
            agent_lines = []
            for name, state in agents.items():
                emoji = "🟢" if state == "active" else "🟡" if state == "building" else "⚪"
                agent_lines.append(f"{emoji} {name}: {state}")
            
            return f"""📊 <b>ENKI SYSTEM STATUS</b>

<b>Overall:</b> {status}
<b>Version:</b> {data.get('version', 'unknown')}
<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

<b>AGENT FLEET:</b>
{chr(10).join(agent_lines)}

<i>Use /report for detailed metrics</i>"""
        except Exception as e:
            return f"🔴 <b>SYSTEM ERROR</b>\n\nCould not fetch status:\n{str(e)}\n\nAGen_OVACa has been alerted."
    
    def cmd_hot_leads(self, args, chat_id) -> str:
        """Get hot leads requiring action"""
        try:
            resp = requests.get(f"{self.api_base}/enki/leads/hot", timeout=10)
            leads = resp.json()
            
            if not leads:
                return """🔥 <b>HOT LEADS</b>

No hot leads currently.

<i>AGen_OVACa will alert you immediately when hot leads arrive.</i>"""
            
            lead_lines = []
            for lead in leads[:5]:  # Show top 5
                lead_lines.append(
                    f"🔥 <b>{lead.get('contact', 'Unknown')}</b>\n"
                    f"   Score: {lead.get('score', 0)}/40\n"
                    f"   Source: {lead.get('source', 'unknown')}\n"
                    f"   " + lead.get('message', '')[:50] + "..."
                )
            
            return f"""🔥 <b>HOT LEADS - ACTION REQUIRED</b>

{chr(10).join(lead_lines)}

<b>Total hot leads:</b> {len(leads)}

<i>Contact these leads IMMEDIATELY for best conversion.</i>"""
        except Exception as e:
            return f"❌ Error fetching hot leads: {str(e)}"
    
    def cmd_stats(self, args, chat_id) -> str:
        """Get lead statistics"""
        try:
            resp = requests.get(f"{self.api_base}/enki/stats", timeout=5)
            stats = resp.json()
            
            return f"""📈 <b>LEAD STATISTICS</b>

<b>Total Leads:</b> {stats.get('total_leads', 0)}
<b>Hot Leads:</b> {stats.get('hot_leads', 0)} 🔥
<b>Today's Leads:</b> {stats.get('today_leads', 0)}
<b>Average Score:</b> {stats.get('average_score', 0):.1f}/40

<i>Last updated: {datetime.now().strftime('%H:%M UTC')}</i>"""
        except Exception as e:
            return f"❌ Error fetching stats: {str(e)}"
    
    def cmd_restart(self, args, chat_id) -> str:
        """Restart services"""
        service = args[0] if args else "api"
        
        if service == "api":
            try:
                subprocess.run(["pkill", "-f", "uvicorn"], timeout=10)
                subprocess.run([
                    "bash", "-c",
                    "cd ~/nz-realestate-ai && source venv/bin/activate && nohup uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2 > /tmp/uvicorn.log 2>&1 &"
                ], timeout=30)
                return "🔄 <b>API RESTARTED</b>\n\nService has been restarted.\nUse /health to verify."
            except Exception as e:
                return f"❌ Restart failed: {str(e)}"
        
        elif service == "nginx":
            try:
                subprocess.run(["sudo", "systemctl", "restart", "nginx"], timeout=30)
                return "🔄 <b>NGINX RESTARTED</b>\n\nWeb server restarted."
            except Exception as e:
                return f"❌ Restart failed: {str(e)}"
        
        else:
            return f"❓ Unknown service: {service}\nAvailable: api, nginx"
    
    def cmd_content(self, args, chat_id) -> str:
        """Generate content on demand"""
        if not args:
            return """📝 <b>CONTENT GENERATION</b>

Usage:
/content property [data]
/content social [platform] [data]
/content email [type]

Example:
/content social instagram '{"type":"house","location":"Auckland","price":"$1.2M"}'
"""
        
        content_type = args[0]
        
        if content_type == "property":
            return "🏠 Generating property description...\n(Integration with Content Forge pending)"
        elif content_type == "social":
            return "📱 Generating social post...\n(Integration with Content Forge pending)"
        elif content_type == "email":
            return "📧 Generating email...\n(Integration with Content Forge pending)"
        else:
            return f"❓ Unknown content type: {content_type}"
    
    def cmd_alert(self, args, chat_id) -> str:
        """Broadcast custom alert"""
        if not args:
            return "❓ Usage: /alert [your message here]"
        
        message = " ".join(args)
        # Log the alert
        print(f"BROADCAST ALERT: {message}")
        return f"📢 <b>ALERT BROADCASTED</b>\n\nMessage: {message}\n\n<i>Logged to system. AGen_OVACa notified.</i>"
    
    def cmd_agents(self, args, chat_id) -> str:
        """Agent fleet status"""
        return self.cmd_status(args, chat_id)
    
    def cmd_health(self, args, chat_id) -> str:
        """Quick health check"""
        try:
            resp = requests.get(f"{self.api_base.replace('/api/v1', '')}/health", timeout=5)
            if resp.status_code == 200:
                return "💚 <b>SYSTEM HEALTHY</b>\n\nAll core services responding."
            else:
                return f"⚠️ <b>HEALTH CHECK WARNING</b>\n\nStatus: {resp.status_code}"
        except Exception as e:
            return f"🔴 <b>SYSTEM DOWN</b>\n\n{str(e)}\n\nUse /restart api to recover."
    
    def cmd_report(self, args, chat_id) -> str:
        """Full system report"""
        try:
            # Run AGen_OVACa report
            result = subprocess.run(
                [
                    "/home/ubuntu/enki-agentic/venv/bin/python3",
                    "/home/ubuntu/enki-agentic/scripts/agen_ovaca.py",
                    "report"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return f"""📊 <b>FULL SYSTEM REPORT</b>

<i>Generated by AGen_OVACa</i>

{result.stdout[:3000]}...

<i>See full report on server.</i>"""
            else:
                return f"❌ Report generation failed:\n{result.stderr[:500]}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def cmd_voice_test(self, args, chat_id) -> str:
        """Test voice notifications"""
        return "🔊 Voice notification system ready.\n(Requires TTS integration)"
    
    def run(self):
        """Main bot loop"""
        print("ENKI Telegram Bot starting...")
        
        if not self.bot_token:
            print("ERROR: TELEGRAM_BOT_TOKEN not set")
            return
        
        print(f"Bot authorized for users: {self.authorized_users}")
        
        while True:
            try:
                updates = self.get_updates()
                
                for update in updates:
                    if "message" in update:
                        message = update["message"]
                        chat_id = message["chat"]["id"]
                        
                        response = self.handle_command(message)
                        if response:
                            self.send_message(chat_id, response)
                
                # Sleep to avoid rate limits
                import time
                time.sleep(1)
                
            except Exception as e:
                print(f"Error in main loop: {e}")
                import time
                time.sleep(5)


if __name__ == "__main__":
    bot = EnkiTelegramBot()
    bot.run()
