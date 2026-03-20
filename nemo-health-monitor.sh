#!/bin/bash
# NEMO Health Monitor - Sends alerts when services are down

API_URL="http://127.0.0.1:8000/health"
FRONTEND_URL="http://127.0.0.1:3000"
LOG_FILE="/var/log/nemo-monitor.log"
ALERT_FILE="/tmp/nemo-last-alert"

# Telegram bot config (will be set by user)
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"

send_alert() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S UTC')
    
    echo "[$timestamp] ALERT: $message" >> $LOG_FILE
    
    # Send Telegram alert if configured
    if [[ -n "$TELEGRAM_BOT_TOKEN" && -n "$TELEGRAM_CHAT_ID" ]]; then
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d "chat_id=$TELEGRAM_CHAT_ID" \
            -d "text=🚨 NEMO ALERT 🚨

$message

Time: $timestamp
Server: 3.25.170.226" \
            -d "parse_mode=HTML" > /dev/null 2>&1
    fi
}

# Check API
if ! curl -s -f "$API_URL" > /dev/null 2>&1; then
    if [[ ! -f "$ALERT_FILE.api" ]]; then
        send_alert "🔴 API is DOWN! Endpoint: $API_URL"
        touch "$ALERT_FILE.api"
    fi
else
    if [[ -f "$ALERT_FILE.api" ]]; then
        send_alert "🟢 API is BACK UP!"
        rm -f "$ALERT_FILE.api"
    fi
fi

# Check Frontend
if ! curl -s -f "$FRONTEND_URL" > /dev/null 2>&1; then
    if [[ ! -f "$ALERT_FILE.frontend" ]]; then
        send_alert "🔴 Frontend is DOWN! URL: $FRONTEND_URL"
        touch "$ALERT_FILE.frontend"
    fi
else
    if [[ -f "$ALERT_FILE.frontend" ]]; then
        send_alert "🟢 Frontend is BACK UP!"
        rm -f "$ALERT_FILE.frontend"
    fi
fi

# Log successful check
echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] Health check passed" >> $LOG_FILE
