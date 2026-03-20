# Windows 11 Migration Checklist

*Created: March 20, 2026*
*Purpose: Step-by-step guide for migrating to Windows 11*

---

## ✅ Phase 1: Pre-Migration Preparation

### 1.1 Compatibility Check
- [ ] Verify PC meets Windows 11 minimum requirements
  - Processor: 1 GHz+, 2+ cores, 64-bit (8th gen Intel or newer)
  - RAM: 4 GB minimum (8 GB recommended)
  - Storage: 64 GB minimum
  - TPM: Version 2.0
  - UEFI firmware with Secure Boot
- [ ] Run Microsoft PC Health Check tool
- [ ] Check for driver compatibility (GPU, printer, peripherals)

### 1.2 Backup Everything
- [ ] **Full system image backup** (Macrium Reflect, Veeam, or Windows Backup)
- [ ] **File backups:**
  - Documents folder
  - Downloads folder
  - Desktop items
  - Pictures, Videos, Music
  - Browser bookmarks and passwords
  - Email client settings and archives
  - Application settings/configurations
- [ ] **Export app data:**
  - Steam/Game library saves (enable Steam Cloud)
  - Creative app settings (Adobe, Blender, etc.)
  - IDE configurations (VS Code, JetBrains, etc.)
  - SSH keys and GPG keys
  - VPN configurations
  - Database exports

### 1.3 License & Account Prep
- [ ] Gather Windows product key (if retail license)
- [ ] Ensure Microsoft account is accessible
- [ ] Deauthorize software that has device limits (Adobe, Spotify, etc.)
- [ ] Document installed software list (use tools like Belarc Advisor or NirSoft ProduKey)

---

## ✅ Phase 2: Installation Method Decision

### Choose Your Path:

**Option A: In-Place Upgrade (Keep files & apps)**
- [ ] Use Windows Update (Settings > Update & Security)
- [ ] Or use Windows 11 Installation Assistant
- [ ] Fastest method, but may carry over issues

**Option B: Clean Install (Recommended)**
- [ ] Download Windows 11 ISO from Microsoft
- [ ] Create bootable USB (8GB+) using Media Creation Tool or Rufus
- [ ] Best performance, fresh start, no legacy baggage

**Option C: Clean Install with local account (Privacy-focused)**
- [ ] Disconnect internet during setup
- [ ] Use `oobe\bypassnro` command to skip Microsoft account
- [ ] Connect internet after setup completes

---

## ✅ Phase 3: Installation Steps

### 3.1 Clean Install Process
- [ ] Boot from USB drive
- [ ] Select language/region
- [ ] Click "Install now"
- [ ] Enter product key (or select "I don't have a product key")
- [ ] Choose "Custom: Install Windows only (advanced)"
- [ ] Delete old partitions (⚠️ **DATA LOSS WARNING** - ensure backups!)
- [ ] Select unallocated space, click Next
- [ ] Wait for installation (10-30 minutes, multiple reboots)

### 3.2 Initial Setup
- [ ] Select region, keyboard layout
- [ ] Name your PC (descriptive but not personal info)
- [ ] Sign in with Microsoft account (or local account)
- [ ] Create PIN for faster login
- [ ] Privacy settings - **TURN OFF:**
  - [ ] Diagnostic data (set to "Required" only)
  - [ ] Inking & typing data
  - [ ] Tailored experiences
  - [ ] Advertising ID
  - [ ] Location (unless needed)
  - [ ] Find my device (optional)

---

## ✅ Phase 4: Post-Installation Setup

### 4.1 System Updates
- [ ] Run Windows Update repeatedly until no updates remain
- [ ] Update drivers via Windows Update first
- [ ] Install manufacturer-specific drivers (Dell SupportAssist, Lenovo Vantage, etc.)
- [ ] Update GPU drivers (NVIDIA GeForce Experience / AMD Adrenalin / Intel Arc)

### 4.2 Essential Software Installation
**Priority 1 - System:**
- [ ] Web browser (Chrome/Firefox/Edge)
- [ ] 7-Zip or WinRAR
- [ ] VLC media player
- [ ] Notepad++ or VS Code
- [ ] PDF reader (SumatraPDF or Adobe)

**Priority 2 - Productivity:**
- [ ] Office suite (Microsoft Office / LibreOffice)
- [ ] Cloud sync (Dropbox, Google Drive, OneDrive)
- [ ] Password manager (Bitwarden, 1Password, KeePass)
- [ ] Communication apps (Discord, Slack, Zoom, Teams)

