# NEMO PROTOCOL: Hourly Revision Scan, Confirm, Correct, Debug

**Effective Date:** 2026-03-19  
**Applies To:** Nemo (Claude Code sub-agent)  
**Frequency:** Every hour during active development  
**Location:** EC2 Instance (3.25.170.226)

---

## 🎯 PROTOCOL OBJECTIVE

**Catch bugs early. Confirm code quality hourly. Avoid massive rewrites.**

This protocol ensures every hour of coding work is validated before proceeding, preventing technical debt accumulation and reducing debugging time by 70%+.

---

## ⏰ HOURLY CHECKPOINT PROTOCOL

### BEFORE You Start Each Hour:

```bash
# 1. Run the protocol manually (or it runs automatically via cron)
~/nemo-protocol.sh

# 2. Review the output
cat ~/logs/nemo-hourly-scan.log | tail -100
```

---

## 🔍 7-POINT SCAN CHECKLIST

### 1. CODE QUALITY SCAN ✅
**Purpose:** Catch syntax errors and code smells

**What to Check:**
- [ ] Python syntax compiles without errors
- [ ] No bare `except:` clauses (use `except Exception:`)
- [ ] No `print()` statements (use `logger`)
- [ ] No TODO/FIXME/XXX comments left unresolved
- [ ] Proper error handling in place

**Command:**
```bash
find . -name '*.py' -not -path './venv/*' -exec python3 -m py_compile {} \;
```

**If Errors Found:**
- STOP current work
- Fix syntax errors FIRST
- Re-run scan before continuing

---

### 2. API HEALTH CHECK ✅
**Purpose:** Ensure backend is functional

**What to Check:**
- [ ] `/health` endpoint returns `{"status": "healthy"}`
- [ ] All 5 agent endpoints respond (HTTP 200 or 500)
- [ ] No 500 errors on basic requests

**Commands:**
```bash
curl http://localhost:8000/health
for agent in lead content scheduling market_intel transaction; do
  curl -X POST http://localhost:8000/api/v1/agents/$agent/process \
    -H 'Content-Type: application/json' \
    -d '{"action": "health_check"}'
done
```

**If API Down:**
- Check server logs: `tail -50 ~/nz-realestate-ai/server.log`
- Restart if needed: `pkill -f uvicorn && ./restart.sh`

---

### 3. GIT STATUS CHECK ✅
**Purpose:** Track changes and commit regularly

**What to Check:**
- [ ] No uncommitted changes older than 1 hour
- [ ] Meaningful commit messages
- [ ] Working in feature branches if needed

**Rule: Commit Every Hour (Minimum)**
```bash
git add -A
git commit -m "feat: descriptive message - $(date +%H:%M)"
```

**Commit Message Format:**
- `feat:` new feature
- `fix:` bug fix
- `refactor:` code restructuring
- `docs:` documentation
- `test:` adding tests

**If Uncommitted:**
- Commit immediately with descriptive message
- Push to remote: `git push origin master`

---

### 4. DEPENDENCY CHECK ✅
**Purpose:** Avoid dependency conflicts

**What to Check:**
- [ ] No pip conflicts: `pip check`
- [ ] All imports resolve
- [ ] requirements.txt is current

**Command:**
```bash
source venv/bin/activate
pip check
pip freeze > requirements.txt  # If new packages added
git diff requirements.txt  # Review changes
```

**If Conflicts:**
- Resolve before adding new features
- Document version constraints

---

### 5. TEST EXECUTION ✅
**Purpose:** Validate functionality

**What to Check:**
- [ ] All tests pass
- [ ] New code has tests
- [ ] Test coverage maintained

**Command:**
```bashnpython3 -m pytest tests/ -v --tb=short
```

**If Tests Fail:**
- Fix failures immediately
- Don't commit broken tests
- Add tests for new features

---

### 6. ERROR LOG ANALYSIS ✅
**Purpose:** Catch runtime errors

**What to Check:**
- [ ] No ERROR or Traceback in recent logs
- [ ] No memory leaks (growing RAM usage)
- [ ] No connection failures to Redis/APIs

**Command:**
```bash
tail -1000 ~/nz-realestate-ai/server.log | grep -E 'ERROR|Traceback' | tail -10
```

**If Errors Found:**
- Analyze error patterns
- Fix root cause
- Verify fix with fresh logs

---

