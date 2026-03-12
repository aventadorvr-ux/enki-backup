# Enki Backup & Recovery Protocol v3.0

**Version:** 3.0  
**Date:** 2026-03-12  
**Repository:** https://github.com/aventadorvr-ux/enki-backup

---

## PART 1: CRITICAL INFORMATION

### Emergency Access
- **Primary Interface:** Telegram @AJDrip_bot
- **Server:** AWS EC2 (Ubuntu)
- **Gateway Dashboard:** http://127.0.0.1:18789/
- **Email:** aventadorvr@gmail.com (alerts/summaries)
- **GitHub:** aventadorvr-ux/enki-backup

⚠️ **KEEP THIS DOCUMENT SAFE** — Store outside your primary server.

---

## PART 2: SYSTEM ARCHITECTURE

### Core Components
| Component | Purpose |
|-----------|---------|
| OpenClaw Gateway | Message routing, channel integration |
| Agent (Main) | AI assistant runtime (Enki) |
| Workspace | /home/ubuntu/.openclaw/workspace (all data) |
| Memory System | SQLite + markdown files (continuity) |
| Git Backup | GitHub repo (auto-backup every 6h) |
| Tool Stack | PDF, Web scraping, API integrations |

### Directory Structure
```
/home/ubuntu/
└── .openclaw/
    ├── workspace/           ← PRIMARY DATA (backed up)
    │   ├── AGENTS.md        (persona rules)
    │   ├── MEMORY.md        (long-term memory)
    │   ├── USER.md          (human profile)
    │   ├── SOUL.md          (core behavior)
    │   ├── TOOLS.md         (tool capabilities)
    │   ├── HEARTBEAT.md     (periodic tasks)
    │   ├── IDENTITY.md      (agent identity)
    │   ├── js-fetch.js      (web scraping tool)
    │   ├── node_modules/    (dependencies)
    │   ├── memory/          (daily logs: YYYY-MM-DD.md)
    │   ├── research/        (project research)
    │   └── skills/          (available skills)
    ├── agents/
    │   └── main/
    │       └── sessions/    (conversation history)
    ├── media/
    │   └── inbound/         (received files)
    ├── memory/              (SQLite database)
    │   └── main.sqlite
    ├── logs/                (system logs)
    └── openclaw.json        (gateway config)
```

---

## PART 3: ACTIVE PROJECTS & DATA INVENTORY

### Project 1: NZ Real Estate AI Agent System ⭐ CRITICAL

**Status:** Research Complete → Ready for MVP Build

**The Opportunity:**
- Market: $1.4B+ NZ real estate, ZERO AI competition
- 16,000 licensed agents, 7 major companies (50% market share)
- $54M annual value lost to inefficiency

**Target Companies:**
| Company | Agents | Monthly Revenue |
|---------|--------|-----------------|
| Harcourts | 2,000 | $1,200,000 |
| Ray White | 1,800 | $1,080,000 |
| Barfoot & Thompson | 1,500 | $900,000 |
| Bayleys | 800 | $480,000 |
| Property Brokers | 700 | $420,000 |
| LJ Hooker | 600 | $360,000 |
| Professionals | 500 | $300,000 |
| **Total** | **7,900** | **$4,740,000** |

**The Product: 5 AI Agents**
1. **Lead Agent** — qualifies, responds in <2min (vs 4-8hr industry avg)
2. **Content Agent** — property descriptions, social posts, SEO
3. **Scheduling Agent** — calendar, showings, inspections
4. **Market Intelligence Agent** — competitor tracking, CMAs, pricing
5. **Transaction Coordinator** — deadlines, signatures, compliance

**Investment Options:**
- Option 1: Full Build — $20,000 (10 weeks, enterprise-grade)
- **Option 2: Hybrid ⭐ RECOMMENDED** — $8,000 (4 weeks, validate first)
- Option 3: DIY — $1,000 (6-8 weeks, bootstrap)

**Revenue Model:**
- Enterprise: $50/agent/month
- Individual: $79-599/month tiers
- Year 1 Potential: $1M-$6M ARR

**Key Documents:**
- Full Research: `research/nz-real-estate-ai-agent.md`
- Pitch Deck: `media/inbound/Sales_Presentation_NZ_Real_Estate_Agent_AI_Agent.pdf`

**API Keys Status:**
- [ ] OpenAI API — *need to verify*
- [ ] Hosting (Vercel/Fly/Railway) — *pending*
- [ ] Payment processor (Stripe/LemonSqueezy) — *pending*
- [x] Brave Search API — configured: `BSA1VLqWDUBlPEoJHLfLssU7xZQNjzg`

### Project 2: Income Automation Stack

**Status:** Foundation Complete
- js-fetch.js built (JavaScript rendering tool)
- Decision: AI Services/SaaS path selected
- Technical infrastructure operational

