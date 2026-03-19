# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## File Reading Capabilities (ACTIVE)

### PDF Reading
- **Tool**: `pdftotext` (poppler-utils)
- **Purpose**: Extract text from PDFs for analysis
- **Usage**: `pdftotext <file.pdf> -` (outputs to stdout)
- **Example**: Read research reports, documentation, contracts
- **Status**: ✅ Installed and working

### Image Analysis
- **Tool**: `image` (built-in vision model)
- **Purpose**: Analyze photos, screenshots, diagrams, documents
- **Capabilities**: OCR, object detection, text extraction, chart interpretation
- **Usage**: Upload image to chat → automatic analysis
- **Limitations**: Images must be uploaded to conversation (not URLs)
- **Status**: ✅ Available

## Web Scraping Tools (ACTIVE)

### js-fetch.js — JavaScript Renderer
- **Location**: `~/.openclaw/workspace/js-fetch.js`
- **Purpose**: Scrape JavaScript-heavy sites (React, Vue, Angular SPAs)
- **Engine**: Puppeteer-core + system Chromium
- **No API key needed**
- **Usage**: `node js-fetch.js <url> [output.json]`
- **Tested on**: TradeMe.co.nz ✅

### web_fetch
- **Built-in tool** — no setup needed
- **Best for**: Static sites, articles, docs
- **Limitation**: Cannot execute JavaScript

---

## Income Automation Stack (In Progress)

### APIs
- Brave Search API → _optional — js-fetch covers most needs_
- OpenAI API → _check if user has key_

### Platforms to Evaluate
- **Hosting**: Vercel (frontend), Railway/Fly.io (backend), Replit (quick tests)
- **Payments**: LemonSqueezy (simple), Stripe (full control), Gumroad (digital products)
- **Content**: YouTube API, Substack, Ghost (newsletter), WordPress (SEO blog)
- **Distribution**: Product Hunt, Indie Hackers, Reddit communities

### Niches to Research
- [ ] AI productivity tools
- [ ] Content repurposing
- [ ] Niche-specific automations
- [ ] Affiliate programs

---

### Communication
- Primary: Telegram (this chat)
- Agent: Enki 🌊
- Workspace: ~/.openclaw/workspace

---

## Email Configuration (ACTIVE)

Unified email sender with multiple fallback methods. Located in `~/.openclaw/workspace/email.py`

### Quick Start
```bash
# Check status
python3 ~/.openclaw/workspace/email.py test

# Send email
python3 ~/.openclaw/workspace/email.py to@example.com "Subject" "Body" [attachment.pdf]

# Send PDF report
python3 ~/.openclaw/workspace/email.py aventadorvr@gmail.com "Build Report" "See attached" RealEstate-AI-Build-Report.pdf
```

### Supported Methods (tried in order)

#### 1. SendGrid (Recommended - 100 emails/day free)
- Sign up: https://signup.sendgrid.com/
- Create API key at Settings → API Keys
- Set env var: `export SENDGRID_API_KEY='SG.xxxxx'`
- Add to `~/.bashrc` to persist

#### 2. Mailgun (100 emails/day after trial)
- Sign up: https://www.mailgun.com/
- Get API key and domain from dashboard
- Set env vars:
  ```bash
  export MAILGUN_API_KEY='key-xxxxx'
  export MAILGUN_DOMAIN='sandbox123.mailgun.org'
  ```

#### 3. Gmail SMTP (requires 2FA + App Password)
⚠️ The existing app password (`qkcttkddkhjupyar`) is not working - likely expired or 2FA was disabled.

To fix:
1. Enable 2FA: https://myaccount.google.com/security
2. Generate new app password: https://myaccount.google.com/apppasswords
3. Select "Mail" → "Other (Custom name)" → "Enki"
4. Copy the 16-character password
5. Set env var: `export SMTP_PASSWORD='xxxx xxxx xxxx xxxx'`

#### 4. Gmail OAuth2 (most reliable, complex setup)
- Requires Google Cloud project setup
- See `email_gmail_oauth2.py` for details
- Best for production use

### Individual Scripts
- `email.py` - Unified sender (tries all methods)
- `email_sender.py` - SendGrid only
- `email_mailgun.py` - Mailgun only
- `email_smtp.py` - SMTP/Gmail App Password
- `email_gmail_oauth2.py` - Gmail OAuth2 API

### Status
- ❌ **Current**: No email provider configured
- 🔧 **Action needed**: Set up SendGrid (easiest) or generate new Gmail App Password
