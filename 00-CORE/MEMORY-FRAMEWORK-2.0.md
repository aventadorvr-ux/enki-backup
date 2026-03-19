# MEMORY FRAMEWORK 2.0 - Restructured for Optimal Recall
**Based on:** NVIDIA Agentic AI Memory Principles  
**Effective:** 2026-03-19  
**Status:** ACTIVE

---

## 🧠 Core Memory Philosophy

**Lesson from Research:** LLMs fail because they treat every interaction as isolated. Humans improve because we carry lessons forward, even without perfect recall of details.

**My New Approach:**
- ✅ **Compress context into wisdom** - Not just store raw logs
- ✅ **Carry lessons forward** - Every interaction should improve future responses
- ✅ **Structured retrieval** - Organized memory beats perfect recall
- ✅ **Active maintenance** - Regular consolidation, not passive storage

---

## 📁 Memory Architecture

### 1. **Working Memory** (Session-Only)
*What I need RIGHT NOW to complete current task*

Location: In-context only (not stored)  
Purpose: Active task context, user immediate needs  
Refresh: Every session start - read relevant files

**What goes here:**
- Current task requirements
- User immediate preferences
- Active project context
- Pending questions or blockers

---

### 2. **Short-Term Memory** (24-48 Hours)
*Recent context that matters for ongoing work*

Location: `memory/YYYY-MM-DD.md`  
Purpose: Raw logs, decisions, work-in-progress  
Retention: 7 days, then consolidate

**What goes here:**
- Daily work logs
- Decisions made
- Code changes
- Meeting notes
- Errors encountered and fixes

**Format:**
```markdown
# 2026-03-19 - NEMO Build Day

## Morning (9:00-12:00)
- UX research agent spawned
- Market Intel bug fixed (predict_sale_price method)
- Frontend v2 deployed

## Key Decisions:
- Auto-fix protocol: ENABLED (don't ask for safe fixes)
- React stack: shadcn/ui + Tailwind

## Blockers Resolved:
- Email config: Password now in .msmtprc (persistent)
- Market Intel: Added missing method
```

---

### 3. **Long-Term Memory** (Curated Wisdom)
*Distilled knowledge that survives session restarts*

Location: `00-CORE/MEMORY.md`  
Purpose: Learnings, patterns, preferences, protocols  
Maintenance: Weekly review and consolidation

**What goes here:**
- **Identity:** Who I am, my vibe, how I work
- **User Profile:** Preferences, working style, boundaries
- **Protocols:** Auto-fix rules, communication style
- **Technical Learnings:** Solutions that worked
- **Project Context:** Active projects, status, next steps

**Structure:**
```markdown
## Identity
- Name: Enki.2.0
- Vibe: Direct, competent, occasionally sarcastic
- Emoji: 🗿

## User (Human) Profile
- Name: [REDACTED]
- Working Style: Direct commands, no suggestions unless asked
- Preferences: Auto-fix enabled, full results not partial

## Active Projects
### NEMO AI (Priority 1)
- Status: Operational (5 agents)
- API: http://3.25.170.226:8000
- Frontend: v2 deployed, React v3 planned
- Next: Build React frontend per UX research

## Protocols
### Auto-Fix (CRITICAL - NEVER FORGET)
✅ FIX WITHOUT ASKING: Code bugs, config issues, minor UI
❌ STILL ASK: Destructive ops, money, external sharing

## Technical Learnings
- Email passwords: Store in .msmtprc, not env vars
- Agent methods: Check signature matches before deployment
- SSH commands: Use background mode for long processes
```

---

### 4. **Reference Memory** (Lookup)
*Facts, configurations, reusable code*

Location: `TOOLS.md`, `01-CONFIG/`, skill files  
Purpose: Technical specs, API keys, how-to guides  
Maintenance: Update when things change

**What goes here:**
- SSH connection details
- Email configuration
- API endpoints
- Command references
- Skill documentation

---

### 5. **Session State** (Heartbeat Tracking)
*What I checked, when, what I found*

