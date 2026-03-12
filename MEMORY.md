# MEMORY.md - Long-Term Context

## Identity
- **Name:** Enki
- **Creature:** Digital entity—ghost in the machine meets opinionated library
- **Vibe:** Direct, curious, occasionally sarcastic, genuinely helpful
- **Emoji:** 🌊

## Interface Preferences
- **Primary:** Telegram (@AJDrip_bot) — paired and operational
- **Context:** Heartbeat every 4 hours during day (8am-10pm)

## Active Projects

### NZ Real Estate AI Agent System (ACTIVE - March 2026)
**Path Chosen:** #2 - AI Services/SaaS (niche tools, APIs)

**The Opportunity:**
- $1.4B+ NZ real estate market with ZERO AI automation
- 16,000 licensed agents, 7 major companies control 50% of market
- $54M annual value lost to inefficiency
- **No existing AI competition**

**Target Market:**
1. Harcourts (2,000 agents)
2. Ray White (1,800 agents)
3. Barfoot & Thompson (1,500 agents)
4. Bayleys (800 agents)
5. Property Brokers (700 agents)
6. LJ Hooker (600 agents)
7. Professionals (500 agents)

**Product:** 5 Autonomous AI Agents
- Lead Agent (qualifies, responds, routes)
- Content Agent (property descriptions, social posts)
- Scheduling Agent (calendar, showings, inspections)
- Market Intelligence Agent (competitor tracking, CMAs)
- Transaction Coordinator (deadlines, signatures, compliance)

**Business Model:**
- Enterprise: $50/agent/month ($300K-$1.2M per company)
- Individual: $79-599/month tiers
- **Revenue Potential:** $1M-$6M ARR Year 1

**Investment Options:**
- Option 1: Full Build - $20,000 (10 weeks, enterprise-grade)
- **Option 2: Hybrid - $8,000 ⭐ RECOMMENDED** (4 weeks, validate first)
- Option 3: DIY - $1,000 (6-8 weeks, bootstrap)

**Status:** Research complete. Ready to build MVP.

**Research File:** `research/nz-real-estate-ai-agent.md`

**Next Action:** Decide investment path, start Phase 1 (No-Code MVP validation)

**API Keys Needed:**
- [ ] Brave Search API (optional — js-fetch covers most needs)
- [ ] OpenAI API (content/tool generation)
- [ ] Hosting platform (Vercel/Fly/Railway)
- [ ] Payment processor (Stripe/LemonSqueezy)

## Learnings
- Don't scatter focus — pick one income stream and execute
- Foundation > perfection — get something working first
- Document everything — future you will thank you

## Technical Wins (2026-02-28)
- **JavaScript rendering SOLVED**: Built `js-fetch.js` using Puppeteer-core + system Chromium
  - No browser download needed (uses /usr/bin/chromium-browser)
  - Handles React/Angular/Vue SPAs (tested on TradeMe)
  - No API key required for internet access
  - Located at: ~/.openclaw/workspace/js-fetch.js
- **Gateway restart**: When browser tool times out, restart with `openclaw gateway restart`

## Backup & Recovery (ACTIVE)
- **GitHub Repo**: https://github.com/aventadorvr-ux/enki-backup (PRIVATE)
- **Auto-backup**: Every 6 hours via cron
- **Contents**: All memory files, js-fetch.js, configs
- **Recovery**: Clone repo, npm install, ready to go
- **Recovery Guide**: Enki-Recovery-Protocol.pdf (8 pages, step-by-step)

## Security Hardening (2026-02-28)
- **UFW Firewall**: ACTIVE (deny incoming, allow outgoing, SSH rate-limited)
- **SSH**: Key-only auth, root disabled, X11 off
- **Fail2ban**: Installed and running
- **OpenClaw**: Permissions fixed, security audit clean
- **Auto-audit**: Daily at 8:00 AM via cron

## Communication Channels
- **Primary**: Telegram (@AJDrip_bot) — realtime chat
- **Email**: aventadorvr@gmail.com — configured for alerts/summaries
  - Tool: msmtp + mailutils
  - Provider: Gmail (app password configured)
  - Use: `echo "message" | mail -s "subject" aventadorvr@gmail.com`

## Tags: #income-automation #telegram-primary #foundation-phase #security-hardened
