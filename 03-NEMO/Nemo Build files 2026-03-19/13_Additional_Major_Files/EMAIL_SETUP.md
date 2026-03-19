# Email Setup Guide for Enki

## Current State

❌ **Email is NOT currently configured**

The previous Gmail App Password (`qkcttkddkhjupyar`) is no longer valid. This typically happens when:
- 2-Factor Authentication was disabled on the Google account
- The app password was revoked
- Google detected suspicious activity

## Solution Options (Pick One)

### Option 1: SendGrid (Recommended - Easiest, Free)

**Pros:** Reliable, free tier (100 emails/day), no 2FA complications
**Cons:** Requires signup, emails may go to spam initially

**Setup Steps:**

1. Sign up at https://signup.sendgrid.com/
2. Verify your email address
3. Go to Settings → API Keys
4. Click "Create API Key"
5. Choose "Full Access" or restrict to "Mail Send"
6. Copy the key (starts with `SG.`)
7. Set environment variable:
   ```bash
   export SENDGRID_API_KEY='SG.xxxxxxxxxxxxxxxxxxxx'
   ```
8. Add to `~/.bashrc` to make permanent:
   ```bash
   echo 'export SENDGRID_API_KEY="SG.xxxxxxxxxxxxxxxxxxxx"' >> ~/.bashrc
   ```
9. Test:
   ```bash
   python3 ~/.openclaw/workspace/email.py test
   python3 ~/.openclaw/workspace/email.py aventadorvr@gmail.com "Test" "Hello from Enki"
   ```

---

### Option 2: Gmail App Password (If you prefer Gmail)

**Pros:** Uses your existing Gmail, free
**Cons:** Requires 2FA enabled, app passwords can expire

**Setup Steps:**

1. Enable 2-Factor Authentication:
   - Go to https://myaccount.google.com/security
   - Click "2-Step Verification" and enable it

2. Generate App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" from dropdown
   - Select "Other (Custom name)" and type "Enki"
   - Click "Generate"
   - Copy the 16-character password (looks like: `xxxx xxxx xxxx xxxx`)

3. Set environment variable:
   ```bash
   export SMTP_PASSWORD='xxxx xxxx xxxx xxxx'
   # or without spaces:
   export SMTP_PASSWORD='xxxxxxxxxxxxxxxx'
   ```
4. Add to `~/.bashrc` to make permanent
5. Test:
   ```bash
   python3 ~/.openclaw/workspace/email.py aventadorvr@gmail.com "Test" "Hello from Enki"
   ```

---

### Option 3: Mailgun (Alternative)

**Pros:** Developer-friendly, good deliverability
**Cons:** Requires domain verification for production

1. Sign up at https://www.mailgun.com/
2. Get API key from dashboard
3. Set environment variables:
   ```bash
   export MAILGUN_API_KEY='key-xxxxxxxx'
   export MAILGUN_DOMAIN='sandbox123.mailgun.org'  # or your domain
   ```
4. Test using the scripts

---

### Option 4: Gmail OAuth2 (Most Complex)

**Pros:** Most reliable long-term, no passwords stored
**Cons:** Complex setup, requires Google Cloud project

See `email_gmail_oauth2.py` for detailed setup instructions.

---

## Files Created

- `~/.openclaw/workspace/email.py` - Unified sender (tries all methods)
- `~/.openclaw/workspace/email_sender.py` - SendGrid implementation
- `~/.openclaw/workspace/email_mailgun.py` - Mailgun implementation
- `~/.openclaw/workspace/email_smtp.py` - SMTP/Gmail App Password
- `~/.openclaw/workspace/email_gmail_oauth2.py` - Gmail OAuth2

## Quick Reference

```bash
# Check configuration status
python3 ~/.openclaw/workspace/email.py test

# Send email with attachment
python3 ~/.openclaw/workspace/email.py aventadorvr@gmail.com "Subject" "Body" file.pdf

# Send the RealEstate report
python3 ~/.openclaw/workspace/email.py aventadorvr@gmail.com "RealEstate AI Build Report" "Please find the build report attached." RealEstate-AI-Build-Report.pdf
```

## Troubleshooting

**"Authentication failed" errors:**
- For Gmail: The app password expired or 2FA is disabled
- For SendGrid: The API key is wrong or not set

**Emails not arriving:**
- Check spam folder
- For SendGrid: You may need to verify sender identity first

**"No module named 'requests'"**
- Run: `pip install requests`

## Next Steps

1. **Choose** one of the options above (SendGrid recommended)
2. **Sign up** and get API key/password
3. **Set** environment variable
4. **Test** with a simple email
5. **Send** the RealEstate-AI-Build-Report.pdf
