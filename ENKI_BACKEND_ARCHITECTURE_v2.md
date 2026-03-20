# ENKI AGENTIC - BACKEND ARCHITECTURE v2.0
## Real Estate AI System - Production Spec

### Core Philosophy
- **Zero vulnerabilities** - Security first
- **Clockwork precision** - 99.9% uptime
- **Kimi K2.5 powered** - Maximum intelligence
- **Token economics** - Monthly allocation system
- **Plug-and-play** - UX/UI agnostic API layer

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ENKI AGENTIC PLATFORM                    │
├─────────────────────────────────────────────────────────────┤
│  LAYER 1: API GATEWAY (nginx + Rate Limiting)              │
│  ├── SSL/TLS termination                                   │
│  ├── DDoS protection                                       │
│  ├── Request validation                                    │
│  └── Auth middleware (JWT)                                 │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: AGENT ORCHESTRATION (FastAPI + Celery)           │
│  ├── Agent registry                                        │
│  ├── Task queue management                                 │
│  ├── Token accounting                                      │
│  └── Load balancing                                        │
├─────────────────────────────────────────────────────────────┤
│  LAYER 3: AGENT FLEET                                      │
│  ├── AGen_OVAWatch (Monitoring)                           │
│  ├── Nemo_BaCBuild (Backend construction)                 │
│  ├── AGen_BackendDev (Security/DevOps)                    │
│  ├── Lead_Terminator (Lead qualification)                 │
│  ├── Content_Forge (Marketing content)                    │
│  ├── Market_Intel_Core (CMAs/Analytics)                   │
│  ├── Scheduling_Drone (Calendar/Bookings)                 │
│  └── Transaction_Coord (Deal management)                  │
├─────────────────────────────────────────────────────────────┤
│  LAYER 4: DATA LAYER                                       │
│  ├── PostgreSQL (Primary DB)                              │
│  ├── Redis (Cache + Queue)                                │
│  ├── S3 (File storage)                                    │
│  └── Elasticsearch (Search/Logs)                          │
├─────────────────────────────────────────────────────────────┤
│  LAYER 5: AI ENGINE (Kimi K2.5 via OpenRouter)            │
│  ├── Token pool management                                 │
│  ├── Request optimization                                  │
│  ├── Response caching                                      │
│  └── Fallback strategies                                   │
└─────────────────────────────────────────────────────────────┘
```

### Token Economics System

**Monthly Token Allocation:**
- **Free tier:** 10K tokens/month (testing)
- **Pro tier:** 100K tokens/month ($29/month)
- **Enterprise:** 1M tokens/month ($199/month)

**Token Consumption:**
- Lead qualification: ~500 tokens/lead
- Content generation: ~1K tokens/piece
- Market analysis: ~2K tokens/report
- Priority support: 2x token efficiency

**Token Management:**
```python
class TokenManager:
    - Track usage per agent
    - Set soft/hard limits
    - Auto-recharge options
    - Usage analytics dashboard
```

### Security Framework

**Authentication:**
- JWT tokens with 1-hour expiry
- Refresh token rotation
- API key management
- Rate limiting: 100 req/min per user

**Authorization:**
- Role-based access control (RBAC)
- Agent-level permissions
- Audit logging (all actions)
- IP whitelisting option

**Data Protection:**
- AES-256 encryption at rest
- TLS 1.3 in transit
- PII data masking
- GDPR compliance ready

**Vulnerability Prevention:**
- Input sanitization (SQL injection, XSS)
- File upload validation
- CORS policy strict
- Security headers (HSTS, CSP, etc.)

### Database Schema (PostgreSQL)

```sql
-- Core tables
users (id, email, role, agency_id, token_balance, created_at)
agencies (id, name, plan_type, token_quota, settings)
leads (id, agency_id, source, contact_info, score, status, ai_conversation)
properties (id, agency_id, address, details, listing_status)
content_cache (id, type, input_hash, output, token_cost, created_at)
token_transactions (id, user_id, amount, type, description, created_at)
agent_logs (id, agent_name, task_type, status, duration, token_usage)
```

### API Design (REST + WebSocket)

**REST Endpoints:**
```
POST   /api/v2/auth/login
POST   /api/v2/auth/refresh
GET    /api/v2/user/profile
GET    /api/v2/user/tokens

