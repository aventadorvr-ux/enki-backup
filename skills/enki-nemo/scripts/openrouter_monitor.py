#!/usr/bin/env python3
"""
OPENROUTER CREDIT MONITOR
Tracks token usage and credit balance
Alerts when credit is low
"""

import os
import json
import requests
from datetime import datetime

class OpenRouterMonitor:
    """
    Monitors OpenRouter credit balance and usage
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        # If using OpenAI key with OpenRouter
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY", "")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.low_credit_threshold = 5.0  # Alert when <$5 remaining
        self.critical_threshold = 1.0    # Critical when <$1 remaining
    
    def get_credit_balance(self):
        """Get current credit balance from OpenRouter"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Try to get user info/balance
            response = requests.get(
                f"{self.base_url}/auth/key",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "balance": data.get("data", {}).get("credit", "Unknown"),
                    "usage": data.get("data", {}).get("usage", 0),
                    "raw": data
                }
            else:
                return {
                    "status": "error",
                    "code": response.status_code,
                    "message": response.text
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def check_credit_status(self):
        """Check credit status and alert if low"""
        result = self.get_credit_balance()
        
        if result.get("status") == "success":
            balance = result.get("balance", 0)
            
            # Try to parse balance as float
            try:
                balance_float = float(balance) if balance != "Unknown" else 0
                
                status = "healthy"
                alert_needed = False
                
                if balance_float < self.critical_threshold:
                    status = "CRITICAL"
                    alert_needed = True
                elif balance_float < self.low_credit_threshold:
                    status = "LOW"
                    alert_needed = True
                
                return {
                    "timestamp": datetime.now().isoformat(),
                    "credit_balance": balance,
                    "status": status,
                    "alert_needed": alert_needed,
                    "threshold_low": self.low_credit_threshold,
                    "threshold_critical": self.critical_threshold
                }
            except:
                return {
                    "timestamp": datetime.now().isoformat(),
                    "credit_balance": balance,
                    "status": "unknown",
                    "alert_needed": False
                }
        else:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": result.get("error", "Unknown error"),
                "alert_needed": False
            }
    
    def send_low_credit_alert(self, balance_data):
        """Send ntfy alert for low credit"""
        try:
            topic = "Enki_SystemAlerts"
            url = f"https://ntfy.sh/{topic}"
            
            balance = balance_data.get("credit_balance", "Unknown")
            status = balance_data.get("status", "UNKNOWN")
            
            headers = {
                "Title": f"⚠️ OPENROUTER CREDIT {status}",
                "Priority": "4",  # High priority
                "Tags": "warning,money"
            }
            
            message = f"""OpenRouter Credit Alert

Status: {status}
Balance: ${balance}

Action: Top up credits immediately to avoid service interruption.

Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S NZT")}"""
            
            requests.post(url, data=message, headers=headers, timeout=10)
            print(f"[ALERT] Low credit notification sent to ntfy")
            
        except Exception as e:
            print(f"[ALERT] Failed to send notification: {e}")
    
    def log_check(self, result):
        """Log credit check to file"""
        log_entry = {
            "timestamp": result.get("timestamp"),
            "balance": result.get("credit_balance"),
            "status": result.get("status")
        }
        
        with open("/home/ubuntu/enki-agentic/data/openrouter_credits.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")


def monitor_credits():
    """Main monitoring function - run via cron every hour"""
    monitor = OpenRouterMonitor()
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking OpenRouter credits...")
    
    result = monitor.check_credit_status()
    
    print(f"Balance: {result.get('credit_balance', 'Unknown')}")
    print(f"Status: {result.get('status', 'Unknown')}")
    
    # Log the check
    monitor.log_check(result)
    
    # Send alert if needed
    if result.get("alert_needed"):
        monitor.send_low_credit_alert(result)
        print("🚨 LOW CREDIT ALERT SENT!")
    
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        result = monitor_credits()
        print(json.dumps(result, indent=2))
    else:
        print("OpenRouter Credit Monitor")
        print("Usage: python3 openrouter_monitor.py check")
        print("")
        print("Environment variables needed:")
        print("  OPENROUTER_API_KEY or OPENAI_API_KEY")
        print("")
        print("Will check credit balance and alert if low.")
