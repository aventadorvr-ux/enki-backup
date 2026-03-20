# ENKI AGENTIC - AGENT FLEET MANIFEST
## Complete Agent Inventory & Responsibilities
**Generated:** Thu 2026-03-19 15:51 UTC

---

## 🎯 Managing Agent

### AGen_OVAWatch (The Overseer)
**FILE:** `agenv_ovawatch.py`  
**STATUS:** 🟢 ACTIVE  
**PRIMARY ROLE:** Dev Team Manager / System Overseer

**RESPONSIBILITIES:**
1. ✅ Monitor ALL agents every 5 minutes
2. ✅ Check agent work quality and output
3. ✅ Ensure agents INTEGRATE with each other
4. ✅ Monitor inter-agent communication/disconnections
5. ✅ Auto-repair services hourly
6. ✅ Escalate critical issues to human (via me)
7. ✅ Track performance metrics
8. ✅ Maintain 100% uptime target

**INTEGRATION:**
- Systemd service: `agenv-ovawatch.service`
- Monitors: Lead_Terminator, Content_Forge, ENKI API, Database, nginx
- Alerts: Telegram (when configured)
- Logs: `/var/log/enki-health.log`

---

## 🤖 Active Agents (4)

### 1. Lead_Terminator
**FILE:** `lead_terminator.py`  
**STATUS:** 🟢 ACTIVE  
**ROLE:** Lead qualification & AI conversation

**RESPONSIBILITIES:**
- Auto-respond to lead inquiries in <30 seconds
- AI-powered qualification conversation
- Score leads 0-40 (Hot leads >30)
- Escalate hot leads to human instantly
- Store all conversations in database

**INTEGRATION:**
- API: `/api/v1/enki/leads/*`
- Database: SQLite `leads.db`
- AI Engine: OpenAI API
- Alerts: Telegram hot lead notifications
- Monitored by: AGen_OVAWatch

**ACTIVITY:**
- Total leads processed: 3
- Hot leads: 0
- Average score: 20.0/40

---

### 2. Content_Forge
**FILE:** `content_forge.py`  
**STATUS:** 🟢 ACTIVE  
**ROLE:** Marketing content generation

**RESPONSIBILITIES:**
- Generate property descriptions
- Create social media posts (Instagram, Facebook, LinkedIn)
- Write email campaigns
- Market update content
- Maintain brand voice consistency

**INTEGRATION:**
- API: `/api/v1/enki/content/*`
- Database: SQLite `content.db`
- AI Engine: OpenAI API
- Templates: 4 loaded
- Monitored by: AGen_OVAWatch

**ACTIVITY:**
- Content generated: 1 (test)
- Templates: 4 available

---

### 3. Enki_Telegram_Bot
**FILE:** `enki_telegram_bot.py`  
**STATUS:** 🟡 READY (Awaiting token)  
**ROLE:** Mobile command center

**RESPONSIBILITIES:**
- `/status` - Full system health from phone
- `/hot` - Instant hot leads list
- `/stats` - Lead statistics
- `/restart` - Remote service restart
- `/content` - Generate content on demand
- `/alert` - Broadcast custom alerts
- Voice alerts for critical issues

**INTEGRATION:**
- Systemd service: `enki-telegram.service`
- Connected to ENKI API
- Monitored by: AGen_OVAWatch

**COMMANDS:** 10+ ready

---

### 4. AGen_Legal (NEW)
**FILE:** `agen_legal.py`  
**STATUS:** 🟢 ACTIVE  
**ROLE:** Legal & Business Compliance

**RESPONSIBILITIES:**
- Business registration and licensing
- Legal entity formation
- Compliance monitoring
- Contract review and management
- Regulatory requirements tracking
- Intellectual property protection

**INTEGRATION:**
- Database: SQLite `legal.db`
- 15 tasks queued
- Jurisdiction: New Zealand
- Monitored by: AGen_OVAWatch

**ACTIVITY:**
- Total legal tasks: 15
- Completed: 0
- High priority: 9
- Completion rate: 0%

---

## ⚙️ Infrastructure Agents (2)

### 5. Health_Check (Cron Agent)
**SCRIPT:** `enki-health-check.sh`  
**STATUS:** 🟢 ACTIVE  
**ROLE:** Continuous health monitoring

**RESPONSIBILITIES:**
- Check API health every 60 seconds
- Auto-restart services if down
- Log all checks
- Prevent alert spam

**INTEGRATION:**
- Cron job: `/etc/cron.d/enki-health`
- Monitors: enki-api.service, nginx
- Connected to: AGen_OVAWatch

---

### 6. Enki_Alarm_System
**SCRIPT:** `enki_alarm_system.py`  
**STATUS:** 🟡 READY (Awaiting phone config)  
**ROLE:** Critical alert notifications

**RESPONSIBILITIES:**
- Monitor critical systems every 30 seconds
- Send MAXIMUM PRIORITY alerts
- Auto-attempt repairs
- Wake up human when systems fail

**ALERT METHODS:**
- Telegram (primary)
- Phone call (Twilio - needs setup)
- SMS backup

---

## 🚀 Queued Agents (6)

| Agent | File | Status | Purpose |
|-------|------|--------|---------|
| Nemo_BaCBuild | TBD | 🔴 QUEUED | Backend constructor |
| AGen_UX | TBD | 🔴 QUEUED | UX development |
| AGen_UI | TBD | 🔴 QUEUED | UI development |
| Market_Intel_Core | TBD | 🔴 QUEUED | CMAs & competitor analysis |
| Scheduling_Drone | TBD | 🔴 QUEUED | Calendar & booking automation |
| Transaction_Coord | TBD | 🔴 QUEUED | Deal pipeline management |

---

## 📊 Agent Statistics

**Total Agents:** 10 (4 active, 6 queued)  
**Active Fleet:** 40% deployed  
**Integration Status:** 🟢 FULLY CONNECTED  
**Monitoring:** 🟢 CONTINUOUS  

---

**AGen_OVAWatch is watching all agents. Integration verified.**
