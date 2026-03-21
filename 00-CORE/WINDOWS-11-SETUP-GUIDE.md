# Windows 11 OpenClaw Setup Guide

> **Purpose:** Complete environment checklist for running OpenClaw on Windows 11 with WSL2 integration.
> **Target:** Developers migrating from Linux/macOS or fresh Windows installs.

---

## 1. Prerequisites Check

### ✅ WSL2 (Windows Subsystem for Linux 2)

**Check if installed:**
```powershell
wsl --list --verbose
```

**Expected output:**
```
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

**If not installed:**
```powershell
# Run in Administrator PowerShell
wsl --install
# Restart required
```

**Set WSL2 as default:**
```powershell
wsl --set-default-version 2
```

**Verify kernel version:**
```bash
wsl cat /proc/version
```

---

### ✅ Windows Terminal (Recommended)

**Install via Microsoft Store** or winget:
```powershell
winget install Microsoft.WindowsTerminal
```

**Why it matters:**
- Better WSL integration than default console
- Supports multiple tabs (PowerShell, WSL, CMD)
- GPU-accelerated text rendering
- Customizable profiles for OpenClaw workflows

**Recommended settings:**
- Set WSL as default profile
- Enable "Copy on select" in settings
- Set scrollback to 10000+ lines

---

### ✅ Node.js LTS

**Check version:**
```powershell
node --version  # Should be v20.x.x or v22.x.x (LTS)
npm --version
```

**Install via nvm-windows (recommended):**
```powershell
# Install nvm-windows from: https://github.com/coreybutler/nvm-windows/releases
nvm install 22
nvm use 22
```

**Or install directly:**
```powershell
winget install OpenJS.NodeJS.LTS
```

**Verify in WSL too:**
```bash
# In WSL terminal
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

### ✅ Git for Windows

**Check version:**
```powershell
git --version  # Should be 2.40+
```

**Install:**
```powershell
winget install Git.Git
```

**Post-install configuration:**
```powershell
# Set default editor (VS Code recommended)
git config --global core.editor "code --wait"

# Enable long paths support
# Run in Administrator PowerShell:
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

---

### ✅ Python 3.11+

**Check version:**
```powershell
python --version  # Should be 3.11.x or 3.12.x
```

**Install via Microsoft Store** or winget:
```powershell
winget install Python.Python.3.12
```

**Install in WSL:**
```bash
# Ubuntu/Debian WSL
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev python3-pip
```

**Verify pip:**
```powershell
pip --version
```

---

## 2. Post-OpenClaw Setup

### 🔑 SSH Key Migration Steps

**From old machine to Windows:**

```powershell
# 1. Copy SSH keys to Windows .ssh directory
# From your backup or old machine:
# Copy: ~/.ssh/id_ed25519, ~/.ssh/id_ed25519.pub, ~/.ssh/config, ~/.ssh/known_hosts

# 2. Set correct permissions (CRITICAL on Windows)
# PowerShell as Administrator:
$sshPath = "$env:USERPROFILE\.ssh"
icacls "$sshPath\id_ed25519" /inheritance:r /grant:r "$($env:USERNAME):R"
icacls "$sshPath\id_ed25519" /remove "NT AUTHORITY\Authenticated Users"
icacls "$sshPath\id_ed25519" /remove "BUILTIN\Users"

# 3. Test SSH connection
ssh -T git@github.com
```

**For WSL (separate key or shared):**
```bash
# Option A: Copy keys to WSL
cp /mnt/c/Users/$WINDOWS_USERNAME/.ssh/id_* ~/.ssh/
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

# Option B: Use 1Password SSH agent or similar
# Recommended for cross-platform consistency
```

**🚨 CRITICAL:** Windows SSH permissions are strict. Wrong permissions = "UNPROTECTED PRIVATE KEY FILE" error.

---

### ⚙️ Git Config Migration

**Copy global config:**
```powershell
# From old machine, copy ~/.gitconfig content
# Or run these commands on Windows:

git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
git config --global push.autoSetupRemote true
git config --global pull.rebase false