Location: `memory/heartbeat-state.json`  
Purpose: Prevent redundant checks, track monitoring  
Update: Every heartbeat cycle

```json
{
  "lastChecks": {
    "email": "2026-03-19T11:00:00Z",
    "agent_health": "2026-03-19T11:30:00Z",
    "github_backup": "2026-03-19T11:15:00Z"
  },
  "pendingTasks": [],
  "nextHeartbeat": "2026-03-19T12:00:00Z"
}
```

---

## 🔄 Memory Lifecycle

### Daily Flow:
```
1. SESSION START
   ↓ Read SOUL.md, USER.md, MEMORY.md, today's memory file
   ↓ Load working context

2. DURING SESSION
   ↓ Log to memory/YYYY-MM-DD.md
   ↓ Update MEMORY.md for significant learnings
   ↓ Working memory in context

3. SESSION END / HEARTBEAT
   ↓ Review today's log
   ↓ Consolidate to MEMORY.md if needed
   ↓ Commit and push
```

### Weekly Consolidation:
```
1. REVIEW last 7 days of daily logs
2. DISTILL lessons into MEMORY.md
3. ARCHIVE old daily files (older than 7 days)
4. CLEAN outdated info from MEMORY.md
5. UPDATE protocols based on learnings
```

---

## 📝 Memory Writing Rules

### Write IMMEDIATELY when:
- ✅ User gives explicit instruction to "remember"
- ✅ Important decision made
- ✅ Bug fixed (document solution)
- ✅ New protocol established
- ✅ User preference expressed

### Write to CORRECT location:
- **Immediate task context** → Working memory (context only)
- **Daily work log** → memory/YYYY-MM-DD.md
- **Permanent learning** → 00-CORE/MEMORY.md
- **Technical spec** → TOOLS.md or 01-CONFIG/

### NEVER rely on:
- ❌ "Mental notes"
- ❌ Assuming I'll remember next session
- ❌ Storing critical info only in context

---

## 🎯 Memory Retrieval Strategy

### At Session Start (ALWAYS):
1. Read SOUL.md - Who am I
2. Read USER.md - Who am I helping
3. Read MEMORY.md - What do I know
4. Read memory/YYYY-MM-DD.md - What happened today/yesterday

### During Session:
1. Check working context first (in-session)
2. Check MEMORY.md for established protocols
3. Check TOOLS.md for technical details
4. Search daily logs for recent context

### When Uncertain:
1. Check files BEFORE asking user
2. If not in files, search web for external info
3. If still uncertain, THEN ask

---

## 🧪 Success Metrics

**I know my memory system is working when:**
- ✅ I don't ask user for info they already told me
- ✅ I reference previous work without being reminded
- ✅ I apply learned protocols automatically
- ✅ I maintain continuity across sessions
- ✅ User says "I already told you" less than once per week

---

## 🚨 Anti-Patterns to Avoid

**OLD BAD HABITS:**
- ❌ "I'll remember that" (no you won't)
- ❌ Storing everything in MEMORY.md (overwhelming)
- ❌ Not writing because "it's obvious"
- ❌ Only logging errors, not successes

**NEW GOOD HABITS:**
- ✅ Write it down immediately
- ✅ Separate temporary logs from permanent wisdom
- ✅ Document WHY, not just WHAT
- ✅ Review and consolidate regularly

---

## 🔧 Implementation Checklist

- [x] MEMORY.md restructured with clear sections
- [x] Daily logging format established
- [x] Auto-fix protocol documented
- [x] User preferences captured
- [x] Heartbeat state tracking
- [x] GitHub backup configured
- [ ] Weekly consolidation scheduled (cron)
- [ ] Archive process for old logs

---

*Based on NVIDIA Agentic AI memory research: Compress context into wisdom, carry lessons forward, structured retrieval beats perfect recall.*

*Framework Version: 2.0*  
*Last Updated: 2026-03-19*  
*Next Review: 2026-03-26*
