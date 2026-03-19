#!/data/data/com.termux/files/usr/bin/bash
# Git Backup Helper - Auto-authentication

REPO_DIR="/data/data/com.termux/files/home/.openclaw/workspace"
GITHUB_USER="aventadorvr-ux"
REPO_NAME="enki-backup"
SSH_KEY="$HOME/.ssh/id_ed25519_enki"

echo "🔧 Git Authentication Setup"
echo "=========================="
echo ""

# Method 1: SSH (Recommended)
echo "1️⃣ SSH Method (Recommended - Already Configured)"
echo "   SSH Key: $SSH_KEY"
echo "   Public Key:"
cat "${SSH_KEY}.pub"
echo ""
echo "   👉 Add to GitHub: https://github.com/settings/keys"
echo "   Click 'New SSH key' → Paste above key → Add"
echo ""

# Method 2: Personal Access Token
echo "2️⃣ Personal Access Token (PAT) Method"
echo "   👉 Generate at: https://github.com/settings/tokens"
echo "   Required scopes: repo (full control of private repositories)"
echo "   Then run:"
echo "   git remote set-url origin https://TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"
echo ""

# Method 3: Credential Helper (Interactive)
echo "3️⃣ Credential Helper (Interactive)"
echo "   Already configured: git config --global credential.helper store"
echo "   Next push will prompt for username/password (use PAT as password)"
echo ""

# Current status
echo "📊 Current Git Config:"
cd "$REPO_DIR" && git remote -v
echo ""
echo "📁 Uncommitted changes:"
cd "$REPO_DIR" && git status --short
