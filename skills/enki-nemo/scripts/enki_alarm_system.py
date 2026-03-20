#!/usr/bin/env python3
"""
ENKI ALARM SYSTEM - CRITICAL ALERT PROTOCOL
Maximum priority alerts for system failures
Never sleep when ENKI is down
"""

import os
import json
import requests
import sqlite3
import subprocess
import time
from datetime import datetime
from typing import Dict, List
import sys

class EnkiAlarmSystem:
    """
    The Alarm System - Wakes you up when things break
    Multiple escalation levels, maximum urgency
    """
    
    def __init__(self):
        self.telegram_bot = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.telegram_chat = os.getenv("TELEGRAM_CHAT_ID", "")
        self.emergency_contact = os.getenv("EMERGENCY_PHONE", "")  # For future SMS integration
        
        # Alert cooldowns (prevent spam)
        self.last_alert = {}
        self.escalation_level = 0
        
        # Critical services to monitor
        self.critical_services = {
            "enki_api": {"url": "http://127.0.0.1:8000/health", "method": "GET"},
            "nginx": {"check": "systemctl is-active nginx", "type": "command"},
            "database": {"check": "ls /home/ubuntu/enki-agentic/data/leads.db", "type": "file"},
            "lead_terminator": {"script": "/home/ubuntu/enki-agentic/scripts/lead_terminator.py stats", "type": "script"}
        }
    
    def send_critical_alert(self, message: str, level: str = "CRITICAL"):
        """Send maximum priority alert to all channels"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        alert_text = f"""🚨🚨🚨 ENKI {level} ALERT 🚨🚨🚨

⏰ {timestamp}

{message}

⚡ ACTION REQUIRED IMMEDIATELY ⚡

AGen_OVAWatch is attempting auto-repair.
Check system at: http://3.25.170.226:3000