---

## PART 4: BACKUP STRATEGY

### What Gets Backed Up ✅
- All markdown files (MEMORY.md, research/, memory/)
- JavaScript tools (js-fetch.js, configs)
- Node modules (dependencies can be reinstalled)
- Skills documentation
- Git history

### NOT Backed Up ⚠️
- Session conversation history (SQLite in ~/.openclaw/agents/main/sessions/)
- Received media files (must copy separately)
- API keys/secrets (must reconfigure)
- System logs (transient)

### Auto-Backup Schedule
- Frequency: Every 6 hours via cron
- Location: GitHub private repo

---

## PART 5: RECOVERY PROCEDURES

### Scenario 1: Gateway Crash
```bash
# Check status
openclaw status

# Restart gateway
openclaw gateway restart

# If stuck
openclaw gateway stop && openclaw gateway start
```

### Scenario 2: Complete Server Rebuild

**Prerequisites:**
- [ ] New EC2 instance (Ubuntu Server 22.04 LTS)
- [ ] SSH access configured
- [ ] GitHub repo access (SSH key)

**Recovery Steps:**

1. **Update system**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl nodejs npm poppler-utils chromium-browser
```

2. **Install OpenClaw**
```bash
npm install -g openclaw
```

3. **Clone workspace backup**
```bash
mkdir -p ~/.openclaw
git clone git@github.com:aventadorvr-ux/enki-backup.git ~/.openclaw/workspace
cd ~/.openclaw/workspace
npm install
```

4. **Configure OpenClaw**
```bash
openclaw onboard
# Set workspace: ~/.openclaw/workspace
# Configure Telegram bot token
# Set AI model: openrouter/moonshotai/kimi-k2.5
```

5. **Set up GitHub SSH**
```bash
ssh-keygen -t ed25519 -C "enki-backup"
cat ~/.ssh/id_ed25519.pub
# Add key to GitHub → Settings → SSH Keys
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

6. **Configure backup cron**
```bash
crontab -e
# Add: 0 */6 * * * cd ~/.openclaw/workspace && git add -A && git commit -m "Auto-backup" && git push origin master:main
```

7. **Start gateway**
```bash
openclaw gateway
```

8. **Pair Telegram**
```bash
openclaw pairing list telegram
openclaw pairing approve telegram <your-code>
```

9. **Verify recovery**
- Send test message to @AJDrip_bot
- Confirm bot responds

---

## PART 6: TOOL CAPABILITIES

### Available Tools
| Tool | Purpose | Status |
|------|---------|--------|
| pdftotext | PDF reading | ✅ Installed v24.02.0 |
| chromium-browser | Web scraping | ✅ Installed v145.0.7632 |
| js-fetch.js | JavaScript SPAs | ✅ Built & tested |
| Git | Version control | ✅ v2.43.0 |
| SSH | Remote access | ✅ Configured |
| Node.js | Runtime | ✅ v22.22.1 |

### API Integrations
| Service | Status | Key |
|---------|--------|-----|
| OpenRouter | ✅ Active | Set |
| Brave Search | ✅ Active | BSA1VLq... |
| OpenAI | ⚠️ Verify | sk-proj... |
| GitHub | ✅ Active | SSH auth |

---

## PART 7: SECURITY NOTES

### Hardening Applied
- UFW Firewall: deny incoming, allow outgoing, SSH rate-limited
- SSH: Key-only auth, root disabled, X11 off
- Fail2ban: Active
- Daily security audit: 8:00 AM via cron

### SSH Access
```bash
# Add to ~/.ssh/config (on your local machine)
Host enki-server
    HostName YOUR-EC2-IP
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
```

---

## PART 8: QUICK REFERENCE

### Most Used Commands
```bash
openclaw status          # Check system status
openclaw gateway restart # Restart gateway
git push origin master:main  # Manual backup
node js-fetch.js <url>   # Scrape JavaScript site
pdftotext <file.pdf> -   # Read PDF to stdout
```

### File Locations
```
Workspace: ~/.openclaw/workspace/
Memory:     ~/.openclaw/memory/
Logs:       ~/.openclaw/logs/
Config:     ~/.openclaw/openclaw.json
Chat logs:  ~/.openclaw/agents/main/sessions/
PDF docs:   ~/.openclaw/media/inbound/
Skills:     ~/.openclaw/skills/
```

---

## PART 9: CONTACT & SUPPORT

- **OpenClaw Docs:** https://docs.openclaw.ai
- **OpenClaw Discord:** https://discord.com/invite/clawd
- **GitHub Issues:** https://github.com/openclaw/openclaw/issues

---

**Protocol Version:** 3.0  
**Last Updated:** 2026-03-12  
**Next Review:** After MVP build completion

*Save this file outside your server. Print it. Keep it accessible in emergencies.*
