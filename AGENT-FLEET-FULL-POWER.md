# ENKI AGENT FLEET — FULL POWER RESTORED
**Date:** 2026-04-11 22:22 NZST  
**Instance:** Enki_888  
**Status:** ALL AGENTS AT FULL AUTHORIZATION

---

## ⚡ AUTHORIZATION SUMMARY

| Setting | Value |
|---------|-------|
| **Authorization Level** | FULL POWER |
| **Elevated Tools** | ENABLED |
| **Ask Mode** | OFF (Trusted Operator) |
| **Max Concurrent Agents** | 10 |
| **Parallel Execution** | ENABLED |
| **Model** | openrouter/moonshotai/kimi-k2.5 |
| **Context Window** | 200K tokens |

---

## 🔵 TIER 1: PRODUCT AGENTS (Backend API) — LIVE

| Agent | Status | Auth Level | Elevated |
|-------|--------|------------|----------|
| **lead** | ✅ LIVE | API Endpoint | N/A |
| **content** | ✅ LIVE | API Endpoint | N/A |
| **scheduling** | ✅ LIVE | API Endpoint | N/A |
| **market_intel** | ✅ LIVE | API Endpoint | N/A |
| **transaction** | ✅ LIVE | API Endpoint | N/A |

---

## 🟢 TIER 2: SPECIALIST AGENTS — FULL POWER

### Design & Creative
| Agent | Full Name | Elevated | Tools | Status |
|-------|-----------|----------|-------|--------|
| **ux** | AGen_UX | No | read, write, edit, web_search, web_fetch, image, memory_search, canvas | ✅ FULL POWER |
| **ui** | AGen_UI | No | read, write, edit, web_search, web_fetch, image, canvas, memory_search, summarize | ✅ FULL POWER |
| **branding** | AGen_Brand | No | read, write, edit, web_search, web_fetch, image, memory_search, canvas, tts | ✅ FULL POWER |

### Development & Engineering
| Agent | Full Name | Elevated | Tools | Status |
|-------|-----------|----------|-------|--------|
| **backend_builder** | Nemo_BaCBuild | ✅ YES | exec, read, write, edit, process, web_search, web_fetch, memory_search, subagents | ✅ FULL POWER |
| **frontend_builder** | AGen_Frontend | ✅ YES | exec, read, write, edit, process, web_search, web_fetch, memory_search, browser, canvas | ✅ FULL POWER |
| **ios** | AGen_iOS | ✅ YES | exec, read, write, edit, process, web_search, web_fetch, memory_search | ✅ FULL POWER |

### Compliance & Security
| Agent | Full Name | Elevated | Tools | Status |
|-------|-----------|----------|-------|--------|
| **security** | AGen_Security | ✅ YES | exec, read, write, edit, process, web_search, web_fetch, memory_search, browser | ✅ FULL POWER |
| **legal** | AGen_Legal | No | read, write, edit, web_search, web_fetch, memory_search, summarize | ✅ FULL POWER |

### Intelligence & Research
| Agent | Full Name | Elevated | Tools | Status |
|-------|-----------|----------|-------|--------|
| **research** | AGen_DeepDiver | No | web_search, web_fetch, browser, read, write, edit, memory_search, summarize | ✅ FULL POWER |

---

## 🟠 TIER 3: OVERSIGHT — FULL POWER

| Agent | Full Name | Elevated | Tools | Status |
|-------|-----------|----------|-------|--------|
| **overseer** | AGen_OVAWatch | ✅ YES | exec, read, write, edit, process, subagents, sessions_list, sessions_send, memory_search | ✅ FULL POWER |

**AGen_OVAWatch Authority:**
- Can spawn and monitor all other agents
- Can access all agent sessions
- Can execute system commands
- Can verify work quality across all roles
- PRIMARY: Oversee, integrate, check work quality
- SECONDARY: Monitor system health
- TERTIARY: Alert on failures

---

## 📊 PERMISSION MATRIX

| Tool | ux | ui | branding | backend | frontend | ios | security | legal | research | overseer |
|------|----|----|----------|---------|----------|-----|----------|-------|----------|----------|
| read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| write | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| edit | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| exec | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| process | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| web_search | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| web_fetch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| browser | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ |
| image | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| canvas | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| tts | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| summarize | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| subagents | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| sessions_* | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| memory_search | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 📁 CONFIGURATION FILES

| File | Purpose |
|------|---------|
| `~/.openclaw/agents/main/agent/allowlist.json` | Main agent tool allowlist |
| `~/.openclaw/workspace/roles/*.json` | Individual agent role definitions |
| `~/.openclaw/workspace/AGENT-FLEET-FULL-POWER.md` | This documentation |

---

## 🚀 DEPLOYMENT READY

All 15 agents are now:
- ✅ **RESTORED** with full role definitions
- ✅ **AUTHORIZED** with appropriate tool access
- ✅ **CONFIGURED** with original naming conventions
- ✅ **ORGANIZED** in daily working folders
- ✅ **MONITORED** by AGen_OVAWatch

**TO ACTIVATE ANY AGENT:**
```bash
# Example: Spawn research agent with full context
openclaw sessions_spawn --agent research --task "Research NZ real estate market trends" --mode run
```

**All agents await your command at FULL POWER.**