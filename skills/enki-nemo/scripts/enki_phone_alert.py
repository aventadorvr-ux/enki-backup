#!/usr/bin/env python3
"""
ENKI PHONE ALERT SYSTEM
Critical outage notifications via phone call + SMS
Guaranteed wake-up for system failures
Phone: +6421777516
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List

class EnkiPhoneAlert:
    """
    Phone Alert System - Wakes you up when ENKI goes down
    Uses Twilio for calls and SMS
    """
    
    def __init__(self):
        self.phone_number = "+6421777516"  # Your NZ number
        self.twilio_sid = os.getenv("TWILIO_SID", "")
        self.twilio_token = os.getenv("TWILIO_TOKEN", "")
        self.twilio_phone = os.getenv("TWILIO_PHONE", "")  # Twilio assigned number
        
    def send_critical_phone_alert(self, message: str, system_status: Dict):
        """Send phone call + SMS for critical outages"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S NZT")
        
        # Build alert message
        alert_text = f"""
🚨 ENKI SYSTEM CRITICAL ALERT 🚨

Time: {timestamp}
Phone: {self.phone_number}

STATUS: {system_status.get('overall_status', 'UNKNOWN').upper()}

ISSUES:
{chr(10).join(['• ' + issue for issue in system_status.get('issues', ['Unknown error'])])}

AGen_OVAWatch is attempting auto-repair.

Check system: http://3.25.170.226:3000

This is an automated alert.
Reply STOP to opt out (not recommended).
"""
        
        # 1. Send SMS (instant delivery)
        self._send_sms(alert_text)
        
        # 2. Place phone call (guaranteed wake-up)
        self._make_phone_call(system_status)
        
        # 3. Log the alert
        self._log_alert(timestamp, system_status)
        
        return {"status": "sent", "phone": self.phone_number, "timestamp": timestamp}
    
    def _send_sms(self, message: str):
        """Send SMS via Twilio"""
        if not all([self.twilio_sid, self.twilio_token, self.twilio_phone]):
            print(f"[SMS Would Send] To: {self.phone_number}")
            print(f"Message: {message[:100]}...")
            return
        
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_sid}/Messages.json"
            
            response = requests.post(
                url,
                auth=(self.twilio_sid, self.twilio_token),
                data={
                    "From": self.twilio_phone,
                    "To": self.phone_number,
                    "Body": message
                },
                timeout=10
            )
            
            if response.status_code == 201:
                print(f"✅ SMS sent to {self.phone_number}")
            else:
                print(f"❌ SMS failed: {response.text}")
                
        except Exception as e:
            print(f"❌ SMS error: {e}")
    
    def _make_phone_call(self, system_status: Dict):
        """Place phone call via Twilio"""
        if not all([self.twilio_sid, self.twilio_token, self.twilio_phone]):
            print(f"[CALL Would Place] To: {self.phone_number}")
            return
        
        try:
            # TwiML for the call - speaks the alert
            twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">
        Emergency alert from ENKI Agentic. 
        System status is {system_status.get('overall_status', 'critical')}.
        Please check your phone for details.
        I repeat, ENKI system requires your attention.
    </Say>
    <Pause length="2"/>
    <Say voice="alice">
        This call will repeat in 5 minutes if not acknowledged.
    </Say>
</Response>"""
            
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_sid}/Calls.json"
            
            response = requests.post(
                url,
                auth=(self.twilio_sid, self.twilio_token),
                data={
                    "From": self.twilio_phone,
                    "To": self.phone_number,
                    "Twiml": twiml,
                    "Timeout": 30
                },
                timeout=10
            )
            
            if response.status_code == 201:
                print(f"✅ Phone call placed to {self.phone_number}")
            else:
                print(f"❌ Call failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Call error: {e}")
    
    def _log_alert(self, timestamp: str, system_status: Dict):
        """Log alert to file"""
        log_entry = {
            "timestamp": timestamp,
            "phone": self.phone_number,
            "status": system_status.get('overall_status'),
            "issues": system_status.get('issues', [])
        }
        
        with open("/var/log/enki-phone-alerts.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def test_alert(self):
        """Test the phone alert system"""
        test_status = {
            "overall_status": "TEST",
            "issues": ["This is a test alert"],
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"🧪 TESTING PHONE ALERT SYSTEM")
        print(f"📱 Target: {self.phone_number}")
        print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
        print("")
        
        result = self.send_critical_phone_alert("TEST ALERT", test_status)
        
        print(f"\n✅ Test complete. Check your phone.")
        return result


# Integration with AGen_OVAWatch
def send_phone_alert_on_critical(system_status: Dict):
    """Called by AGen_OVAWatch when critical issues detected"""
    alert = EnkiPhoneAlert()
    return alert.send_critical_phone_alert("CRITICAL SYSTEM FAILURE", system_status)


if __name__ == "__main__":
    import sys
    
    alert = EnkiPhoneAlert()
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        alert.test_alert()
    else:
        print("ENKI Phone Alert System")
        print(f"Configured for: {alert.phone_number}")
        print("\nRun: python3 enki_phone_alert.py test")