# Windows-specific: Handle line endings
git config --global core.autocrlf true  # Convert LF to CRLF on checkout
```

**If using WSL git:**
```bash
# Same commands in WSL - WSL git is separate from Windows git
# Keep them synced or use one consistently
```

---

### 🌍 Environment Variables to Set

**System-level (PowerShell Admin):**
```powershell
# OpenClaw workspace location
[Environment]::SetEnvironmentVariable("OPENCLAW_WORKSPACE", "$env:USERPROFILE\.openclaw\workspace", "User")

# Node options (for memory if needed)
[Environment]::SetEnvironmentVariable("NODE_OPTIONS", "--max-old-space-size=4096", "User")

# Add to PATH if needed
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
[Environment]::SetEnvironmentVariable("PATH", "$currentPath;%USERPROFILE%\.openclaw\bin", "User")
```

**For WSL (add to ~/.bashrc or ~/.zshrc):**
```bash
# OpenClaw env vars
export OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"

# Windows interoperability
export WINDOWS_USERPROFILE="/mnt/c/Users/$(cmd.exe /c 'echo %USERNAME%' 2>/dev/null | tr -d '\r')"

# Path helpers
export PATH="$PATH:$HOME/.openclaw/bin"
```

**Optional - API Keys (store securely):**
- Use Windows Credential Manager
- Or 1Password CLI
- Or .env files (gitignored)
- **Never** commit API keys to the repo

---

### 🤖 Telegram Bot Connection Test

**1. Verify bot token:**
```powershell
# Check if TELEGRAM_BOT_TOKEN is set
echo $env:TELEGRAM_BOT_TOKEN

# Or in OpenClaw config
cat "$env:USERPROFILE\.openclaw\config.yaml" | findstr telegram
```

**2. Test connection manually:**
```powershell
# PowerShell
$token = $env:TELEGRAM_BOT_TOKEN
Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/getMe"
```

**Expected response:**
```json
{
  "ok": true,
  "result": {
    "id": 123456789,
    "is_bot": true,
    "first_name": "YourBotName",
    "username": "your_bot_username"
  }
}
```

**3. Test via OpenClaw:**
```bash
openclaw message send --target "@your_username" --message "OpenClaw Windows test"
```

**Common issues:**
- Firewall blocking Telegram API (rare)
- Incorrect bot token format (should be `123456:ABC-DEF...`)
- Bot not started (send `/start` to bot in Telegram first)

---

### ✅ First-Run Verification Steps

**After OpenClaw installation:**

```powershell
# 1. Verify installation
openclaw --version
openclaw status

# 2. Check gateway status
openclaw gateway status

# 3. Verify workspace
ls $env:USERPROFILE\.openclaw\workspace

# 4. Test basic tools
openclaw exec -- echo "Hello from OpenClaw"

# 5. Test browser (if using browser automation)
openclaw browser status
```

**Expected results:**
- [ ] `openclaw --version` returns version number
- [ ] `openclaw gateway status` shows "running" or ready state
- [ ] Workspace directory exists and is writable
- [ ] Basic exec commands work

**WSL-specific verification:**
```bash
# If running OpenClaw in WSL
which openclaw
openclaw status
# Should detect it's running in WSL environment
```

---

## 3. Backup Strategy for Windows

### 🔄 Auto-Backup to Same GitHub Repo

**Recommended setup:**

```powershell
# 1. Ensure your workspace is a git repo
cd $env:USERPROFILE\.openclaw\workspace
git status

# 2. Create backup script (save as backup-openclaw.ps1)
```

**backup-openclaw.ps1:**
```powershell
#!/usr/bin/env pwsh
# OpenClaw Windows Backup Script

$workspace = "$env:USERPROFILE\.openclaw\workspace"
$logFile = "$env:USERPROFILE\.openclaw\backup.log"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Tee-Object -FilePath $logFile -Append
}

Set-Location $workspace

# Check for changes
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Log "No changes to backup"
    exit 0
}

# Stage and commit
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
git add -A
$commitMsg = "Auto-backup: $timestamp [Windows]"
git commit -m $commitMsg

if ($LASTEXITCODE -eq 0) {
    git push origin main
    Write-Log "Backup completed: $commitMsg"
} else {
    Write-Log "ERROR: Commit failed"
    exit 1
}
```

**Schedule with Task Scheduler:**
```powershell
# Create scheduled task for auto-backup
$action = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-File $env:USERPROFILE\.openclaw\backup-openclaw.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At "18:00"
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd

