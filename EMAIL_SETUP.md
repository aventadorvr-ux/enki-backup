# Email Setup Guide - aventadorvr@gmail.com

**Date:** March 12, 2026  
**Location:** ~/.openclaw/workspace/EMAIL_SETUP.md

---

## ✅ INSTALLED TOOLS

| Tool | Purpose | Status |
|------|---------|--------|
| **msmtp** | Send emails via SMTP | ✅ Installed |
| **mailutils** | Mail command interface | ✅ Installed |
| **mutt** | Email client (read/receive) | ✅ Installed |

---

## 🔐 REQUIRED: Gmail App Password

**You MUST create an App Password before email will work.**

### How to Create App Password:

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in to aventadorvr@gmail.com
3. Click "Select app" → Choose "Mail"
4. Click "Select device" → Choose "Other (Custom name)"
   - Name it: "OpenClaw Server" or "Enki AI"
5. Click "Generate"
6. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)
7. Save this password securely - you cannot view it again!

---

## 📧 SENDING EMAILS

### Option 1: Quick Command (after setting password)

```bash
# Set the password (one-time per session, or add to ~/.bashrc)
export MSMTP_PASSWORD="your_16_char_app_password"

# Send email
echo "Email body text here" | mail -s "Subject line" recipient@example.com
```

### Option 2: Using the Wrapper Script

```bash
# Set password
export MSMTP_PASSWORD="your_16_char_app_password"

# Send email
cd ~/.openclaw/workspace/scripts
./send-email.sh "recipient@example.com" "Subject" "Body text"
```

### Option 3: With Attachment (PDF, etc.)

```bash
export MSMTP_PASSWORD="your_16_char_app_password"

echo "Please find the framework attached." | \
  mail -s "Real Estate AI Framework" \
  -A /path/to/file.pdf \
  recipient@example.com
```

---

## 📥 RECEIVING EMAILS

### Using Mutt (Interactive)

```bash
# Set password
export MUTT_PASSWORD="your_16_char_app_password"

# Open email client
mutt -F ~/.muttrc-gmail
```

**Mutt controls:**
- `i` - Go to inbox
- `Enter` - Open email
- `r` - Reply
- `d` - Delete
- `q` - Quit

### Check Inbox (Command Line)

```bash
# List unread emails
echo "No direct CLI tool installed - use mutt or set up fetchmail"

# Alternative: Use Python script (can be created if needed)
```

---

## 🔄 AUTOMATED EMAIL CHECKING

### Cron Job to Check Email Every Hour

```bash
# Edit crontab
crontab -e

# Add line:
0 * * * * export MUTT_PASSWORD="your_password" && /usr/bin/mutt -F ~/.muttrc-gmail -e "push 'c<enter>'" -e "push 'q'" > /dev/null 2>&1
```

---

## 🧪 TEST EMAIL SETUP

### Test Sending:

```bash
# 1. Set password
export MSMTP_PASSWORD="your_16_char_app_password"

# 2. Send test to yourself
echo "Test email from Enki AI server" | \
  mail -s "Test Email" \
  aventadorvr@gmail.com

# 3. Check logs if failed
cat ~/.msmtp.log
```

### Expected Output:
```
✅ Email sent successfully to aventadorvr@gmail.com
```

---

## 🔒 SECURITY NOTES

- **Never commit passwords to Git** ✅ `.msmtprc` has restrictive permissions (600)
- **Use environment variables** for passwords in scripts
- **App Passwords are safer** than your main Gmail password
- **Rotate passwords** every 90 days recommended
- **Monitor sent folder** for unauthorized emails

---

## 🐛 TROUBLESHOOTING

### "Authentication failed"
- Check you created an **App Password** (not your regular Gmail password)
- Verify password is exported: `echo $MSMTP_PASSWORD`

### "SMTP server not found"
- Check internet connection: `ping smtp.gmail.com`
- Verify firewall allows port 587

### "Permission denied"
- Config file permissions: `chmod 600 ~/.msmtprc`

### Emails not appearing
- Check spam folder
- Verify `from` address matches Gmail account
- Check logs: `cat ~/.msmtp.log`

---

## 📋 QUICK REFERENCE

| Action | Command |
|--------|---------|
| Set password | `export MSMTP_PASSWORD="xxx"` |
| Send email | `echo "body" \| mail -s "subject" recipient` |
| Send with attachment | `echo "body" \| mail -s "subject" -A file.pdf recipient` |
| Read emails | `mutt -F ~/.muttrc-gmail` |
| Check logs | `cat ~/.msmtp.log` |

---

## ⚡ IMMEDIATE ACTION REQUIRED

**You need to:**
1. Create Gmail App Password at https://myaccount.google.com/apppasswords
2. Run: `export MSMTP_PASSWORD="your_password"`
3. Test: `echo "test" | mail -s "Test" aventadorvr@gmail.com`

**Then I can send you PDFs and documents directly.**

---

*Setup by Enki AI - March 12, 2026*
