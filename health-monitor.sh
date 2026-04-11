#!/bin/bash
# Enki_888 Health Monitor
# Checks NEMO backend and OpenClaw gateway every 5 minutes

LOG_FILE="$HOME/.openclaw/workspace/logs/health.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Check NEMO Backend
NEMO_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health 2>/dev/null)
if [ "$NEMO_STATUS" = "200" ]; then
    NEMO_HEALTH="OK"
else
    NEMO_HEALTH="FAIL ($NEMO_STATUS)"
fi

# Check OpenClaw Gateway
GATEWAY_PID=$(pgrep -f "openclaw.*gateway" | head -1)
if [ -n "$GATEWAY_PID" ]; then
    GATEWAY_HEALTH="OK (pid $GATEWAY_PID)"
else
    GATEWAY_HEALTH="FAIL (not running)"
fi

# Log results
echo "[$TIMESTAMP] NEMO: $NEMO_HEALTH | Gateway: $GATEWAY_HEALTH" >> "$LOG_FILE"

# Alert if failures
if [[ "$NEMO_HEALTH" != "OK" ]] || [[ "$GATEWAY_HEALTH" != OK* ]]; then
    echo "[$TIMESTAMP] ALERT: System degradation detected" >> "$LOG_FILE"
    echo "[$TIMESTAMP]   NEMO: $NEMO_HEALTH" >> "$LOG_FILE"
    echo "[$TIMESTAMP]   Gateway: $GATEWAY_HEALTH" >> "$LOG_FILE"
fi

# Keep log file manageable (last 1000 lines)
tail -n 1000 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"