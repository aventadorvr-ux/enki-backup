#!/bin/bash
# Windows 11 Migration Manager for OpenClaw
# Source: Android/Termux → Destination: Windows 11

set -e

MIGRATION_DIR="$HOME/.openclaw/workspace/migration-package"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="openclaw-migration-${TIMESTAMP}"
PACKAGE_PATH="${MIGRATION_DIR}/${PACKAGE_NAME}.tar.gz"

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         Windows 11 Migration Manager for OpenClaw                  ║"
echo "║              Android/Termux → Windows 11                           ║"
echo "╚════════════════════════════════════════════════════════════════════╝"

mkdir -p "$MIGRATION_DIR"
cd "$MIGRATION_DIR"

STAGING_DIR="${MIGRATION_DIR}/staging"
rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR"

echo ""
echo "🔍 Phase 1: Scanning source system..."

# Initialize manifest
cat > "$STAGING_DIR/MANIFEST.md" << 'EOF'
# OpenClaw Migration Package Manifest
# Source: Android/Termux | Destination: Windows 11
EOF

echo "  ✓ Scanning OpenClaw workspace..."

# 1. OpenClaw Workspace Files
if [ -d "$HOME/.openclaw/workspace" ]; then
    mkdir -p "$STAGING_DIR/workspace"
    
    # Core documentation
    for file in AGENTS.md SOUL.md USER.md IDENTITY.md TOOLS.md MEMORY.md HEARTBEAT.md; do
        if [ -f "$HOME/.openclaw/workspace/$file" ]; then
            cp "$HOME/.openclaw/workspace/$file" "$STAGING_DIR/workspace/" 2>/dev/null
        fi
    done
    
    # Git config
    if [ -d "$HOME/.openclaw/workspace/.git" ]; then
        mkdir -p "$STAGING_DIR/workspace/.git"
        cp "$HOME/.openclaw/workspace/.git/config" "$STAGING_DIR/workspace/.git/" 2>/dev/null
    fi
    
    # Memory files
    if [ -d "$HOME/.openclaw/workspace/memory" ]; then
        mkdir -p "$STAGING_DIR/workspace/memory"
        cp "$HOME/.openclaw/workspace/memory/"*.md "$STAGING_DIR/workspace/memory/" 2>/dev/null
    fi
    
    # Scripts folders
    for dir in scripts 05-SCRIPTS; do
        if [ -d "$HOME/.openclaw/workspace/$dir" ]; then
            mkdir -p "$STAGING_DIR/workspace/$dir"
            cp -r "$HOME/.openclaw/workspace/$dir/"* "$STAGING_DIR/workspace/$dir/" 2>/dev/null
        fi
    done
    
    # Other directories (filtered)
    for dir in 00-CORE 01-CONFIG 02-EMAIL 03-NEMO 04-DELIVERABLES 07-RESEARCH 08-ARCHIVE 09-REPORTS; do
        if [ -d "$HOME/.openclaw/workspace/$dir" ]; then
            mkdir -p "$STAGING_DIR/workspace/$dir"
            find "$HOME/.openclaw/workspace/$dir" -maxdepth 2 -type f \( \
                -name "*.sh" -o -name "*.py" -o -name "*.js" -o \
                -name "*.md" -o -name "*.json" -o -name "*.txt" -o \
                -name "*.yml" -o -name "*.yaml" -o -name "*.toml" \
            \) -exec cp {} "$STAGING_DIR/workspace/$dir/" \; 2>/dev/null
        fi
    done
    
    # Root level scripts
    for file in "$HOME/.openclaw/workspace/"*.{sh,py,js,json,yml,yaml,toml}; do
        [ -f "$file" ] && cp "$file" "$STAGING_DIR/workspace/" 2>/dev/null
    done
fi

echo "  ✓ Scanning SSH keys..."

# 2. SSH Keys
if [ -d "$HOME/.ssh" ]; then
    mkdir -p "$STAGING_DIR/ssh"
    for key in id_rsa id_rsa_nemoclaw id_rsa_nemoclaw.pub id_ed25519 id_ed25519.pub id_ed25519_enki id_ed25519_enki.pub known_hosts; do
        if [ -f "$HOME/.ssh/$key" ]; then
            cp "$HOME/.ssh/$key" "$STAGING_DIR/ssh/" 2>/dev/null
        fi
    done
    [ -f "$HOME/.ssh/config" ] && cp "$HOME/.ssh/config" "$STAGING_DIR/ssh/" 2>/dev/null
fi

echo "  ✓ Scanning Git configuration..."