### 7. SUMMARY & ACTION ITEMS ✅
**Purpose:** Clear next steps

**Before Continuing, Ask:**
1. Is the code syntactically correct?
2. Does the API respond correctly?
3. Are changes committed?
4. Do tests pass?
5. Are there any errors in logs?

**Action Priority:**
- 🔴 CRITICAL: Syntax errors, API down → FIX IMMEDIATELY
- 🟡 WARNING: Uncommitted changes, test failures → Fix before next hour
- 🟢 OK: All checks pass → Continue development

---

## 🚨 ESCALATION PROTOCOL

### When to STOP and ASK:

1. **Syntax errors that can't be fixed in 5 minutes**
2. **API crashes after restart**
3. **Git merge conflicts**
4. **Database migration failures**
5. **Dependency conflicts that break the system**
6. **More than 10 test failures**

**Action:**
- Document the error
- Stop current work
- Report to Enki (main agent) with logs

---

## 📊 HOURLY LOG FORMAT

Each scan produces a log entry:

```
2026-03-19 14:00:00 - === HOURLY REVISION SCAN STARTED ===
2026-03-19 14:00:01 - --- 1. Code Quality Scan ---
2026-03-19 14:00:02 - ✅ Python syntax: OK
2026-03-19 14:00:03 - --- 2. API Health Check ---
2026-03-19 14:00:04 - ✅ API Health: OK
2026-03-19 14:00:05 - ✅ Agent lead: Responding (HTTP 200)
...
2026-03-19 14:00:30 - === HOURLY SCAN COMPLETED ===
```

**View Logs:**
```bash
tail -f ~/logs/nemo-hourly-scan.log
```

---

## 🔄 AUTOMATED VS MANUAL

### Automated (Every Hour via Cron):
- Basic health checks
- Syntax validation
- API endpoint tests
- Error log scanning

### Manual (You Must Do):
- Code review of changes
- Test writing for new features
- Dependency updates documentation
- Commit with meaningful messages

---

## 📝 DEVELOPMENT WORKFLOW

```
┌─────────────────────────────────────────────────────────────┐
│  START HOUR                                                 │
│  ↓                                                          │
│  Run ~/nemo-protocol.sh (or check last hourly run)         │
│  ↓                                                          │
│  ALL CHECKS PASS?                                           │
│  ├─ YES → Continue development                             │
│  └─ NO  → Fix issues first                                 │
│           ↓                                                 │
│           Re-run protocol                                   │
│           ↓                                                 │
│           Continue                                          │
│  ↓                                                          │
│  CODE FOR 1 HOUR                                            │
│  ↓                                                          │
│  Run protocol again                                         │
│  ↓                                                          │
│  Commit changes                                             │
│  ↓                                                          │
│  NEXT HOUR                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ QUALITY GATES

**Before ANY commit:**
1. ✓ Code compiles
2. ✓ API responds
3. ✓ No new ERRORs in logs
4. ✓ Tests pass (or updated)
5. ✓ Meaningful commit message

**Before END of session:**
1. ✓ All changes committed
2. ✓ Pushed to GitHub
3. ✓ API left running and healthy
4. ✓ Documentation updated
5. ✓ No uncommitted WIP files

---

## 🎯 SUCCESS METRICS

**Target:**
- Zero syntax errors caught in production
- API uptime > 99%
- Test coverage > 80%
- Average bug fix time < 15 minutes
- Commit frequency: Every 1-2 hours

---

## 🔧 TOOLS INSTALLED

**On EC2 Instance:**
- `~/nemo-protocol.sh` - Hourly scan script
- Cron job: `0 * * * * ~/nemo-protocol.sh`
- Logs: `~/logs/nemo-hourly-scan.log`
- `~/logs/nemo-cron.log` (cron output)

---

## 📞 COMMUNICATION

**Report Issues To:**
- Enki (main agent) via Telegram/SSH
- Include: Error logs, git status, last commit
- Tag with: [NEMO-PROTOCOL] [PRIORITY]

---

## ✍️ SIGN-OFF

By following this protocol, Nemo commits to:
1. Hourly code quality validation
2. Immediate bug fixing
3. Regular commits with clear messages
4. Maintaining API stability
5. Escalating blockers promptly

**Result:** Clean codebase, fewer bugs, faster development.

---

**Protocol Version:** 1.0  
**Last Updated:** 2026-03-19 05:08 UTC  
**Next Review:** As needed
