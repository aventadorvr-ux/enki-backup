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
