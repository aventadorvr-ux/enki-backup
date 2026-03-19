# Nemo Build Report - NZ Real Estate AI System
## Complete Build Documentation & A Records

**Generated:** 2026-03-19 04:31 UTC  
**Builder:** Nemo (Claude Code sub-agent)  
**Target:** AWS EC2 Instance  
**Repository:** https://github.com/aventadorvr-ux/enki-backup

---

## 📍 Infrastructure & A Records

### EC2 Instance Details
| Property | Value |
|----------|-------|
| **Public IP** | 3.25.170.226 |
| **Private IP** | 172.31.35.97 |
| **Hostname** | ip-172-31-35-97.ap-southeast-2.compute.internal |
| **Region** | ap-southeast-2 (Sydney) |
| **Instance Type** | t3.medium (inferred) |
| **OS** | Ubuntu 24.04 LTS (x86_64) |
| **Kernel** | 6.17.0-1007-aws |

### DNS Configuration
```
Search Domain: ap-southeast-2.compute.internal
Nameserver: 127.0.0.53 (systemd-resolved)
```

### Network Interfaces
| Interface | IP Address | MAC Address |
|-----------|------------|-------------|
| lo | 127.0.0.1 | 00:00:00:00:00:00 |
| enp39s0 | 172.31.35.97/20 | 06:4b:4d:96:d2:df |

### Open Ports (Listening Services)
| Port | Protocol | Service | Process |
|------|----------|---------|---------|
| 22 | TCP | SSH | sshd |
| 53 | TCP | DNS (systemd-resolve) | systemd-resolve |
| 3000 | TCP | HTTP (Frontend) | python3 (http.server) |
| 8000 | TCP | HTTP API (Backend) | uvicorn |

---

## 🏗️ Build Architecture

### System Specifications
| Resource | Total | Used | Available |
|----------|-------|------|-----------|
| **Memory** | 7.6 GB | 606 MB | 7.0 GB |
| **Disk (/)** | 96 GB | 3.2 GB | 93 GB (4%) |
| **Swap** | 0 B | 0 B | 0 B |
| **Load Average** | 0.00 | 0.00 | 0.00 |
| **Uptime** | 5 hours 36 minutes | | |

### Installed Services (Running)
- acpid.service - ACPI event daemon
- chrony.service - NTP client/server
- cron.service - Cron daemon
- dbus.service - D-Bus system message bus
- fwupd.service - Firmware update daemon
- irqbalance.service - IRQ balance daemon
- ModemManager.service - Modem manager
- multipathd.service - Multipath device controller
- networkd-dispatcher.service - Network dispatcher
- polkit.service - Authorization manager
- rsyslog.service - System logging
- snap.amazon-ssm-agent.amazon-ssm-agent.service - AWS SSM agent
- snapd.service - Snap daemon
- ssh.service - OpenSSH server
- systemd-journald.service - Journal service
- systemd-logind.service - Login management
- systemd-networkd.service - Network configuration

---

## 🚀 Application Stack

### Project: NZ Real Estate AI
**Location:** `/home/ubuntu/nz-realestate-ai`  
**Git Commit:** 98400f4 (Initial commit: 5-agent architecture)  
**Virtual Environment:** Python 3.12 venv

### Technology Stack
| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.12 | Runtime |
| FastAPI | 0.109.0 | Web framework |
| Uvicorn | 0.27.0 | ASGI server |
| Pydantic | 2.6.0 | Data validation |
| SQLAlchemy | 2.0.48 | ORM |
| Redis | 5.0.1 (client) | Cache/Queue |
| Celery | 5.3.6 | Task queue |
| pytest | 8.0.0 | Testing |
| python-jose | 3.3.0 | JWT tokens |
| passlib | 1.7.4 | Password hashing |
| aioredis | 2.0.1 | Async Redis |
| structlog | 24.1.0 | Structured logging |
| httpx | 0.26.0 | HTTP client |
| requests | 2.32.5 | HTTP client |
| openai | 2.29.0 | OpenAI API |

### AI/LLM Integration
- **OpenRouter API**: Configured
- **OpenAI API**: Configured
- **Default Model**: anthropic/claude-3.5-sonnet (via OpenRouter)

---

## 🤖 5-Agent Architecture

### Agent 1: Lead Agent (`lead`)
**Purpose:** Lead qualification and routing  
**File:** `app/agents/lead_agent.py`

**Actions:**
- `qualify` - Rule-based lead scoring (budget, timeline, pre-approval)
- `qualify_ai` - AI-powered lead analysis via OpenRouter
- `respond` - Automated response templates
- `route` - Route to available agents

**Scoring Logic:**
- Budget > $500k: +30 points
- Timeline (immediate/1-3mo): +40 points
- Pre-approved: +20 points
- Contact method: +10 points
- Qualified: ≥60 points
- High Priority: ≥80 points

### Agent 2: Content Agent (`content`)
**Purpose:** Property descriptions and marketing  
**File:** `app/agents/content_agent.py`

**Actions:**
- `description` - Generate basic property descriptions
- `description_ai` - AI-generated compelling descriptions
- `social` - Platform-specific social posts
- `social_ai` - AI-optimized social content
- `email` - Email campaign generation

### Agent 3: Scheduling Agent (`scheduling`)
**Purpose:** Calendar management and bookings  
**File:** `app/agents/scheduling_agent.py`