GET    /api/v2/leads
POST   /api/v2/leads
GET    /api/v2/leads/:id
POST   /api/v2/leads/:id/respond

GET    /api/v2/content/templates
POST   /api/v2/content/generate

GET    /api/v2/market/cma
GET    /api/v2/market/trends

GET    /api/v2/agents/status
POST   /api/v2/agents/:name/task

WS     /api/v2/stream/realtime  # WebSocket for live updates
```

### Agent Communication Protocol

**Message Format:**
```json
{
  "task_id": "uuid",
  "agent": "agent_name",
  "action": "task_type",
  "payload": {},
  "priority": 1-5,
  "token_budget": 1000,
  "callback_url": "optional"
}
```

**Response Format:**
```json
{
  "task_id": "uuid",
  "status": "success|error",
  "result": {},
  "tokens_used": 500,
  "duration_ms": 1200,
  "timestamp": "2026-03-19T15:00:00Z"
}
```

### 48-Hour Deployment Plan

**Day 1 (0-24h):**
- [ ] Deploy PostgreSQL + Redis
- [ ] Set up new FastAPI v2 architecture
- [ ] Implement authentication system
- [ ] Deploy AGen_BackendDev + Nemo_BaCBuild
- [ ] Security audit + vulnerability scan
- [ ] Token management system

**Day 2 (24-48h):**
- [ ] Deploy all agents with new architecture
- [ ] Build admin dashboard
- [ ] UX/UI integration layer
- [ ] Load testing (1000 concurrent)
- [ ] Demo environment setup
- [ ] Documentation

### UX/UI Integration Points

**Frontend SDK:**
```javascript
// Plug-and-play JavaScript SDK
import { EnkiClient } from '@enki/agentic';

const enki = new EnkiClient({
  apiKey: 'your_key',
  agencyId: 'your_agency'
});

// Use any UI framework (React, Vue, vanilla)
enki.leads.create({ source: 'website', ... });
enki.content.generate({ type: 'property_description', ... });
enki.on('lead.hot', (lead) => { alert(`Hot lead: ${lead.contact}`); });
```

**Webhook Support:**
```
POST /webhooks/enki
- lead.qualified
- lead.hot
- content.ready
- market.alert
- system.warning
```

### Kimi K2.5 Integration

**Model Config:**
```python
{
  "model": "openrouter/moonshotai/kimi-k2.5",
  "max_tokens": 4000,
  "temperature": 0.7,
  "top_p": 0.9,
  "presence_penalty": 0.1,
  "frequency_penalty": 0.1
}
```

**Optimization:**
- Response caching (Redis)
- Request batching
- Token usage prediction
- Smart retries with backoff

### Monitoring & Alerting

**AGen_OVAWatch v2.0:**
- Prometheus metrics
- Grafana dashboards
- PagerDuty integration
- SLA monitoring (99.9% target)

**Alerts:**
- Token quota 80% reached
- API latency > 2s
- Error rate > 1%
- Database connections > 80%

### Demo Requirements (48h)

**Working Features:**
1. ✅ User login/auth
2. ✅ Lead capture + AI qualification
3. ✅ Hot lead alerts (Telegram/SMS)
4. ✅ Content generation (property descriptions)
5. ✅ Token usage dashboard
6. ✅ Agent status monitoring
7. ✅ Mobile-responsive UI

**Demo Flow:**
1. Login as agent
2. View lead dashboard
3. Process test lead (AI conversation)
4. Generate property description
5. Check token usage
6. Receive hot lead alert

---

**THIS IS THE ARCHITECTURE. DEPLOYING NOW.**