# 3. Git Configuration
if [ -f "$HOME/.gitconfig" ]; then
    mkdir -p "$STAGING_DIR/git"
    cp "$HOME/.gitconfig" "$STAGING_DIR/git/" 2>/dev/null
fi

echo "  ✓ Scanning OpenClaw configuration..."

# 4. OpenClaw Configuration (sanitized)
if [ -d "$HOME/.openclaw" ]; then
    mkdir -p "$STAGING_DIR/openclaw"
    
    # Sanitized config
    if [ -f "$HOME/.openclaw/openclaw.json" ]; then
        cat "$HOME/.openclaw/openclaw.json" | \
            sed 's/"apiKey": "[^"]*"/"apiKey": "YOUR_API_KEY_HERE"/g' | \
            sed 's/"botToken": "[^"]*"/"botToken": "YOUR_BOT_TOKEN_HERE"/g' \
            > "$STAGING_DIR/openclaw/openclaw.json.template"
    fi
    
    # Agent configs
    if [ -d "$HOME/.openclaw/agents" ]; then
        mkdir -p "$STAGING_DIR/openclaw/agents"
        cp -r "$HOME/.openclaw/agents/"* "$STAGING_DIR/openclaw/agents/" 2>/dev/null
    fi
fi

echo "  ✓ Scanning environment variables..."

# 5. Environment Variables Reference
mkdir -p "$STAGING_DIR/environment"
cat > "$STAGING_DIR/environment/ENVIRONMENT.md" << 'EOF'
# Environment Variables Reference

## OpenClaw-Specific Variables
- OPENCLAW_SHELL=exec
- OPENCLAW_GATEWAY_PORT=18789
- OPENCLAW_PATH_BOOTSTRAPPED=1
- OPENCLAW_CLI=1

## Custom Paths
- HOME=/data/data/com.termux/files/home (Termux)
- PATH includes: ~/.local/bin, ~/.local/share/pnpm, ~/.bun/bin

## Windows Equivalents
On Windows, set these in System Properties → Environment Variables
EOF

# 6. Custom Scripts
mkdir -p "$STAGING_DIR/custom-scripts"
find "$HOME/.openclaw" -maxdepth 2 -type f \( -name "*.sh" -o -name "*.py" \) \
    ! -path "*/node_modules/*" ! -path "*/workspace/*" \
    -exec cp {} "$STAGING_DIR/custom-scripts/" \; 2>/dev/null

echo ""
echo "📦 Phase 2: Creating migration package..."

# Create documentation
cat > "$STAGING_DIR/README.md" << 'EOF'
# OpenClaw Windows 11 Migration Package

## Quick Start
1. Extract this package on Windows 11
2. Run `setup-windows.ps1` as Administrator
3. Follow the on-screen instructions

## Contents
- workspace/ - OpenClaw workspace files
- ssh/ - SSH keys and configuration
- git/ - Git configuration
- openclaw/ - OpenClaw configuration templates
- environment/ - Environment variable reference
- custom-scripts/ - Custom scripts

⚠️ SSH keys included - handle with care!
⚠️ API keys removed - must re-enter manually
EOF

# Create the tarball
cd "$STAGING_DIR"
tar -czf "$PACKAGE_PATH" . 2>/dev/null

PACKAGE_SIZE=$(du -h "$PACKAGE_PATH" 2>/dev/null | cut -f1)

echo "  ✓ Package created: $PACKAGE_PATH"
echo "  ✓ Size: $PACKAGE_SIZE"

# Generate manifest
cat > "$MIGRATION_DIR/MANIFEST.md" << EOF
# Migration Package Manifest

**Package**: ${PACKAGE_NAME}.tar.gz
**Generated**: $(date -Iseconds)
**Size**: ${PACKAGE_SIZE}

## What Was Migrated
✅ OpenClaw workspace (AGENTS.md, SOUL.md, MEMORY.md, etc.)
✅ Memory files (daily notes)
✅ Custom scripts and configurations
✅ SSH keys (id_rsa_nemoclaw, id_ed25519_enki, etc.)
✅ Git configuration (.gitconfig, .git/config)
✅ OpenClaw configuration templates (sanitized)
✅ Environment variable reference

## What Was NOT Migrated
❌ node_modules/ directories
❌ venv/ Python virtual environments
❌ .next/ build directories
❌ Large binary files
❌ OpenClaw installation
❌ API keys and tokens
❌ System packages
EOF

# Cleanup staging
rm -rf "$STAGING_DIR"

echo ""
echo "✅ Migration package created successfully!"
echo ""
echo "📁 Location: $PACKAGE_PATH"
echo "📋 Manifest: $MIGRATION_DIR/MANIFEST.md"
echo ""
