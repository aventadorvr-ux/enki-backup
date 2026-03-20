#!/usr/bin/env python3
"""
ENKI ntfy ALERT SYSTEM
FREE push notifications with alarm sound
Topic: ntfy.sh/Enki_SystemAlerts
"""

import requests
import json
from datetime import datetime
from typing import Dict

class EnkiNtfyAlert:
    """
    ntfy Alert System - FREE audible alerts for critical outages
    Uses ntfy.sh (open source, free tier)
    """
    
    def __init__(self):
        self.topic = "Enki_SystemAlerts"
        self.base_url = f"https://ntfy.sh/{self.topic}"
        self.phone_number = "+6421777516"  # For reference
    
    def send_critical_alert(self, message: str, system_status: Dict):
        """Send MAXIMUM PRIORITY alert with alarm sound"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S NZT")
        
        # Build notification payload
        title = "🚨 ENKI SYSTEM CRITICAL 🚨"
        
        full_message = f"""{message}

⏰ {timestamp}
📱 {self.phone_number}
Status: {system_status.get('overall_status', 'CRITICAL').upper()}

AGen_OVAWatch attempting auto-repair...
Check: http://3.25.170.226:3000

Reply to acknowledge."""
        
        # ntfy headers for MAXIMUM ALERT
        headers = {
            "Title": title,
            "Priority": "5",  # MAXIMUM (1-5)
            "Tags": "warning,alarm,skull",  # Visual icons
            "Actions": "view, Open Dashboard, http://3.25.170.226:3000",  # Quick action button
        }
        
        try:
            response = requests.post(
                self.base_url,
                data=full_message.encode('utf-8'),
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ ntfy ALERT SENT to {self.topic}")
                print(f"   Status: {response.status_code}")
                return {"status": "sent", "topic": self.topic, "timestamp": timestamp}
            else:
                print(f"❌ ntfy failed: {response.status_code} - {response.text}")
                return {"status": "error", "code": response.status_code}
                
        except Exception as e:
            print(f"❌ ntfy error: {e}")
            return {"status": "error", "error": str(e)}
    
    def test_alert(self):
        """Send test alert to verify setup"""
        test_status = {
            "overall_status": "TEST",
            "issues": ["This is a test of the ENKI alert system"]
        }
        
        print("🧪 SENDING TEST ALERT TO YOUR PHONE...")
        print(f"📱 Topic: {self.topic}")
        print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
        print("")
        print("You should hear an ALARM sound on your phone in 3-5 seconds...")
        print("")
        
        result = self.send_critical_alert(
            "🧪 TEST ALERT - This is a test of the ENKI emergency alert system. If you hear an alarm sound and see this message, everything is configured correctly!",
            test_status
        )
        
        if result.get("status") == "sent":
            print("✅ TEST ALERT SENT SUCCESSFULLY!")
            print("   Check your phone NOW - you should hear an alarm sound!")
        
        return result
    
    def send_recovery_alert(self):
        """Send alert when system recovers"""
        headers = {
            "Title": "✅ ENKI SYSTEM RECOVERED",
            "Priority": "3",  # Normal priority
            "Tags": "white_check_mark",
        }
        
        message = f"System has recovered and is now operational.\nTime: {datetime.now().strftime('%H:%M:%S NZT')}"
        
        try:
            requests.post(
                self.base_url,
                data=message.encode('utf-8'),
                headers=headers,
                timeout=10
            )
            print(f"✅ Recovery alert sent")
        except:
            pass


# Integration with AGen_OVAWatch
def send_ntfy_critical_alert(system_status: Dict):
    """Called by AGen_OVAWatch when critical issues detected"""
    alert = EnkiNtfyAlert()
    
    # Build alert message
    issues_text = "\n".join([f"• {issue}" for issue in system_status.get('issues', ['Unknown error'])])
    
    message = f"""CRITICAL SYSTEM FAILURES DETECTED:

{issues_text}

Immediate action may be required."""
    
    return alert.send_critical_alert(message, system_status)


def send_ntfy_test():
    """Test function"""
    alert = EnkiNtfyAlert()
    return alert.test_alert()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        alert = EnkiNtfyAlert()
        alert.test_alert()
    else:
        print("ENKI ntfy Alert System")
        print(f"Topic: ntfy.sh/Enki_SystemAlerts")
        print(f"Phone: +6421777516")
        print("")
        print("Run: python3 enki_ntfy_alert.py test")
