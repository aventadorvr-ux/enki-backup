#!/data/data/com.termux/files/usr/bin/bash
# Health Monitor Daemon - runs health checks every 5 minutes
# This script runs continuously in the background

SCRIPT_DIR="/data/data/com.termux/files/home/.openclaw/workspace/scripts"
LOG_FILE="/data/data/com.termux/files/home/.openclaw/workspace/logs/monitor-daemon.log"
PID_FILE="/data/data/com.termux/files/home/.openclaw/workspace/.monitor.pid"
INTERVAL=300  # 5 minutes in seconds

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if already running
check_running() {
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE" 2>/dev/null)
        if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
            log "Monitor already running (PID: $OLD_PID)"
            return 0
        fi
    fi
    return 1
}

# Cleanup on exit
cleanup() {
    log "Monitor stopping..."
    rm -f "$PID_FILE"
    exit 0
}

trap cleanup SIGTERM SIGINT

# Main monitor loop
run_monitor() {
    log "=== Health Monitor Daemon Started ==="
    log "PID: $$, Interval: ${INTERVAL}s"
    echo $$ > "$PID_FILE"
    
    # Run immediately on start
    "$SCRIPT_DIR/healthcheck.sh" >> "$LOG_FILE" 2>&1
    
    while true; do
        sleep "$INTERVAL"
        "$SCRIPT_DIR/healthcheck.sh" >> "$LOG_FILE" 2>&1
    done
}

# Handle commands
case "${1:-start}" in
    start)
        if check_running; then
            echo "Monitor is already running"
            exit 1
        fi
        # Run in background
        nohup bash "$0" daemon >> "$LOG_FILE" 2>&1 &
        echo "Health monitor started (PID: $!)"
        ;;
    daemon)
        run_monitor
        ;;
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            kill "$PID" 2>/dev/null && echo "Monitor stopped" || echo "Monitor not running"
            rm -f "$PID_FILE"
        else
            echo "Monitor not running (no PID file)"
        fi
        ;;
    status)
        if check_running; then
            echo "Monitor is running"
            if [ -f "$LOG_FILE" ]; then
                echo "Last check: $(tail -5 "$LOG_FILE" | grep "Health Check" | tail -1)"
            fi
        else
            echo "Monitor is not running"
        fi
        ;;
    restart)
        "$0" stop
        sleep 2
        "$0" start
        ;;
    test)
        log "Running manual test..."
        "$SCRIPT_DIR/healthcheck.sh"
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart|test}"
        exit 1
        ;;
esac
