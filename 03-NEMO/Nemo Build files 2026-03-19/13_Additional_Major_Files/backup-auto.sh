#!/data/data/com.termux/files/usr/bin/bash
# Auto-backup script with token-based auth

REPO_DIR="/data/data/com.termux/files/home/.openclaw/workspace"
GITHUB_USER="aventadorvr-ux"
REPO_NAME="enki-backup"
TOKEN_FILE="/data/data/com.termux/files/home/.openclaw/.github_token"

# Load token if exists
if [ -f "$TOKEN_FILE" ]; then
    source "$TOKEN_FILE"
fi

if [ -z "$GITHUB_TOKEN" ] || [ "$GITHUB_TOKEN" = "YOUR_TOKEN_HERE" ]; then
    echo "❌ GitHub token not configured"
    echo "   1. Generate token: https://github.com/settings/tokens"
    echo "   2. Edit: $TOKEN_FILE"
    echo "   3. Replace YOUR_TOKEN_HERE with your token"
    exit 1
fi

cd "$REPO_DIR"

# Configure git URL with token
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"

# Add all changes
git add -A

# Commit with timestamp
COMMIT_MSG="Auto-backup: $(date -u +%Y-%m-%d-%H%M)"
if ! git diff --cached --quiet; then
    git commit -m "$COMMIT_MSG"
    git push origin master
    echo "✅ Backup complete: $COMMIT_MSG"
else
    echo "ℹ️ No changes to backup"
fi