Reply /status for current state.
Reply /restart to attempt recovery."""
        
        print(f"\n{'='*60}")
        print(alert_text)
        print(f"{'='*60}\n")
        
        # 1. Telegram Alert (Primary)
        if self.telegram_bot and self.telegram_chat:
            try:
                # Send with sound notification
                requests.post(
                    f"https://api.telegram.org/bot{self.telegram_bot}/sendMessage",
                    json={
                        "chat_id": self.telegram_chat,
                        "text": alert_text,
                        "parse_mode": "HTML",
                        "disable_notification": False  # Force sound
                    },
                    timeout=10
                )
                
                # Send second message to ensure sound (Telegram sometimes batches)
                requests.post(
                    f"https://api.telegram.org/bot{self.telegram_bot}/sendMessage",
                    json={
                        "chat_id": self.telegram_chat,
                        "text": "🔔🔔🔔 WAKE UP - SYSTEM DOWN 🔔🔔🔔",
                        "disable_notification": False
                    },
                    timeout=10
                )
                
                print("✅ Telegram alerts sent with sound")
            except Exception as e:
                print(f"❌ Telegram failed: {e}")
        
        # 2. Log to emergency log
        self._log_emergency(timestamp, level, message)
        
        # 3. Play audible alarm (if running locally with speakers)
        self._play_audible_alarm()
    
    def _log_emergency(self, timestamp: str, level: str, message: str):
        """Log emergency to file"""
        log_entry = f"[{timestamp}] {level}: {message}\n"
        with open("/var/log/enki-emergency.log", "a") as f:
            f.write(log_entry)
    
    def _play_audible_alarm(self):
        """Play audible alarm sound"""
        try:
            # Try to play beep or alarm sound
            # This will work if the server has speakers (unlikely on EC2)
            # But serves as documentation of intent
            os.system("echo -e '\a'")  # Terminal bell
        except:
            pass
    
    def check_critical_systems(self) -> Dict:
        """Check all critical systems"""
        failures = []
        
        # Check ENKI API
        try:
            resp = requests.get("http://127.0.0.1:8000/health", timeout=5)
            if resp.status_code != 200:
                failures.append("ENKI API returning HTTP errors")
        except Exception as e:
            failures.append(f"ENKI API DOWN: {str(e)}")
        
        # Check nginx
        try:
            result = subprocess.run(
                ["systemctl", "is-active", "nginx"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout.strip() != "active":
                failures.append("nginx web server DOWN")
        except Exception as e:
            failures.append(f"nginx check failed: {e}")
        
        # Check database
        try:
            if not os.path.exists("/home/ubuntu/enki-agentic/data/leads.db"):
                failures.append("Database file missing")
        except Exception as e:
            failures.append(f"Database check failed: {e}")
        
        # Check disk space
        try:
            result = subprocess.run(
                ["df", "/"],
                capture_output=True,
                text=True
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                usage = lines[1].split()
                if len(usage) > 4:
                    percent = int(usage[4].replace('%', ''))
                    if percent > 90:
                        failures.append(f"CRITICAL: Disk space {percent}% full")
        except:
            pass
        
        # Check memory
        try:
            result = subprocess.run(
                ["free"],
                capture_output=True,
                text=True
            )
            # Parse memory usage
        except:
            pass
        
        return {
            "timestamp": datetime.now().isoformat(),
            "failures": failures,
            "status": "CRITICAL" if failures else "HEALTHY"
        }
    
    def emergency_monitor(self):
        """Continuous emergency monitoring - NEVER STOPS"""
        print("🔔 ENKI ALARM SYSTEM ACTIVATED")
        print("Monitoring critical systems every 30 seconds...")
        print("Press Ctrl+C to stop (DON'T STOP IN PRODUCTION)\n")
        
        while True:
            try:
                result = self.check_critical_systems()
                
                if result["failures"]:
                    # DEDUPLICATE: Don't spam same alert within 5 minutes
                    alert_key = result["failures"][0][:50]
                    now = time.time()
                    
                    if alert_key in self.last_alert:
                        if now - self.last_alert[alert_key] < 300:  # 5 min cooldown
                            time.sleep(30)
                            continue
                    
                    self.last_alert[alert_key] = now
                    
                    # BUILD ALERT MESSAGE
                    message = "CRITICAL SYSTEM FAILURES:\n\n"
                    for failure in result["failures"]:
                        message += f"❌ {failure}\n"
                    
                    message += f"\n🤖 AGen_OVAWatch attempting auto-repair..."
                    
                    # SEND MAXIMUM PRIORITY ALERT
                    self.send_critical_alert(message, "CRITICAL")
                    
                    # AUTO-ATTEMPT REPAIR
                    self._emergency_repair()
                
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] All systems healthy")
                
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                print("\n⚠️ Alarm system stopped")
                break
            except Exception as e:
                print(f"Alarm error: {e}")
                time.sleep(30)
    
    def _emergency_repair(self):
        """Attempt emergency repairs"""
        repairs = []
        
        print("Attempting emergency repairs...")
        
        # Restart nginx
        try:
            subprocess.run(["sudo", "systemctl", "restart", "nginx"], timeout=30)
            repairs.append("nginx restarted")
        except:
            pass
        
        # Restart API
        try:
            subprocess.run(["pkill", "-f", "uvicorn"], timeout=10)
            time.sleep(2)
            subprocess.run([
                "bash", "-c",
                "cd ~/nz-realestate-ai && source venv/bin/activate && nohup uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2 > /tmp/uvicorn.log 2>&1 &"
            ], timeout=30)
            repairs.append("API restarted")
        except:
            pass
        
        if repairs:
            self.send_critical_alert(
                f"AUTO-REPAIR ATTEMPTED:\n" + "\n".join([f"✅ {r}" for r in repairs]),
                "REPAIR_ATTEMPT"
            )
    
    def test_alert(self):
        """Test the alarm system"""
        self.send_critical_alert(
            "🧪 THIS IS A TEST ALERT\n\n"
            "If you're seeing this, the alarm system is working correctly.\n"
            "In a real emergency, you would receive this when systems go down.",
            "TEST"
        )
        print("\n✅ Test alert sent. Check your phone.")


if __name__ == "__main__":
    alarm = EnkiAlarmSystem()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            alarm.test_alert()
        elif sys.argv[1] == "monitor":
            alarm.emergency_monitor()
        elif sys.argv[1] == "check":
            result = alarm.check_critical_systems()
            print(json.dumps(result, indent=2))
    else:
        print("Usage: alarm_system.py <command>")
        print("Commands:")
        print("  test    - Send test alert to your phone")
        print("  monitor - Start continuous monitoring (NEVER STOP)")
        print("  check   - One-time system check")
