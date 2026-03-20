#!/data/data/com.termux/files/usr/bin/bash
# Auto-backup script for ENKI workspace
# Created: 2026-03-20

BACKUP_DIR="/data/data/com.termux/files/home/.openclaw/workspace/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="enki_backup_${TIMESTAMP}.zip"

echo "[$(date -Iseconds)] Starting backup..."

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create backup (excluding venv, node_modules, .git)
cd /data/data/com.termux/files/home/.openclaw/workspace
zip -r "$BACKUP_DIR/$BACKUP_FILE" . \
  -x "venv/*" \
  -x "*/node_modules/*" \
  -x ".git/*" \
  -x "*/__pycache__/*" \
  -x "*.pyc" \
  -x "backups/*" \
  -x "ENKI_FULL_BACKUP_*.zip" \
  > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date -Iseconds)] Backup created: $BACKUP_FILE"
    # Keep only last 10 backups
    ls -t "$BACKUP_DIR"/enki_backup_*.zip 2>/dev/null | tail -n +11 | xargs rm -f
    echo "[$(date -Iseconds)] Backup complete. Size: $(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)"
else
    echo "[$(date -Iseconds)] Backup FAILED"
    exit 1
fi
