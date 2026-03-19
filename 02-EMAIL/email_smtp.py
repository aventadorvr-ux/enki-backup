#!/usr/bin/env python3
"""
Simple SMTP email sender using Python's smtplib
Works with Gmail App Passwords, Outlook, and other SMTP providers

Gmail Setup:
1. Enable 2-Factor Authentication on your Google account
2. Generate App Password at: https://myaccount.google.com/apppasswords
3. Use that 16-character password in the config below (NOT your regular password)

Usage:
    python3 email_smtp.py to@example.com "Subject" "Body" [attachment.pdf]
"""

import sys
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import getpass

# SMTP Configuration - READ FROM .msmtprc CONFIG FILE
def load_smtp_config():
    """Load SMTP config from .msmtprc file."""
    config = {
        'host': 'smtp.gmail.com',
        'port': 587,
        'user': 'aventadorvr@gmail.com',
        'password': '',
        'from': 'aventadorvr@gmail.com'
    }
    try:
        with open('/data/data/com.termux/files/home/.openclaw/workspace/.msmtprc', 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('host '):
                    config['host'] = line.split(' ', 1)[1]
                elif line.startswith('port '):
                    config['port'] = int(line.split(' ', 1)[1])
                elif line.startswith('user '):
                    config['user'] = line.split(' ', 1)[1]
                elif line.startswith('password '):
                    config['password'] = line.split(' ', 1)[1]
                elif line.startswith('from '):
                    config['from'] = line.split(' ', 1)[1]
    except Exception as e:
        print(f"⚠️  Could not read .msmtprc: {e}")
    return config

_cfg = load_smtp_config()
SMTP_HOST = _cfg['host']
SMTP_PORT = _cfg['port']
SMTP_USER = _cfg['user']
SMTP_PASSWORD = _cfg['password']
SMTP_FROM = _cfg['from']

def send_email_smtp(to_email, subject, body, attachment_path=None, password=None):
    """Send email using SMTP with TLS."""
    
    # Get password from parameter, env, or prompt
    pwd = password or SMTP_PASSWORD
    if not pwd:
        print(f"🔐 Enter app password for {SMTP_USER}:")
        pwd = getpass.getpass("   Password: ")
    
    if not pwd:
        print("❌ Error: No password provided")
        return False
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = SMTP_FROM
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add body
    msg.attach(MIMEText(body, 'plain'))
    
    # Add attachment
    if attachment_path and os.path.exists(attachment_path):
        filename = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        msg.attach(part)
        print(f"📎 Attached: {filename}")
    elif attachment_path:
        print(f"⚠️  Attachment not found: {attachment_path}")
    
    try:
        print(f"📤 Connecting to {SMTP_HOST}:{SMTP_PORT}...")
        
        # Create secure SSL context
        context = ssl.create_default_context()
        
        # Connect and send
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            
            print(f"🔐 Authenticating as {SMTP_USER}...")
            server.login(SMTP_USER, pwd)
            
            print(f"📧 Sending to {to_email}...")
            server.send_message(msg)
            
        print(f"✅ Email sent successfully!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   For Gmail:")
        print("   1. You MUST use an App Password, not your regular password")
        print("   2. Enable 2FA first at https://myaccount.google.com/security")
        print("   3. Generate app password at https://myaccount.google.com/apppasswords")
        print("   4. Select 'Mail' and your device, copy the 16-char password")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config():
    """Show current configuration."""
    print("🔍 SMTP Configuration")
    print(f"   Host: {SMTP_HOST}")
    print(f"   Port: {SMTP_PORT}")
    print(f"   User: {SMTP_USER}")
    print(f"   From: {SMTP_FROM}")
    print(f"   Password: {'✅ Set' if SMTP_PASSWORD else '❌ Not set'}")
    print("\n📋 Gmail App Password Setup:")
    print("   1. Enable 2FA: https://myaccount.google.com/security")
    print("   2. Create app password: https://myaccount.google.com/apppasswords")
    print("   3. Choose 'Mail' → 'Other (Custom name)' → 'Enki'")
    print("   4. Copy the 16-character password (no spaces)")
    print("   5. Use it with this script (NOT your regular Gmail password)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} test                  # Show configuration")
        print(f"  {sys.argv[0]} to@email.com 'Subject' 'Body' [attachment.pdf]")
        print(f"\nEnvironment variables:")
        print(f"  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM")
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
    
    success = send_email_smtp(to_email, subject, body, attachment)
    sys.exit(0 if success else 1)
