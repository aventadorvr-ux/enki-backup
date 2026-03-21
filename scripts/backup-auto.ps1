#!/bin/bash
# Auto-backup script for Windows OpenClaw workspace
# Runs every 30 minutes via heartbeat
# Created: 2026-03-22

REPO_DIR="C:/Users/enkir/.openclaw/workspace"
LOG_FILE="$REPO_DIR/logs/backup.log"

# Create log directory if not exists
mkdir -p "$REPO_DIR/logs"

echo "[$(date -Iseconds)] Starting auto-backup..." >> "$LOG_FILE"

cd "$REPO_DIR"

# Check if there are changes to commit
if git diff --quiet HEAD && git diff --cached --quiet; then
    echo "[$(date -Iseconds)] No changes to backup" >> "$LOG_FILE"
    exit 0
fi

# Add all changes
git add -A

# Commit with timestamp
COMMIT_MSG="Auto-backup: $(date -u +%Y-%m-%d-%H%M)"
git commit -m "$COMMIT_MSG" >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date -Iseconds)] ✅ Backup committed: $COMMIT_MSG" >> "$LOG_FILE"
    
    # Push to GitHub (with error handling)
    git push origin master >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "[$(date -Iseconds)] ✅ Pushed to GitHub" >> "$LOG_FILE"
    else
        echo "[$(date -Iseconds)] ⚠️ Push failed - will retry next cycle" >> "$LOG_FILE"
    fi
else
    echo "[$(date -Iseconds)] ❌ Commit failed" >> "$LOG_FILE"
    exit 1
fi

echo "[$(date -Iseconds)] Backup complete" >> "$LOG_FILE"