**Priority 3 - Development (if applicable):**
- [ ] Git for Windows
- [ ] Docker Desktop
- [ ] VS Code + extensions
- [ ] Node.js/Python/Go/Rust
- [ ] Terminal (Windows Terminal, PowerShell 7, WezTerm)
- [ ] WSL2 (if needed)

**Priority 4 - Creative/Gaming:**
- [ ] Steam, Epic, GOG, Xbox app
- [ ] Creative software (Adobe CC, Blender, DaVinci Resolve)
- [ ] OBS Studio

### 4.3 System Configuration
- [ ] **Taskbar & Start Menu:**
  - Pin essential apps
  - Move taskbar left/center (personal preference)
  - Disable "Recommended" section in Start
  - [ ] **Settings > Personalization:**
  - Set dark/light mode
  - Configure accent color
  - Set wallpaper
  - Configure lock screen
- [ ] **File Explorer:**
  - Show file extensions (View > Show > File name extensions)
  - Show hidden files
  - Enable "Compact view" or adjust icon size
- [ ] **Power settings:**
  - Set sleep/hibernate timers
  - Configure lid close action (laptops)
  - Set high performance plan (if desktop)
- [ ] **Notifications:**
  - Turn off unnecessary app notifications
  - Configure Focus Assist

### 4.4 Security Setup
- [ ] Windows Security (Defender) is usually sufficient
- [ ] Enable BitLocker drive encryption (Pro/Enterprise)
- [ ] Configure Windows Hello (fingerprint/face/PIN)
- [ ] Set up backup solution (File History, Veeam, or Macrium)
- [ ] Enable Find My Device (optional)

---

## ✅ Phase 5: Data Restoration

### 5.1 Restore Files
- [ ] Copy documents from backup
- [ ] Restore browser data (bookmarks, passwords, extensions)
- [ ] Import email client settings and archives
- [ ] Restore SSH keys, GPG keys to appropriate directories
- [ ] Restore app configurations

### 5.2 Verify Everything
- [ ] Test all critical applications
- [ ] Verify printer/scanner functionality
- [ ] Test external monitors and peripherals
- [ ] Check audio input/output devices
- [ ] Verify network shares and VPN connections

---

## ✅ Phase 6: Optimization & Cleanup

### 6.1 Remove Bloatware
- [ ] Uninstall pre-installed apps you don't need:
  - TikTok, Instagram, Facebook (if present)
  - Candy Crush, Solitaire (optional)
  - News, Weather, Sports (if unwanted)
- [ ] Use `winget` or PowerShell to batch uninstall

### 6.2 Performance Tweaks
- [ ] Disable startup programs (Task Manager > Startup)
- [ ] Disable transparency effects (Settings > Accessibility > Visual effects)
- [ ] Adjust visual effects for performance (System Properties > Advanced)
- [ ] Disable Game Mode (if not gaming)
- [ ] Configure Storage Sense for automatic cleanup

### 6.3 Create Restore Point
- [ ] Create manual System Restore point
- [ ] Document clean state for future reference

---

## 📋 Quick Reference

### Useful Commands
```powershell
# List installed apps (PowerShell)
Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName

# Windows Update from command line
UsoClient StartInteractiveScan

# Open startup folder
shell:startup
```

### Winget One-Liners
```powershell
# Essential dev tools
winget install Git.Git Microsoft.PowerShell Microsoft.WindowsTerminal JanDeDobbeleer.OhMyPosh

# Browsers
winget install Google.Chrome Mozilla.Firefox Brave.Brave

# Media & utils
winget install VideoLAN.VLC 7zip.7zip Notepad++.Notepad++
```

---

## ⚠️ Known Issues & Solutions

| Issue | Solution |
|-------|----------|
| TPM/Secure Boot error | Enable in BIOS/UEFI settings |
| Driver compatibility | Check manufacturer website for Win11 drivers |
| Start menu slow | Restart Explorer or check for updates |
| High RAM usage | Disable SysMain (Superfetch) service |
| Printer not working | Remove and re-add printer; update drivers |

---

## 📝 Post-Migration Notes

*Use this space to document any issues encountered and their solutions:*

- 
- 
- 

---

*Migration completed: ___/___/____*
*Migration method used: [In-Place Upgrade / Clean Install]*
*Any issues encountered:*
