│   ├── services/                  # Shared services
│   │   ├── llm/
│   │   ├── memory/
│   │   ├── vector/
│   │   ├── scrapers/
│   │   └── integrations/
│   │
│   ├── shared/                    # Shared utilities
│   │   ├── types/
│   │   ├── constants/
│   │   ├── utils/
│   │   └── errors/
│   │
│   └── workers/                   # Background jobs
│       ├── queue.ts
│       └── processors/
│
├── config/                        # Configuration
│   ├── database.ts
│   ├── redis.ts
│   ├── llm.ts
│   └── agents.ts
│
├── docs/                          # Documentation
│   ├── api.md
│   ├── agents.md
│   ├── integrations.md
│   └── deployment.md
│
├── tests/                         # Test suites
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/                       # Utility scripts
│   ├── migrate.sh
│   ├── seed.sh
│   └── deploy.sh
│
├── docker-compose.yml
├── Dockerfile
├── package.json
├── tsconfig.json
└── README.md
```

---

## 7. Key Design Decisions & Trade-offs

### 7.1 Why Node.js/NestJS over Python?

**Node.js chosen because:**
- Single language across stack (TypeScript everywhere)
- Better async/concurrent request handling for I/O-bound workloads
- Native GraphQL support via Apollo
- Large ecosystem for real-time applications

**Trade-off**: Python has better ML libraries, but we can call Python microservices for specific ML tasks if needed.

### 7.2 Why GraphQL over REST?

**GraphQL chosen because:**
- Mobile and web clients need different data shapes
- Real-time subscriptions built-in
- Strong typing reduces bugs
- Single endpoint simplifies architecture

**Trade-off**: Caching is more complex; we'll use persisted queries and DataLoader pattern.

### 7.3 Multi-tenancy Approach

**Hybrid strategy:**
- Start with row-level security (simplest, cost-effective)
- Migrate enterprise clients to schema-per-tenant as needed
- This balances cost and isolation requirements

### 7.4 Agent Coordination

**Event-driven vs Direct API calls:**
- Event-driven chosen for loose coupling and scalability
- Each agent can be deployed independently
- Easier to add new agents without modifying existing ones

### 7.5 LLM Strategy

**Multi-provider approach:**
- GPT-4o for complex reasoning tasks
- Claude for long-form content generation
- GPT-4o-mini for high-volume, simple tasks
- This optimizes cost/quality balance

---

## 8. Security & Compliance

### 8.1 NZ-Specific Requirements

- **Privacy Act 2020**: Data retention limits, access controls
- **REAA 2008**: Agent licensing verification, audit trails
- **Anti-money laundering**: Customer due diligence workflows

### 8.2 Technical Measures

- End-to-end encryption for sensitive data
- Field-level encryption for PII
- Audit logging for all agent decisions
- Regular penetration testing

---

## 9. Scaling Strategy

### Phase 1 (0-500 agents)
- Single deployment, managed PostgreSQL/Redis
- All agents in one process
- Cost: ~$500/month infrastructure

### Phase 2 (500-5,000 agents)
- Agent workers scale independently
- Read replicas for database
- CDN for static assets
- Cost: ~$2,000/month

### Phase 3 (5,000+ agents)
- Schema-per-tenant for enterprise
- Regional deployments (AU/NZ)
- Dedicated ML inference cluster
- Cost: ~$10,000+/month

---

## 10. Development Roadmap

### Sprint 1-2: Foundation
- [ ] Database schema + migrations
- [ ] API skeleton (GraphQL)
- [ ] Auth integration (Clerk)
- [ ] Base agent framework

### Sprint 3-4: Lead Agent MVP
- [ ] Intent classification
- [ ] Lead qualification flow
- [ ] CRM connector (AgentBox)
- [ ] WhatsApp integration

### Sprint 5-6: Content Agent MVP
- [ ] Property description generator
- [ ] SEO optimization
- [ ] Image analysis
- [ ] Social post templates

### Sprint 7-8: Scheduling & Transaction
- [ ] Calendar integration
- [ ] Inspection booking
- [ ] Transaction pipeline
- [ ] Document templates

### Sprint 9-10: Market Intelligence
- [ ] TradeMe scraper
- [ ] CMA generation
- [ ] Price alerts
- [ ] Market reports

---

## Appendix: NZ Real Estate Context

### Key Terms
- **LIM**: Land Information Memorandum (council records)
- **S&P**: Sale and Purchase Agreement
- **REINZ**: Real Estate Institute of New Zealand
- **REAA**: Real Estate Agents Authority
- **Open Home**: Scheduled property viewing
- **Tender**: Closed bidding process
- **Auction**: Public bidding process (very common in NZ)
- **Settlement**: Closing/completion date
- **Conditions**: Finance, building report, LIM, valuation

### Regional Variations
- Auckland: Fastest market, auctions common
- Wellington: Government influence, steady market
- Christchurch: Post-quake rebuild focus
- Regional NZ: Longer sales cycles, more conditional offers