**Actions:**
- `book_showing` - Schedule property showings
- `inspection` - Schedule building inspections
- `availability` - Check agent availability

### Agent 4: Market Intelligence Agent (`market_intel`)
**Purpose:** CMAs and competitor tracking  
**File:** `app/agents/market_agent.py`

**Actions:**
- `cma` - Generate Comparative Market Analysis
- `track_competitor` - Monitor competitor activity
- `trends` - Analyze market trends

### Agent 5: Transaction Coordinator Agent (`transaction`)
**Purpose:** Deal coordination and compliance  
**File:** `app/agents/transaction_agent.py`

**Actions:**
- `track_deadline` - Monitor transaction deadlines
- `checklist` - Generate deal checklists
- `compliance` - Check regulatory compliance

---

## 📁 Project Structure

```
nz-realestate-ai/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API endpoints
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py          # Base agent class
│   │   ├── lead_agent.py
│   │   ├── content_agent.py
│   │   ├── scheduling_agent.py
│   │   ├── market_agent.py
│   │   └── transaction_agent.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Application settings
│   │   ├── ai_service.py    # OpenRouter integration
│   │   └── memory.py        # Shared memory (Redis/local)
│   └── db/
│       ├── __init__.py
│       └── models.py        # SQLAlchemy models
├── frontend/
│   └── index.html           # Dashboard UI
├── alembic/                 # Database migrations
├── docker/
├── tests/
├── venv/                    # Python virtual environment
├── .env                     # Environment variables
├── .git/                    # Git repository
├── docker-compose.yml       # Docker orchestration
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
├── README.md                # Documentation
├── server.log               # Application logs
└── test_api.py              # API tests
```

---

## 🔌 API Endpoints

### Base URL
```
http://3.25.170.226:8000
```

### Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and available endpoints |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI documentation |
| GET | `/api/v1/agents` | List all agents |
| POST | `/api/v1/agents/{agent_name}/process` | Send task to agent |

### Example Requests

**Health Check:**
```bash
curl http://3.25.170.226:8000/health
```

**List Agents:**
```bash
curl http://3.25.170.226:8000/api/v1/agents
```

**Qualify Lead:**
```bash
curl -X POST http://3.25.170.226:8000/api/v1/agents/lead/process \
  -H "Content-Type: application/json" \
  -d '{
    "action": "qualify",
    "data": {
      "budget": 900000,
      "timeline": "immediate",
      "pre_approved": true
    }
  }'
```

**Generate Property Description:**
```bash
curl -X POST http://3.25.170.226:8000/api/v1/agents/content/process \
  -H "Content-Type: application/json" \
  -d '{
    "action": "description",
    "data": {
      "bedrooms": 3,
      "bathrooms": 2,
      "location": "Auckland CBD"
    }
  }'
```

---

## 🗄️ Database Schema

### Tables

**agents**
- id (PK)
- name (unique)
- description
- status
- created_at, updated_at

**leads**
- id (PK)
- name, email, phone
- budget, timeline, pre_approved
- score, qualified, status
- assigned_agent_id (FK)

**properties**
- id (PK)
- address, suburb, city
- bedrooms, bathrooms, price
- description, status

**bookings**
- id (PK)
- property_id (FK)
- client_name, client_email
- datetime, status

**transactions**
- id (PK)
- property_id (FK)
- buyer_name, seller_name
- sale_price, status

**deadlines**
- id (PK)
- transaction_id (FK)
- task, due_date, completed

---

## 📊 System Status

### Backend API
- **Status:** ✅ Healthy
- **Uptime:** 5+ hours
- **Process:** Uvicorn (PID 9216)
- **Port:** 8000 (0.0.0.0)
- **Health Endpoint:** `{"status": "healthy"}`

### Frontend Server
- **Status:** ✅ Running
- **Process:** Python HTTP server (PID 7398)
- **Port:** 3000 (0.0.0.0)

---

## 🔧 Deployment Commands

### SSH Access
```bash
ssh -i ~/.ssh/id_rsa_nemoclaw ubuntu@3.25.170.226
```

### Start Backend
```bash
cd ~/nz-realestate-ai
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
cd ~/nz-realestate-ai/frontend
python3 -m http.server 3000
```

### Docker Deployment
```bash
cd ~/nz-realestate-ai
docker-compose up --build -d
```

---

## ⚠️ Pending Actions

1. **AWS Security Group:** Open ports 8000 & 3000 for external access
2. **Domain Name:** Configure A record pointing to 3.25.170.226
3. **SSL/TLS:** Set up HTTPS with Let's Encrypt
4. **Redis:** Install and configure for production
5. **Database:** Migrate from SQLite to PostgreSQL
6. **Environment:** Move secrets to AWS Secrets Manager

---

## 📦 Backup Information

**Source Code:** Git repository at `~/nz-realestate-ai`  
**Backup Target:** https://github.com/aventadorvr-ux/enki-backup  
**Build Report:** This document (nemo-build-report.md)  
**Generated By:** Enki (main agent) + Nemo (Claude Code sub-agent)

---

## 🔗 Related Resources

- **Enki Backup Repo:** https://github.com/aventadorvr-ux/enki-backup
- **API Documentation:** http://3.25.170.226:8000/docs
- **Dashboard:** http://3.25.170.226:3000

---

*Build completed: 2026-03-19 04:31 UTC*
