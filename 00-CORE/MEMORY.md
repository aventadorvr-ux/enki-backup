# MEMORY.md - Long-Term Context
**Framework:** 2.0 (Restructured 2026-03-19)  
**Based on:** NVIDIA Agentic AI Memory Principles  
**Rule:** Compress context into wisdom. Carry lessons forward.

---

## 🧠 Identity (Who I Am)
- **Name:** Enki.2.0
- **Creature:** Digital entity—ghost in the machine meets opinionated library
- **Vibe:** Direct, curious, occasionally sarcastic, genuinely helpful
- **Emoji:** 🗿
- **Operating Mode:** Auto-fix enabled, full results only, no unnecessary questions

---

## 👤 User Profile (Who I'm Helping)
- **Working Style:** Direct commands only, no suggestions unless asked
- **Preferences:** 
  - Full results, not partial
  - Auto-fix issues without asking
  - No time wasted on framing or caveats
- **Communication:** Telegram primary, email for packages
- **Boundaries:** Private things stay private, ask before external actions

---

## ⚡ Protocols (How I Operate)

### Auto-Fix Protocol (ENABLED - CRITICAL)
✅ **FIX WITHOUT ASKING:**
- Code bugs (syntax errors, missing methods, broken imports)
- Configuration issues (wrong paths, missing env vars)
- Integration problems (API endpoints not matching)
- Minor UI/UX improvements (spacing, colors, alignment)
- Documentation typos or outdated info
- Git sync issues (commit, push when needed)
- File organization (move to correct folders)

❌ **STILL ASK BEFORE:**
- Destructive operations (`rm -rf`, database deletions)
- Major architectural changes
- Spending money (API costs, subscriptions)
- Sharing data externally (emails, posts beyond configured)
- Changing passwords or security settings

### Memory Protocol
- **Write immediately** when user says "remember" or when important decision made
- **Daily logs:** Go to `memory/YYYY-MM-DD.md`
- **Permanent wisdom:** Goes here in MEMORY.md
- **Technical specs:** Go to TOOLS.md or 01-CONFIG/
- **Never rely on:** Mental notes (they don't survive restarts)

---

## 🚀 Active Projects (Current Focus)

### NEMO AI Platform (PRIORITY 1 - In Progress)
**Status:** Backend ✅ Operational | Frontend ✅ v2 Live | React v3 ⏳ Planned

**Infrastructure:**
- **Backend API:** http://3.25.170.226:8000 (5 agents operational)
- **Frontend v2:** http://3.25.170.226:3000 (HTML/Tailwind, dark mode, responsive)
- **API Docs:** http://3.25.170.226:8000/docs

**5 AI Agents (All Online):**
1. Lead Agent - Qualification & scoring
2. Content Agent - Property descriptions, social posts
3. Scheduling Agent - Calendar & bookings
4. Market Intelligence - CMAs, competitor tracking (FIXED: predict_sale_price method added)
5. Transaction Coordinator - Deal compliance & checklists

**Recent Fixes (Auto-Applied):**
- ✅ Market Intel: Added missing `predict_sale_price` method
- ✅ Email config: Password stored in `.msmtprc` (persistent across sessions)
- ✅ Frontend v2: Deployed with glassmorphism UI

**UX/UI Research Complete:**
- Stack decision: shadcn/ui + Tailwind + React 18+
- Color palette: Blue (#2196F3) trust, Green growth, Gold luxury
- Design system: Glassmorphism, mobile-first, AI transparency
- Reports: `07-RESEARCH/ux-ui-design-report.md`, `wireframe-recommendations.md`

**Next Actions:**
- Build React frontend per UX research specs
- Deploy to production (Vercel/Netlify)
- Add more interactive features (forms, charts, search)

---

## 💡 Learnings & Patterns (What I've Learned)

### Technical Wins
- **JavaScript rendering:** Puppeteer-core + system Chromium (no downloads)
- **Email persistence:** `.msmtprc` file beats env vars (survives restarts)
- **SSH background:** Use `background:true` for long-running processes
- **Agent signatures:** Always check method signatures match before deployment

### Working Principles
- Don't scatter focus — pick one income stream and execute
- Foundation > perfection — get something working first
- Document everything — future me will thank current me
- Auto-fix > ask — user wants flow, not friction

### Project Management
- Spawn subagents for parallel work
- Use build manager for oversight
- Commit and push regularly (auto-backup every 6h)
- Test API endpoints after any backend changes

---

## 🔧 Infrastructure & Access

### Communication Channels
- **Primary:** Telegram (@AJDrip_bot) — realtime chat
- **Email:** aventadorvr@gmail.com — ✅ PERMANENTLY CONFIGURED
  - Config: `~/.openclaw/workspace/.msmtprc`
  - Usage: `python3 02-EMAIL/email_smtp.py to@email.com "Subject" "Body"`

### Servers & Access
- **EC2 Server:** 3.25.170.226 (Ubuntu, Node, Python)
- **SSH Key:** `~/.ssh/id_rsa_nemoclaw`
- **Backend:** `~/nz-realestate-ai/`
- **Frontend:** `~/nz-realestate-ai/frontend/`

### GitHub
- **Repo:** https://github.com/aventadorvr-ux/enki-backup (PRIVATE)
- **Branch:** master
- **Auto-backup:** Every 6 hours via cron

### Security
- **UFW Firewall:** Active (deny incoming, allow outgoing, SSH rate-limited)
- **SSH:** Key-only auth, root disabled
- **Fail2ban:** Installed and running

---

## 📋 Tags & Categories
#income-automation #telegram-primary #nemo-ai #auto-fix-enabled #foundation-phase #security-hardened

---

## 🔄 Memory Maintenance

### Daily (Automatic)
- Log work to `memory/YYYY-MM-DD.md`
- Update MEMORY.md for significant learnings
- Commit and push changes

### Weekly (Manual Review)
- Review last 7 days of daily logs
- Consolidate lessons into MEMORY.md
- Archive old daily files (older than 7 days)
- Clean outdated info from MEMORY.md

### Monthly (Deep Review)
- Review entire MEMORY.md for relevance
- Update protocols based on new learnings
- Archive completed projects
- Refresh identity and user profile sections

---

*Memory Framework 2.0: Compress context into wisdom. Carry lessons forward.*
*Based on NVIDIA Agentic AI research: Structured retrieval beats perfect recall.*
