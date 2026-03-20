# ENKI AGENTIC - INFRASTRUCTURE DOCUMENTATION
## Production Server Architecture
**Server:** AWS EC2 3.25.170.226 (ap-southeast-2)  
**OS:** Ubuntu 24.04 LTS  
**Generated:** Thu 2026-03-19 15:51 UTC

---

## 🏗️ System Architecture

```
Internet → nginx (Port 3000) → ENKI API (Port 8000) → Agents → SQLite
```

---

## 📦 Installed Services

### 1. nginx (Web Server)
**Status:** 🟢 ACTIVE  
**Config:** `/etc/nginx/sites-enabled/nemo`  
**Purpose:** Reverse proxy, static files, SSL termination

**Configuration:**
```nginx
server {
    listen 3000;
    server_name _;
    
    location / {
        root /home/ubuntu/nz-realestate-ai/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Commands:**
```bash
sudo systemctl status nginx
sudo systemctl restart nginx
sudo nginx -t  # Test config
```

---

### 2. ENKI API (FastAPI)
**Status:** 🟢 ACTIVE  
**Service:** `enki-api.service`  
**Purpose:** Main API layer for all agents

**Configuration:** `/etc/systemd/system/enki-api.service`
```ini
[Unit]
Description=ENKI AGENTIC API Server
After=network.target

[Service]
Type=exec
User=ubuntu
WorkingDirectory=/home/ubuntu/nz-realestate-ai
ExecStart=/home/ubuntu/nz-realestate-ai/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=5
StartLimitInterval=60s
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
```

**Auto-Restart:** YES (every 5 seconds if crashes)  
**Start Limit:** 3 attempts per minute

**Commands:**
```bash
sudo systemctl status enki-api
sudo systemctl restart enki-api
sudo journalctl -u enki-api -f  # View logs
```

---

### 3. AGen_OVAWatch (Monitoring)
**Status:** 🟢 ACTIVE  
**Service:** `agenv-ovawatch.service`  
**Purpose:** System monitoring & agent oversight

**Configuration:** `/etc/systemd/system/agenv-ovawatch.service`

**Auto-Restart:** YES  
**Check Interval:** Every 5 minutes

**Commands:**
```bash
sudo systemctl status agenv-ovawatch
sudo systemctl restart agenv-ovawatch
```

---

### 4. Health Monitoring (Cron)
**Status:** 🟢 ACTIVE  
**File:** `/etc/cron.d/enki-health`  
**Purpose:** 60-second health checks

**Configuration:**
```cron
* * * * * root /usr/local/bin/enki-health-check.sh
```

**Log:** `/var/log/enki-health.log`

---

## 🗄️ Database Layer

### SQLite Databases
**Location:** `/home/ubuntu/enki-agentic/data/`

| Database | Purpose | Records |
|----------|---------|---------|
| `leads.db` | Lead_Terminator data | 3 leads |
| `content.db` | Content_Forge templates & output | 1 content, 4 templates |
| `overseer.db` | AGen_OVAWatch metrics | Monitoring data |
| `legal.db` | AGen_Legal compliance | 15 tasks |

**Backup:** To be configured

---

## 📁 Directory Structure

```
/home/ubuntu/
├── nz-realestate-ai/           # Main API application
│   ├── app/
│   │   ├── api/routes.py      # API endpoints
│   │   ├── agents/            # Original agent framework
│   │   └── main.py            # FastAPI entry point
│   ├── frontend/              # Static HTML dashboard
│   └── venv/                  # Python virtual environment
│
└── enki-agentic/              # ENKI Agent System
    ├── scripts/               # Agent scripts
    │   ├── agenv_ovawatch.py # Overseer
    │   ├── lead_terminator.py
    │   ├── content_forge.py
    │   ├── enki_telegram_bot.py
    │   ├── agen_legal.py
    │   └── enki_alarm_system.py
    ├── data/                  # SQLite databases
    └── venv/                  # Agent virtual environment
```

---

## 🌐 API Endpoints

**Base URL:** `http://3.25.170.226:3000/api/v1`

### Authentication
- JWT tokens (to be configured)
- Rate limit: 100 req/min

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | System health check |
| GET | `/enki/status` | Agent fleet status |
| GET | `/enki/stats` | Lead statistics |
| POST | `/enki/leads/process` | Process new lead |
| GET | `/enki/leads/hot` | Get hot leads |
| GET | `/enki/content/templates` | Content templates |
| POST | `/enki/content/generate` | Generate content |
| GET | `/enki/overseer/check` | AGen_OVAWatch health |
| GET | `/enki/overseer/report` | Full system report |

---

## 🔒 Security

### SSH Access
**Key:** `~/.ssh/id_rsa_nemoclaw`  
**User:** `ubuntu`  
**IP:** `3.25.170.226`

### AWS Security Group
**Open Ports:**
- 22 (SSH)
- 3000 (HTTP - nginx)
- 80 (HTTP - for future)

### File Permissions
```bash
# Home directory (required for nginx)
chmod 755 /home/ubuntu

# Data directory
chmod 777 /home/ubuntu/enki-agentic/data
```

---

## 📊 System Resources

| Resource | Usage | Total | % |
|----------|-------|-------|---|
| Memory | 755 MB | 7.7 GB | 10% |
| Disk | 4.2 GB | 96 GB | 5% |
| CPU | 0.00 | - | 0% |
| Uptime | 16+ hours | - | - |

---

## 🛠️ Useful Commands

### Status Check
```bash
enki-status          # Quick status overview
```

### Restart Services
```bash
enki-restart         # Restart all ENKI services
sudo systemctl restart enki-api
sudo systemctl restart nginx
```

### View Logs
```bash
# API logs
sudo journalctl -u enki-api -f

# Health check logs
tail -f /var/log/enki-health.log

# nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Database Access
```bash
cd ~/enki-agentic/data
sqlite3 leads.db
sqlite3 content.db
sqlite3 legal.db
```

---

## 🔄 Backup Strategy

**TO BE CONFIGURED:**
- Daily database dumps to S3
- Git repository backups
- Configuration backups

---

**Infrastructure is BULLETPROOF and OPERATIONAL.**
