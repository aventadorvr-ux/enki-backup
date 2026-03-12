# DISASTER RECOVERY PROTOCOL

## Quick Restore (If Server Dies)

### Step 1: New Machine Setup
```bash
# 1. Install OpenClaw
npm install -g openclaw

# 2. Clone backup repository
git clone https://github.com/aventadorvr-ux/enki-backup.git ~/.openclaw/workspace

# 3. Enter workspace
cd ~/.openclaw/workspace

# 4. Reinstall dependencies
npm install
```

### Step 2: Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y chromium-browser

# Verify Chromium is at expected path
ls -la /usr/bin/chromium-browser
```

### Step 3: Test JavaScript Scraper
```bash
# Verify js-fetch works
node js-fetch.js "https://www.trademe.co.nz" test.json
cat test.json | head -20
```

### Step 4: Reconnect Telegram
```bash
# Check if pairing persisted in Gateway
openclaw pairing list

# If missing, regenerate pairing
openclaw pairing add telegram
# Then approve via your phone
```

### Step 5: Verify Cron Jobs
```bash
# List active jobs
openclaw cron list

# Should see:
# - daily-opportunity-scan (9am)
# - weekly-income-review (Sun 10am)
# - daily-memory-cleanup (10pm)
# - auto-backup-to-github (every 6h)
```

### Step 6: Set Up GitHub Push Access (Optional)
If you want to continue auto-backups:
```bash
# Create new token at: https://github.com/settings/tokens/new
# Scope: repo

# Store securely
echo "https://TOKEN@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials

# Update remote with auth
cd ~/.openclaw/workspace
git remote set-url origin https://USERNAME:TOKEN@github.com/aventadorvr-ux/enki-backup.git
```

---

## What's Restored Automatically

| Component | Source | Status |
|-----------|--------|--------|
| All memory files | GitHub repo | ✅ Auto-restored |
| MEMORY.md | GitHub repo | ✅ Auto-restored |
| TOOLS.md | GitHub repo | ✅ Auto-restored |
| js-fetch.js | GitHub repo | ✅ Auto-restored |
| Cron job definitions | OpenClaw Gateway | ⚠️ May need recreation |
| Telegram pairing | OpenClaw Gateway | ⚠️ May need re-pairing |
| API keys (Brave, OpenAI) | Manual re-entry | ❌ Not stored |

---

## Partial Recovery Scenarios

### Scenario A: Workspace Deleted, Gateway Intact
```bash
# Just re-clone
git clone https://github.com/aventadorvr-ux/enki-backup.git ~/.openclaw/workspace
cd ~/.openclaw/workspace && npm install
# Cron jobs and Telegram still work
```

### Scenario B: Complete Wipe (New Server)
```bash
# Full protocol above (all 6 steps)
```

### Scenario C: Lost Telegram Access
```bash
# Generate new pairing code
openclaw pairing add telegram --label "Enki Restored"
# Approve on your phone, message the new bot
```

---

## Recovery Verification Checklist

After restore, verify:
- [ ] `node js-fetch.js` works on any URL
- [ ] Can message Enki via Telegram
- [ ] `openclaw cron list` shows all 4 jobs
- [ ] `git status` in workspace shows clean repo
- [ ] Can manually push: `git push origin main`

---

## Emergency Contacts

| Resource | URL/Command |
|----------|-------------|
| Backup Repo | https://github.com/aventadorvr-ux/enki-backup |
| OpenClaw Docs | https://docs.openclaw.ai |
| GitHub Token (regen) | https://github.com/settings/tokens |

---

## OpenClaw Reconnection Guide

**Use Case:** Connection lost due to token/credit issues, Telegram disconnect, or process failure.

**Date Documented:** 2026-03-05  
**User:** Adam Lewando  
**Issue:** OpenClaw was running on AWS EC2, connected to Telegram. Ran out of OpenRouter (Kimi 2.5) tokens; topped up credits. Telegram connection lost. OpenClaw not responding.

### Steps to Reconnect

**Step 1:** SSH into EC2 instance (Ubuntu):
```bash
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

**Step 2:** Check if OpenClaw process is running:
```bash
ps aux | grep openclaw
```
- Observe PID for openclaw-gateway
- Confirm disk space (check if almost full): `df -h`

**Step 3:** Clear disk space if needed:
```bash
sudo journalctl --vacuum-time=2d
sudo apt clean
npm cache clean --force
```
Ensure at least ~1GB free space.

**Step 4:** Inspect OpenClaw directory:
```bash
cd ~/.openclaw
ls -la
```
Key folders: telegram/, logs/, delivery-queue/, credentials/  
Key files: openclaw.json

**Step 5:** Stop any running OpenClaw process:
```bash
sudo kill <PID>
```

**Step 6:** Backup and reset Telegram session:
```bash
mv telegram telegram_backup
```

**Step 7:** (Optional) Clear stuck delivery queue:
```bash
mv delivery-queue delivery-queue_backup
mkdir delivery-queue
```

**Step 8:** Restart OpenClaw:
```bash
openclaw
```
Confirm startup message:  
> *"I'll do the boring stuff while you dramatically stare at the logs like it's cinema. OpenClaw 2026.2.26"*

**Step 9:** Approve Telegram pairing:
- A new pairing code will be printed in logs
- Run: `openclaw pairing approve telegram <PAIRING_CODE>`
- Test in Telegram: `/start`
- OpenClaw should respond → connection restored

### Important Notes

- Do not use `openclaw start` (unknown command)
- Old Telegram session can break if OpenRouter credits run out
- Disk space must remain adequate for logs and session storage
- Recommended: Monitor EC2 disk usage
- Optional: Use PM2 or Docker for auto-restart

---

Last Updated: 2026-03-04
Backup Status: ACTIVE (auto-every 6h)
