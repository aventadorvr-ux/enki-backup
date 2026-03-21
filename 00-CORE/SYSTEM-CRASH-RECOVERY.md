# SYSTEM CRASH RECOVERY PROTOCOL
## Automatic Restore Procedures

**Last Updated:** 2026-03-20
**Status:** ACTIVE

---

## TRIGGER: System Crash / Service Down / Agent Failure

### IMMEDIATE ACTIONS (Do NOT ask - just execute)

#### 1. System Health Check (30 seconds)
```bash
# Check core services
- SSH to NEMO server
- Verify API endpoints
- Check local OpenClaw status
- Test Telegram connectivity
```

#### 2. Agent Status Verification (1 minute)
```
FOR EACH AGENT:
- Check if process is running
- Test API endpoint
- If DOWN → Restart immediately
- Log restart event
```

#### 3. Workspace Integrity (1 minute)
```
- Git status check
- Identify uncommitted changes
- Emergency backup if needed
- Verify .gitignore excludes node_modules
```

#### 4. Protocol Update (Always)
```
- Document what failed
- Update this recovery protocol
- Commit changes
```

---

## AGENT FLEET STATUS

### Current Active Agents

| Agent | Location | Status | Restart Command |
|-------|----------|--------|-----------------|
| **AGen_OVAWatch** | NEMO:~/enki-agentic | CHECK | `sudo systemctl restart enki-ovawatch` |
| **Lead_Terminator** | NEMO:~/enki-agentic | CHECK | `sudo systemctl restart enki-lead` |
| **Content_Forge** | NEMO:~/enki-agentic | CHECK | `sudo systemctl restart enki-content` |
| **AGen_Legal** | NEMO:~/enki-agentic | CHECK | `sudo systemctl restart enki-legal` |
| **Telegram_Bot** | NEMO:~/enki-agentic | CHECK | `sudo systemctl restart enki-telegram` |

### Verification Endpoints
- Health: `http://3.25.170.226:8000/health`
- Agents: `http://3.25.170.226:8000/api/v1/agents`
- SSH: `ssh -i ~/.ssh/id_rsa_nemoclaw ubuntu@3.25.170.226`

---

## AUTOMATIC RECOVERY SCRIPT

Location: `~/.openclaw/workspace/scripts/auto-recovery.sh`

```bash
#!/bin/bash
# Auto-recovery on crash - DO NOT MODIFY

echo "[$(date)] Starting crash recovery..."

# 1. Check NEMO server
if ! ssh -o ConnectTimeout=5 -i ~/.ssh/id_rsa_nemoclaw ubuntu@3.25.170.226 "echo 'OK'" > /dev/null 2>&1; then
    echo "[ERROR] NEMO server unreachable"
    # Send alert
    curl -d "NEMO DOWN" ntfy.sh/enki-alerts 2>/dev/null
fi

# 2. Restart all agents
ssh -i ~/.ssh/id_rsa_nemoclaw ubuntu@3.25.170.226 "sudo systemctl restart enki-*" 2>/dev/null

# 3. Verify
sleep 5
HEALTH=$(curl -s http://3.25.170.226:8000/health 2>/dev/null | grep -o '"status":"healthy"')
if [ "$HEALTH" ]; then
    echo "[OK] All systems restored"
else
    echo "[ERROR] Restoration failed"
fi

echo "[$(date)] Recovery complete"
```

---

## POST-CRASH CHECKLIST

- [ ] All agents running
- [ ] API responding
- [ ] Telegram bot connected
- [ ] Git backup completed
- [ ] Memory files updated
- [ ] Protocol updated with lessons learned
- [ ] Report sent to user

---

## NEXT CRASH

**I will:**
1. Run recovery automatically
2. Report status only
3. No questions during recovery
4. Document what broke

**You will:**
1. Get a status report
2. Tell me what to prioritize
3. Continue normal operations
