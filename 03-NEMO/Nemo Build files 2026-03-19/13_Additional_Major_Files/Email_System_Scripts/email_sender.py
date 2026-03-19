#!/usr/bin/env python3
"""
Email sender for Enki - SendGrid-based solution for Termux

Setup:
1. Sign up at sendgrid.com (free tier: 100 emails/day)
2. Create API key at https://app.sendgrid.com/settings/api_keys
3. Set environment variable: export SENDGRID_API_KEY='your-key'
   Or edit this file and set API_KEY directly

Usage:
    python3 email_sender.py to@example.com "Subject" "Body text" [attachment.pdf]
    python3 email_sender.py aventadorvr@gmail.com "Test Report" "See attached" RealEstate-AI-Build-Report.pdf
"""

import sys
import os
import base64
import requests
import json
from pathlib import Path

# CONFIGURATION - Set your SendGrid API key here or via environment variable
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
DEFAULT_FROM = os.environ.get('EMAIL_FROM', 'enki-agent@sendgrid.net')

def send_email_sendgrid(to_email, subject, body, attachment_path=None):
    """Send email using SendGrid API via HTTP request."""
    
    if not SENDGRID_API_KEY:
        print("❌ Error: SENDGRID_API_KEY not set")
        print("   Get a free API key at: https://app.sendgrid.com/settings/api_keys")
        print("   Then run: export SENDGRID_API_KEY='your-key'")
        return False
    
    # Build email payload
    data = {
        "personalizations": [{
            "to": [{"email": to_email}],
            "subject": subject
        }],
        "from": {"email": DEFAULT_FROM, "name": "Enki Agent"},
        "content": [{
            "type": "text/plain",
            "value": body
        }]
    }
    
    # Add attachment if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            file_content = f.read()
            encoded = base64.b64encode(file_content).decode('utf-8')
            filename = os.path.basename(attachment_path)
            
            # Determine content type
            content_type = "application/octet-stream"
            if filename.endswith('.pdf'):
                content_type = "application/pdf"
            elif filename.endswith('.txt'):
                content_type = "text/plain"
            elif filename.endswith('.html'):
                content_type = "text/html"
            
            data["attachments"] = [{
                "content": encoded,
                "filename": filename,
                "type": content_type,
                "disposition": "attachment"
            }]
            print(f"📎 Attached: {filename} ({len(file_content)} bytes)")
    
    # Send via SendGrid API
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"📤 Sending email to {to_email}...")
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 202:
            print(f"✅ Email sent successfully!")
            return True
        else:
            print(f"❌ Failed to send email")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def test_without_sending():
    """Test configuration without actually sending."""
    print("🔍 Email Configuration Test")
    print(f"   API Key: {'✅ Set' if SENDGRID_API_KEY else '❌ Not set'}")
    print(f"   From: {DEFAULT_FROM}")
    if SENDGRID_API_KEY:
        print(f"   Key length: {len(SENDGRID_API_KEY)} chars")
        print(f"   Key preview: {SENDGRID_API_KEY[:10]}...{SENDGRID_API_KEY[-4:]}")
    print("\n💡 To get a free API key:")
    print("   1. Visit https://signup.sendgrid.com/")
    print("   2. Sign up for free account (100 emails/day)")
    print("   3. Create API key at Settings > API Keys")
    print("   4. Run: export SENDGRID_API_KEY='your-key'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} test              # Test configuration")
        print(f"  {sys.argv[0]} to@email.com 'Subject' 'Body' [attachment.pdf]")
        sys.exit(1)
    
    if sys.argv[1] == "test":
        test_without_sending()
        sys.exit(0)
    
    if len(sys.argv) < 4:
        print("❌ Error: Need at least 3 arguments: to, subject, body")
        sys.exit(1)
    
    to_email = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment = sys.argv[4] if len(sys.argv) > 4 else None
    
    success = send_email_sendgrid(to_email, subject, body, attachment)
    sys.exit(0 if success else 1)
