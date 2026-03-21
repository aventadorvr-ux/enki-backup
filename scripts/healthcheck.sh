#!/data/data/com.termux/files/usr/bin/bash
# Server Health Check Script with ntfy.sh alerts
# Sends alerts to phone +6421777516

NTFY_TOPIC="server-alerts-$(hostname | md5sum | head -c 8)"
NTFY_URL="https://ntfy.sh/$NTFY_TOPIC"
PHONE="+6421777516"
LOG_FILE="/data/data/com.termux/files/home/.openclaw/workspace/logs/healthcheck.log"
ALERT_STATE_FILE="/data/data/com.termux/files/home/.openclaw/workspace/.healthcheck_state"

# Create logs directory if needed
mkdir -p "$(dirname "$LOG_FILE")"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Send ntfy alert
send_alert() {
    local priority="$1"
    local title="$2"
    local message="$3"
    
    curl -s -o /dev/null -w "%{http_code}" \
        -H "Title: $title" \
        -H "Priority: $priority" \
        -H "Tags: server,health,alert" \
        -d "$message" \
        "$NTFY_URL" 2>/dev/null
}

# Check system resources
check_resources() {
    # Check CPU usage (average over 1 minute)
    CPU_USAGE=$(cat /proc/loadavg | awk '{print $1}')
    CPU_CORES=$(nproc)
    CPU_PERCENT=$(echo "scale=0; ($CPU_USAGE * 100) / $CPU_CORES" | bc 2>/dev/null || echo "0")
    
    # Check memory usage
    MEM_INFO=$(free 2>/dev/null || cat /proc/meminfo 2>/dev/null)
    if command -v free >/dev/null 2>&1; then
        MEM_USED=$(free | grep Mem | awk '{print $3}')
        MEM_TOTAL=$(free | grep Mem | awk '{print $2}')
        MEM_PERCENT=$(echo "scale=0; ($MEM_USED * 100) / $MEM_TOTAL" | bc 2>/dev/null || echo "0")
    else
        MEM_PERCENT="0"
    fi
    
    # Check disk usage
    DISK_USAGE=$(df -h / 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%')
    
    echo "CPU:${CPU_PERCENT}% MEM:${MEM_PERCENT}% DISK:${DISK_USAGE}%"
}

# Check OpenClaw gateway
check_openclaw() {
    # Check if gateway process is running
    if pgrep -f "openclaw" >/dev/null 2>&1 || ps aux | grep -v grep | grep -q openclaw; then
        echo "running"
    else
        echo "stopped"
    fi
}

# Check network connectivity
check_network() {
    if ping -c 1 -W 3 8.8.8.8 >/dev/null 2>&1; then
        echo "connected"
    else
        echo "disconnected"
    fi
}

# Main health check
main() {
    log "=== Health Check Started ==="
    
    RESOURCES=$(check_resources)
    OPENCLAW_STATUS=$(check_openclaw)
    NETWORK_STATUS=$(check_network)
    
    log "Resources: $RESOURCES"
    log "OpenClaw: $OPENCLAW_STATUS"
    log "Network: $NETWORK_STATUS"
    
    # Parse resource values
    CPU_PERCENT=$(echo "$RESOURCES" | grep -o 'CPU:[0-9]*%' | cut -d: -f2 | tr -d '%')
    MEM_PERCENT=$(echo "$RESOURCES" | grep -o 'MEM:[0-9]*%' | cut -d: -f2 | tr -d '%')
    DISK_USAGE=$(echo "$RESOURCES" | grep -o 'DISK:[0-9]*%' | cut -d: -f2 | tr -d '%')
    
    ALERTS=""
    PRIORITY="default"
    
    # Check thresholds and build alert message
    if [ "$CPU_PERCENT" -gt 90 ] 2>/dev/null; then
        ALERTS="${ALERTS}⚠️ HIGH CPU: ${CPU_PERCENT}%\n"
        PRIORITY="high"
    fi
    
    if [ "$MEM_PERCENT" -gt 90 ] 2>/dev/null; then
        ALERTS="${ALERTS}⚠️ HIGH MEMORY: ${MEM_PERCENT}%\n"
        PRIORITY="high"
    fi
    
    if [ "$DISK_USAGE" -gt 85 ] 2>/dev/null; then
        ALERTS="${ALERTS}⚠️ HIGH DISK: ${DISK_USAGE}%\n"
        PRIORITY="high"
    fi
    
    if [ "$OPENCLAW_STATUS" = "stopped" ]; then
        ALERTS="${ALERTS}🚨 OPENCLAW STOPPED\n"
        PRIORITY="urgent"
        # Attempt auto-restart
        log "Attempting auto-restart of OpenClaw..."
        nohup openclaw gateway start >/dev/null 2>&1 &
        sleep 2
        if [ "$(check_openclaw)" = "running" ]; then
            ALERTS="${ALERTS}✅ Auto-restart successful\n"
        else
            ALERTS="${ALERTS}❌ Auto-restart FAILED\n"
        fi
    fi
    
    if [ "$NETWORK_STATUS" = "disconnected" ]; then
        ALERTS="${ALERTS}📡 NETWORK DOWN\n"
        PRIORITY="high"
    fi
    
    # Send alert if there are issues
    if [ -n "$ALERTS" ]; then
        HOSTNAME=$(hostname)
        MESSAGE="📊 Server: $HOSTNAME\n\n$ALERTS\n📋 Current Status:\n$RESOURCES"
        
        RESULT=$(send_alert "$PRIORITY" "🚨 Server Alert - $HOSTNAME" "$MESSAGE")
        log "Alert sent (HTTP $RESULT)"
        
        # Save state
        echo "$(date +%s)" > "$ALERT_STATE_FILE"
        echo "ALERT_SENT" >> "$ALERT_STATE_FILE"
    else
        log "All systems healthy"
    fi
    
    # Always update the state file with latest check
    echo "LAST_CHECK=$(date +%s)" > "$ALERT_STATE_FILE"
    echo "RESOURCES=$RESOURCES" >> "$ALERT_STATE_FILE"
    echo "OPENCLAW=$OPENCLAW_STATUS" >> "$ALERT_STATE_FILE"
    echo "NETWORK=$NETWORK_STATUS" >> "$ALERT_STATE_FILE"
    
    log "=== Health Check Complete ==="
}

# Run main function
main "$@"
