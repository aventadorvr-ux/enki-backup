#!/bin/bash
# BULLETPROOF ENKI DEPLOYMENT
# Zero-downtime, auto-restart, production-grade

echo "🔧 BUILDING BULLETPROOF INFRASTRUCTURE..."

# 1. Install proper process manager
echo "Installing supervisor..."
sudo apt-get update -qq && sudo apt-get install -y -qq supervisor

# 2. Create ENKI API systemd service
echo "Creating ENKI API service..."
sudo tee /etc/systemd/system/enki-api.service > /dev/null << 'EOF'
[Unit]
Description=ENKI AGENTIC API Server
After=network.target
Wants=network.target

[Service]
Type=exec
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/nz-realestate-ai
Environment=PATH=/home/ubuntu/nz-realestate-ai/venv/bin
Environment=PYTHONPATH=/home/ubuntu/nz-realestate-ai
Environment=NEMO_DB=/home/ubuntu/enki-agentic/data/leads.db
Environment=OPENAI_API_KEY=${OPENAI_API_KEY}
ExecStart=/home/ubuntu/nz-realestate-ai/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30
Restart=always
RestartSec=5
StartLimitInterval=60s
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
EOF

# 3. Create health check script
echo "Creating health monitor..."
sudo tee /usr/local/bin/enki-health-check.sh > /dev/null << 'EOF'
#!/bin/bash
# Health check + auto-restart if needed

API_URL="http://127.0.0.1:8000/health"
LOG_FILE="/var/log/enki-health.log"
ALERT_FILE="/tmp/enki-down-alert"

# Check API
if ! curl -s -f "$API_URL" > /dev/null 2>&1; then
    echo "$(date): API DOWN - Triggering restart" >> $LOG_FILE
    
    # Check if already alerted (prevent spam)
    if [[ ! -f "$ALERT_FILE" ]]; then
        echo "$(date): ALERT - API is down" >> $LOG_FILE
        touch "$ALERT_FILE"
        
        # Restart the service properly
        sudo systemctl restart enki-api
        
        # Wait and verify
        sleep 5
        if curl -s -f "$API_URL" > /dev/null 2>&1; then
            echo "$(date): API recovered after restart" >> $LOG_FILE
            rm -f "$ALERT_FILE"
        else
            echo "$(date): CRITICAL - API still down after restart" >> $LOG_FILE
        fi
    fi
else
    # API is healthy, clear alert file if exists
    if [[ -f "$ALERT_FILE" ]]; then
        echo "$(date): API back to healthy" >> $LOG_FILE
        rm -f "$ALERT_FILE"
    fi
    
    # Log health check success (every 5th check to avoid spam)
    if (( RANDOM % 5 == 0 )); then
        echo "$(date): Health check OK" >> $LOG_FILE
    fi
fi
EOF

sudo chmod +x /usr/local/bin/enki-health-check.sh

# 4. Create proper cron (syntax fixed)
echo "Setting up monitoring cron..."
sudo tee /etc/cron.d/enki-health > /dev/null << 'EOF'
# ENKI Health Monitoring - Runs every minute
* * * * * root /usr/local/bin/enki-health-check.sh
EOF

sudo chmod 644 /etc/cron.d/enki-health

# 5. Create comprehensive monitoring script
echo "Creating AGen_OVAWatch systemd service..."
sudo tee /etc/systemd/system/agenv-ovawatch.service > /dev/null << 'EOF'
[Unit]
Description=AGen_OVAWatch - ENKI System Monitor
After=network.target enki-api.service
Wants=enki-api.service

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/enki-agentic
Environment=NEMO_DB=/home/ubuntu/enki-agentic/data/leads.db
Environment=OPENAI_API_KEY=${OPENAI_API_KEY}
ExecStart=/home/ubuntu/enki-agentic/venv/bin/python3 /home/ubuntu/enki-agentic/scripts/agenv_ovawatch.py monitor
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# 6. Create log rotation (prevent disk fill)
echo "Setting up log rotation..."
sudo tee /etc/logrotate.d/enki > /dev/null << 'EOF'
/var/log/enki*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 ubuntu ubuntu
}
EOF

# 7. Enable and start all services
echo "Enabling services..."
sudo systemctl daemon-reload
sudo systemctl enable enki-api
sudo systemctl enable agenv-ovawatch

# 8. Create status checker
echo "Creating status command..."
sudo tee /usr/local/bin/enki-status > /dev/null << 'EOF'
#!/bin/bash
echo "═══════════════════════════════════════"
echo "      ENKI SYSTEM STATUS"
echo "═══════════════════════════════════════"
echo ""
echo "Services:"
echo "  ENKI API:      $(systemctl is-active enki-api)"
echo "  nginx:         $(systemctl is-active nginx)"
echo "  AGen_OVAWatch: $(systemctl is-active agenv-ovawatch 2>/dev/null || echo 'not installed')"
echo ""
echo "Processes:"
echo "  Uvicorn:       $(pgrep -c uvicorn) instances"
echo "  nginx:         $(pgrep -c nginx) workers"
echo ""
echo "Health:"
curl -s http://127.0.0.1:8000/health 2>/dev/null || echo "  API: UNREACHABLE"
echo ""
echo "═══════════════════════════════════════"
EOF

sudo chmod +x /usr/local/bin/enki-status

# 9. Create emergency restart command
sudo tee /usr/local/bin/enki-restart > /dev/null << 'EOF'
#!/bin/bash
echo "Restarting ENKI services..."
sudo systemctl restart enki-api
sleep 3
sudo systemctl restart nginx
enki-status
EOF

sudo chmod +x /usr/local/bin/enki-restart

echo ""
echo "✅ BULLETPROOF INFRASTRUCTURE INSTALLED"
echo ""
echo "Next steps:"
echo "1. Stop old processes:  pkill -f uvicorn"
echo "2. Start new services:  sudo systemctl start enki-api"
echo "3. Check status:        enki-status"
echo "4. Monitor logs:        sudo journalctl -u enki-api -f"
echo ""
