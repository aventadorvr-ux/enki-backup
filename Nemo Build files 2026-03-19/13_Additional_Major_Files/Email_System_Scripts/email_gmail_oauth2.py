#!/usr/bin/env python3
"""
Email sender using Gmail OAuth2
This avoids the "app password required" error by using proper OAuth2 flow.

Setup (one-time):
1. Go to https://console.cloud.google.com/
2. Create a project → Enable Gmail API
3. Create OAuth2 credentials (Desktop application)
4. Download client_secret.json
5. Run first auth flow to get token.json

Usage:
    python3 email_gmail_oauth2.py to@example.com "Subject" "Body" [attachment.pdf]
"""

import os
import sys
import base64
import json
from pathlib import Path

# Gmail OAuth2 settings
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRETS_FILE = os.path.expanduser('~/.openclaw/workspace/client_secret.json')
TOKEN_FILE = os.path.expanduser('~/.openclaw/workspace/gmail_token.json')

def get_credentials():
    """Get or refresh OAuth2 credentials."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("❌ Required packages not installed")
        print("   Run: pip install google-auth google-auth-oauthlib google-auth-httplib2")
        return None
    
    creds = None
    
    # Load existing token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Refresh or create new token
    if not credreds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing token...")
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print(f"❌ Client secrets file not found: {CLIENT_SECRETS_FILE}")
                print("   Download it from Google Cloud Console:")
                print("   https://console.cloud.google.com/apis/credentials")
                return None
            
            print("🔐 Starting OAuth2 authorization flow...")
            print("   A browser should open. If not, follow the URL provided.")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token for future runs
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        print(f"💾 Token saved to {TOKEN_FILE}")
    
    return creds

def send_email_gmail_oauth(to_email, subject, body, attachment_path=None):
    """Send email using Gmail API with OAuth2."""
    
    try:
        from googleapiclient.discovery import build
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
    except ImportError:
        print("❌ Required packages not installed")
        print("   Run: pip install google-api-python-client google-auth")
        return False
    
    creds = get_credentials()
    if not creds:
        return False
    
    try:
        # Create message
        message = MIMEMultipart()
        message['to'] = to_email
        message['subject'] = subject
        
        # Get "from" email from credentials
        from_email = getattr(creds, 'id_token', None)
        if from_email:
            message['from'] = from_email
        
        # Add body
        message.attach(MIMEText(body, 'plain'))
        
        # Add attachment
        if attachment_path and os.path.exists(attachment_path):
            filename = os.path.basename(attachment_path)
            with open(attachment_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            message.attach(part)
            print(f"📎 Attached: {filename}")
        
        # Encode and send
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        service = build('gmail', 'v1', credentials=creds)
        print(f"📤 Sending email to {to_email}...")
        
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        print(f"✅ Email sent! Message ID: {result['id']}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_setup():
    """Check if OAuth2 is properly configured."""
    print("🔍 Gmail OAuth2 Setup Check")
    print(f"   Client secrets: {'✅ Found' if os.path.exists(CLIENT_SECRETS_FILE) else '❌ Not found'}")
    print(f"   Token file: {'✅ Found' if os.path.exists(TOKEN_FILE) else '❌ Not found'}")
    
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print("\n📋 Setup Instructions:")
        print("   1. Go to https://console.cloud.google.com/")
        print("   2. Create a new project (or select existing)")
        print("   3. Enable the Gmail API:")
        print("      APIs & Services → Library → Gmail API → Enable")
        print("   4. Create OAuth2 credentials:")
        print("      APIs & Services → Credentials → Create Credentials → OAuth client ID")
        print("      Application type: Desktop app")
        print("      Name: Enki Email")
        print("   5. Download the JSON file and save as:")
        print(f"      {CLIENT_SECRETS_FILE}")
        print("   6. Run this script to authorize")
    
    return os.path.exists(CLIENT_SECRETS_FILE)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} check             # Check OAuth2 setup")
        print(f"  {sys.argv[0]} to@email.com 'Subject' 'Body' [attachment.pdf]")
        sys.exit(1)
    
    if sys.argv[1] in ('check', 'setup', 'test'):
        check_setup()
        sys.exit(0)
    
    if len(sys.argv) < 4:
        print("❌ Error: Need at least 3 arguments: to, subject, body")
        sys.exit(1)
    
    to_email = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment = sys.argv[4] if len(sys.argv) > 4 else None
    
    success = send_email_gmail_oauth(to_email, subject, body, attachment)
    sys.exit(0 if success else 1)
