#!/usr/bin/env python3
"""
Email sender using Mailgun API
Free tier: 5,000 emails/month for 3 months, then 100/day

Setup:
1. Sign up at https://www.mailgun.com/
2. Verify your domain (or use sandbox for testing)
3. Get API key from dashboard
4. Set MAILGUN_API_KEY and MAILGUN_DOMAIN env vars

Usage:
    python3 email_mailgun.py to@example.com "Subject" "Body" [attachment.pdf]
"""

import os
import sys
import base64
import requests

# Configuration
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', '')
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', '')  # e.g., sandbox123.mailgun.org

def send_email_mailgun(to_email, subject, body, attachment_path=None):
    """Send email using Mailgun API."""
    
    if not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
        print("❌ Error: MAILGUN_API_KEY and MAILGUN_DOMAIN must be set")
        print("\n📋 Setup Instructions:")
        print("   1. Sign up at https://www.mailgun.com/ (free tier available)")
        print("   2. Verify your domain OR use the sandbox domain for testing")
        print("   3. Get your API key from the dashboard")
        print("   4. Set environment variables:")
        print("      export MAILGUN_API_KEY='key-xxxxxxxx'")
        print("      export MAILGUN_DOMAIN='sandbox123.mailgun.org'")
        return False
    
    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    
    data = {
        'from': f'Enki Agent <mailgun@{MAILGUN_DOMAIN}>',
        'to': to_email,
        'subject': subject,
        'text': body
    }
    
    files = []
    if attachment_path and os.path.exists(attachment_path):
        filename = os.path.basename(attachment_path)
        files.append(("attachment", (filename, open(attachment_path, 'rb').read())))
        print(f"📎 Attached: {filename}")
    
    try:
        print(f"📤 Sending email via Mailgun ({MAILGUN_DOMAIN})...")
        
        response = requests.post(
            url,
            auth=('api', MAILGUN_API_KEY),
            data=data,
            files=files,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Email sent! ID: {result.get('id', 'N/A')}")
            return True
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config():
    """Show configuration status."""
    print("🔍 Mailgun Configuration")
    print(f"   API Key: {'✅ Set' if MAILGUN_API_KEY else '❌ Not set'}")
    print(f"   Domain: {MAILGUN_DOMAIN if MAILGUN_DOMAIN else '❌ Not set'}")
    if MAILGUN_API_KEY:
        print(f"   Key length: {len(MAILGUN_API_KEY)} chars")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} test              # Show configuration")
        print(f"  {sys.argv[0]} to@email.com 'Subject' 'Body' [attachment.pdf]")
        sys.exit(1)
    
    if sys.argv[1] == "test":
        test_config()
        sys.exit(0)
    
    if len(sys.argv) < 4:
        print("❌ Error: Need at least 3 arguments: to, subject, body")
        sys.exit(1)
    
    to_email = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment = sys.argv[4] if len(sys.argv) > 4 else None
    
    success = send_email_mailgun(to_email, subject, body, attachment)
    sys.exit(0 if success else 1)
