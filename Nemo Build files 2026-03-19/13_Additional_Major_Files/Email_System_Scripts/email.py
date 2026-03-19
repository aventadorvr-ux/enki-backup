#!/usr/bin/env python3
"""
Unified Email Sender for Enki
Tries multiple email methods in order until one works

Methods (in order):
1. SendGrid API (100 emails/day free)
2. Mailgun API (100 emails/day after trial)
3. Gmail SMTP with App Password
4. Gmail OAuth2 API (requires setup)

Usage:
    python3 email.py test                          # Test configuration
    python3 email.py to@email.com "Subject" "Body" [attachment.pdf]
    
Environment Variables:
    SENDGRID_API_KEY    - SendGrid API key
    MAILGUN_API_KEY     - Mailgun API key
    MAILGUN_DOMAIN      - Mailgun domain
    SMTP_USER           - SMTP username (default: aventadorvr@gmail.com)
    SMTP_PASSWORD       - SMTP password (app password for Gmail)
"""

import sys
import os

# Add workspace to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import individual senders
try:
    from email_sender import send_email_sendgrid
except ImportError:
    send_email_sendgrid = None

try:
    from email_mailgun import send_email_mailgun
except ImportError:
    send_email_mailgun = None

try:
    from email_smtp import send_email_smtp
except ImportError:
    send_email_smtp = None

try:
    from email_gmail_oauth2 import send_email_gmail_oauth
except ImportError:
    send_email_gmail_oauth = None

def get_config_status():
    """Get status of all email methods."""
    status = []
    
    # SendGrid
    sg_key = os.environ.get('SENDGRID_API_KEY', '')
    status.append(f"SendGrid: {'✅' if sg_key else '❌'} (SENDGRID_API_KEY)")
    
    # Mailgun
    mg_key = os.environ.get('MAILGUN_API_KEY', '')
    mg_domain = os.environ.get('MAILGUN_DOMAIN', '')
    status.append(f"Mailgun: {'✅' if (mg_key and mg_domain) else '❌'} (MAILGUN_API_KEY, MAILGUN_DOMAIN)")
    
    # SMTP
    smtp_pwd = os.environ.get('SMTP_PASSWORD', '')
    status.append(f"SMTP: {'✅' if smtp_pwd else '❌'} (SMTP_PASSWORD)")
    
    # OAuth2
    client_secret = os.path.exists(os.path.expanduser('~/.openclaw/workspace/client_secret.json'))
    status.append(f"Gmail OAuth2: {'✅' if client_secret else '❌'} (client_secret.json)")
    
    return status

def send_email(to_email, subject, body, attachment_path=None):
    """Try sending email with available methods."""
    
    methods = [
        ("SendGrid", send_email_sendgrid),
        ("Mailgun", send_email_mailgun),
        ("Gmail SMTP", send_email_smtp),
        ("Gmail OAuth2", send_email_gmail_oauth),
    ]
    
    for name, sender_func in methods:
        if sender_func is None:
            continue
            
        print(f"\n📧 Trying {name}...")
        try:
            if sender_func(to_email, subject, body, attachment_path):
                print(f"✅ Success with {name}!")
                return True
        except Exception as e:
            print(f"   Error: {e}")
            continue
    
    print("\n❌ All email methods failed")
    print("\n💡 To set up email, choose one of these options:")
    print("   1. SendGrid (Recommended): https://signup.sendgrid.com/")
    print("   2. Mailgun: https://www.mailgun.com/")
    print("   3. Gmail App Password: Enable 2FA → https://myaccount.google.com/apppasswords")
    print("\n   Then set the appropriate environment variables.")
    
    return False

def show_help():
    """Show help and configuration status."""
    print("🌊 Enki Email Sender")
    print("=" * 50)
    print("\n📊 Configuration Status:")
    for status in get_config_status():
        print(f"   {status}")
    
    print("\n📖 Usage:")
    print("   python3 email.py test                          # Show this help")
    print("   python3 email.py to@email.com 'Subject' 'Body' [attachment.pdf]")
    
    print("\n🔧 Setup Options:")
    print("\n   Option 1: SendGrid (Easiest, 100 emails/day)")
    print("   1. Sign up: https://signup.sendgrid.com/")
    print("   2. Verify your email")
    print("   3. Create API key at Settings → API Keys")
    print("   4. Run: export SENDGRID_API_KEY='SG.xxx'")
    
    print("\n   Option 2: Gmail App Password")
    print("   1. Enable 2FA: https://myaccount.google.com/security")
    print("   2. Create app password: https://myaccount.google.com/apppasswords")
    print("   3. Choose 'Mail' → 'Other' → name it 'Enki'")
    print("   4. Copy the 16-char password")
    print("   5. Run: export SMTP_PASSWORD='your-16-char-password'")
    
    print("\n   Option 3: Gmail OAuth2 (Most complex, most reliable)")
    print("   1. Go to https://console.cloud.google.com/")
    print("   2. Create project → Enable Gmail API")
    print("   3. Create OAuth2 Desktop credentials")
    print("   4. Download client_secret.json to workspace")
    print("   5. Run: python3 email_gmail_oauth2.py check")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    if sys.argv[1] in ('test', 'help', '--help', '-h'):
        show_help()
        sys.exit(0)
    
    if len(sys.argv) < 4:
        print("❌ Error: Need at least 3 arguments: to, subject, body")
        print("   Run 'python3 email.py help' for usage")
        sys.exit(1)
    
    to_email = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachment = sys.argv[4] if len(sys.argv) > 4 else None
    
    success = send_email(to_email, subject, body, attachment)
    sys.exit(0 if success else 1)