Register-ScheduledTask -TaskName "OpenClaw Backup" -Action $action -Trigger $trigger -Principal $principal -Settings $settings
```

---

### 📁 Windows-Specific Paths to Know

| Purpose | Windows Path | WSL Path |
|---------|-------------|----------|
| User home | `%USERPROFILE%` | `/mnt/c/Users/<username>` |
| OpenClaw workspace | `%USERPROFILE%\.openclaw\workspace` | `/mnt/c/Users/<username>/.openclaw/workspace` |
| SSH keys | `%USERPROFILE%\.ssh\` | `/mnt/c/Users/<username>/.ssh/` |
| Git config | `%USERPROFILE%\.gitconfig` | `~/.gitconfig` (separate file!) |
| npm global | `%APPDATA%\npm` | `/usr/local/lib/node_modules` |
| Python (Windows) | `%LOCALAPPDATA%\Programs\Python\Python312` | `/usr/bin/python3` |

**Key differences from Linux/macOS:**
- Backslashes (`\`) instead of forward slashes
- Case-insensitive file system (usually)
- Long path support may need enabling
- Antivirus may scan/intercept file operations
- Windows Defender may flag unknown executables

---

### ⏰ Sync Schedule Recommendation

**Daily (automated):**
- Workspace changes committed and pushed
- Trigger: Evening (6 PM) or when idle

**Weekly (manual review):**
- Review MEMORY.md updates
- Clean up old memory files
- Verify backup integrity: `git log --oneline -10`

**Monthly:**
- Full environment verification
- Update Node.js/Python if needed
- Review and rotate SSH keys
- Check disk usage: `Get-ChildItem $env:USERPROFILE\.openclaw -Recurse | Measure-Object -Property Length -Sum`

**Event-triggered:**
- Pre-system update: Manual backup
- After major changes: Immediate commit
- Before travel: Full sync verification

---

## 🚨 Critical Warnings

### 1. **Line Endings Hell**
Windows uses CRLF (`\r\n`), Unix uses LF (`\n`). Mixed line endings break shell scripts.

**Fix:**
```powershell
# For specific files (keep LF)
git config --global core.autocrlf input
# Or use .gitattributes in repo
```

### 2. **Path Separator Confusion**
PowerShell accepts both `/` and `\`, but some tools don't.

**Fix:** Always use `Join-Path` in scripts:
```powershell
$path = Join-Path $env:USERPROFILE ".openclaw" "workspace"
```

### 3. **WSL/Windows Git Conflicts**
Using Git in both environments can cause permission/line-ending issues.

**Recommendation:** Pick one and stick to it. WSL git is closer to Linux behavior.

### 4. **Antivirus Interference**
Windows Defender or third-party AV may:
- Slow down file operations in workspace
- Block unknown executables
- Flag Node.js native modules

**Fix:** Add `%USERPROFILE%\.openclaw` to exclusions if trusted.

### 5. **SSH Agent Conflicts**
Windows OpenSSH agent and 1Password/wsl-ssh-agent may conflict.

**Fix:** Use one SSH agent consistently. 1Password works well cross-platform.

### 6. **WSL Clock Drift**
WSL clock can drift from Windows clock after sleep/hibernate.

**Fix:**
```bash
# In WSL
sudo hwclock -s
# Or restart WSL: wsl --shutdown
```

---

## Quick Reference Card

```powershell
# Check everything is ready
wsl --list --verbose                    # WSL2 status
node --version                          # Node.js
python --version                        # Python
git --version                           # Git
openclaw --version                      # OpenClaw

# Common paths
$env:USERPROFILE                        # C:\Users\<you>
$env:USERPROFILE\.openclaw\workspace    # Workspace
$env:USERPROFILE\.ssh\                  # SSH keys

# Quick backup
cd $env:USERPROFILE\.openclaw\workspace; git add -A; git commit -m "Backup $(Get-Date -Format 'yyyy-MM-dd')"; git push
```

---

**Last Updated:** 2025-03-20  
**Applies To:** Windows 11 23H2+, OpenClaw latest, WSL2 with Ubuntu 22.04+
