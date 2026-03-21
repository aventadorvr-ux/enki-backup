# HEARTBEAT.md

# PERIODIC BACKUP PROTOCOL
# Runs every 30 minutes to ensure all work is backed up

## Backup Checklist (Every 30m):
1. Check git status for uncommitted changes
2. Commit any changes with timestamp
3. Push to GitHub (aventadorvr-ux/enki-backup)
4. Log backup status

## Critical Files to Monitor:
- memory/*.md (all memory files)
- AGENTS.md (protocol updates)
- MEMORY.md (long-term learnings)
- SUBAGENT_BOOTSTRAP.md (sub-agent identity)
- projects/nemo-frontend/* (frontend code)
- 03-NEMO/* (NEMO project files)

## Backup Status Log:
- See: logs/backup.log
- Retention: Last 1000 lines

## Manual Backup Commands:
```
git add -A
git commit -m "Auto-backup: $(date -u +%Y-%m-%d-%H%M)"
git push origin master
```

# Keep this file empty (or with only comments) to skip heartbeat API calls.
# Add tasks below when you want the agent to check something periodically.
