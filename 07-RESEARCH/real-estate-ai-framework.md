# NZ Real Estate AI Agent System
## Technical Framework & Implementation Guide

**Version:** 1.0  
**Target Market:** New Zealand Real Estate  
**Document Type:** Technical Architecture & Roadmap  

---

## Executive Summary

This document outlines a comprehensive AI agent system designed to automate and optimize real estate operations for New Zealand agencies. The system leverages 5-7 specialized AI agents working in concert to handle lead generation, qualification, property matching, and transaction coordination—reducing manual workload while increasing conversion rates.

### Key Value Proposition
- **40-60% reduction** in administrative tasks
- **24/7 lead response** capability
- **AI-powered property matching** with 85%+ relevance accuracy
- **Scalable from single agent to enterprise brokerage**

---

## 1. AGENT ARCHITECTURE

### Multi-Agent System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     ORCHESTRATION LAYER                         │
│              (Workflow Manager / Task Router)                   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
    ┌──────────────────┼──────────────────┬──────────────────┐
    │                  │                  │                  │
    ▼                  ▼                  ▼                  ▼
┌────────┐      ┌────────┐      ┌────────────┐      ┌────────────┐
│ LEAD   │      │OUTREACH│      │ VALUATION  │      │   BUYER    │
│ SCOUT  │      │  AI    │      │    AI      │      │   MATCH    │
└────────┘      └────────┘      └────────────┘      └────────────┘
    │                  │                  │                  │
    ▼                  ▼                  ▼                  ▼
┌────────┐      ┌────────┐      ┌────────────┐      ┌────────────┐
│CONTENT │      │SCHEDULE│      │CONTRACT    │      │  MARKET    │
│ASSIST  │      │ASSIST  │      │   COORD    │      │  ANALYST   │
└────────┘      └────────┘      └────────────┘      └────────────┘
```

---

### Agent 1: Lead Scout AI 🤖
**Purpose:** Continuous lead discovery and ingestion

**Core Functions:**
- **FSBO Detection:** Monitor TradeMe, Facebook Marketplace, Neighbourly for owner-listed properties
- **Expired Listing Tracking:** Identify listings that expired 30/60/90 days ago
- **Distressed Property Signals:** Parse mortgagee sales, deceased estates, divorce filings (public notices)
- **Geo-Hotspot Monitoring:** Track high-activity suburbs, price momentum indicators
- **Social Listening:** Monitor local community groups for "thinking of selling" signals

**AI Capabilities:**
- NLP for intent detection ("might sell", "testing market", "downsizing soon")
- Image analysis for property condition assessment
- Predictive scoring (motivation probability 0-100%)

**Output:** Qualified lead queue with enrichment data

---

### Agent 2: Outreach AI 📞
**Purpose:** Initial contact, qualification, and relationship initiation

**Core Functions:**
- **Multi-Channel Sequences:** Email → SMS → Voice (automated with human handoff)
- **Dynamic Scripting:** Context-aware conversation flows
- **Qualification Scoring:** BANT framework adapted for NZ real estate
  - Budget (price expectations vs. market reality)
  - Authority (decision maker identification)
  - Need (motivation level, timeline clarity)
  - Timeline (30/60/90 day windows)
- **Objection Handling:** Automated responses to common concerns
- **Appointment Booking:** Calendar integration for listing presentations

**AI Capabilities:**
- Conversational memory across channels
- Sentiment analysis for engagement scoring
- Voice synthesis for NZ-accent English
- Response classification (interested/deflecting/hostile/qualified)

**Decision Logic:**
```
IF sentiment_score > 0.7 AND timeline < 60_days
  → Schedule human agent callback within 2 hours
  
IF asks_pricing_question
  → Trigger Valuation AI preparation
  
IF wants_to_list_now
  → Priority flag + immediate human notification
```

---

### Agent 3: Valuation AI 💰
**Purpose:** Automated property valuation and CMA generation

**Core Functions:**
- **Comparable Analysis:** TradeMe Property Insights + QV data integration
- **Price Prediction:** ML model trained on NZ transaction history
- **CMA Generation:** PDF/Interactive presentation with market context
- **Pricing Strategy:** Recommend listing price, expectations management
- **Value-Add Identification:** Renovation ROI suggestions, staging tips

**Data Inputs:**
- TradeMe API (suburb medians, days on market, clearance rates)
- QV.co.nz (property records, RVs, sales history)
- OneRoof (comparable sales, price estimates)
- Property photos (condition assessment via computer vision)

**Output:**
- 3-tier pricing strategy (conservative/market/optimistic)
- 12-page CMA presentation
- Listing probability score

---

### Agent 4: Buyer Match AI 🎯
**Purpose:** Intelligent buyer-property pairing

**Core Functions:**
- **Buyer Preference Learning:** Implicit (click patterns) + explicit (requirements)
- **Property Scoring:** Match percentage calculation per buyer
- **Alert System:** Instant notifications for high-match properties
- **Viewing Optimization:** Route planning, clustering nearby properties
- **Feedback Loop:** Post-viewing rating to refine matching algorithm

**Matching Algorithm:**
```python
match_score = (
    location_fit * 0.30 +
    budget_alignment * 0.25 +
    feature_match * 0.20 +
    lifestyle_score * 0.15 +
    urgency_multiplier * 0.10
)
```

**Buyer Segments:**
- First home buyers (FHFAQ, KiwiSaver guidance)
- Investors (yield calculations, cashflow analysis)
- Downsizers (single-level, low maintenance focus)
- Relocators (virtual tours, neighborhood guides)

---

### Agent 5: Content Assistant AI 📝
**Purpose:** Marketing content generation and optimization

**Core Functions:**
- **Listing Descriptions:** SEO-optimized, emotionally resonant copy
- **Photo Enhancement:** Auto-brightening, sky replacement (virtual staging)
- **Video Scripts:** Property tour narration, neighborhood highlight reels
- **Social Media:** Facebook/Instagram post generation with best-time posting
- **Email Campaigns:** Newsletter content, market updates, nurture sequences

**Tone Adaptation:**
- Premium listings → Sophisticated, aspirational language
- First home → Warm, accessible, encouraging language
- Investment → Data-driven, ROI-focused content

**Output:**
- TradeMe-ready listing copy
- Social content calendar
- Email nurture sequences (7/14/30 day)

---

### Agent 6: Schedule Assistant AI 📅
**Purpose:** Calendar management and logistics coordination

**Core Functions:**
- **Open Home Coordination:** Scheduling, signage, follow-up automation
- **Private Viewing Booking:** 24/7 availability with conflict resolution
- **Inspection Reminders:** Automated LIM/builder inspection scheduling
- **Deadline Tracking:** Contract conditions, finance dates, settlement tracking
- **Vendor Updates:** Weekly automated reports to sellers

**Integrations:**
- Google Calendar / Outlook
- ShowingTime or similar showing services
- Email/SMS for confirmations
- Map routing for multi-property days

---

### Agent 7: Contract Coordinator AI 📄
**Purpose:** Transaction management and compliance

**Core Functions:**
- **Document Generation:** Sale agreements, disclosure statements, authority to list
- **Condition Tracking:** Finance, building inspection, LIM status monitoring
- **Deadline Alerts:** Countdown timers, 48-hour warnings, critical path management
- **Stakeholder Updates:** Solicitor, buyer, vendor communication threads
- **Compliance Check:** Ensure all NZ legal requirements met

**Document Templates:**
- ADLS Agreement for Sale and Purchase (10th edition)
- Authority to List (REA compliant)
- Privacy Act disclosures
- Healthy Homes statements
- Meth/PSI test results

---

## 2. WORKFLOW AUTOMATION

### SIDE A: Finding Listings (Sellers)

```
┌─────────────────────────────────────────────────────────────────┐
│                    LISTING ACQUISITION FLOW                     │
└─────────────────────────────────────────────────────────────────┘

[LEAD SCOUT AI]
     │
     ├──► Crawl TradeMe for FSBOs
     ├──► Monitor expired listings (90-day window)
     ├──► Scan Neighbourly "for sale by owner" posts
     └──► Detect mortgagee sale notices (NZ Gazette)
     │
     ▼
[ENRICHMENT ENGINE]
     │
     ├──► QV lookup (RV, rates, sales history)
     ├──► Google Street View capture
     └──► Social profile discovery (LinkedIn, Facebook)
     │
     ▼
[LEAD SCORING ALGO]
     │
     Motivation Score = f(days_on_market, price_reductions, 
                          life_events, market_conditions)
     │
     ▼
[OUTREACH AI]
     │
     ├──► Day 1: Personalized email
     ├──► Day 3: SMS follow-up
     ├──► Day 7: Informative market report
     └──► Day 14: Phone call scheduling
     │
     ▼
[QUALIFICATION GATE]
     │
     IF qualified = TRUE ──► [VALUATION AI]
                               │
                               ├──► CMA generation (60 mins)
                               ├──► Pricing strategy document
                               └──► Comparable sales packet
                               │
                               ▼
                          [CALENDAR BOOKING]
                               │
                               └──► Listing presentation scheduled
                               │
                               ▼
                          [HUMAN AGENT]
                               (face-to-face listing presentation)
                               │
                               ▼
                          [ONBOARDING AI]
                               │
                               ├──► Contract sent via DocuSign
                               ├──► Photographer scheduling
                               ├──► Marketing plan confirmation
                               └──► Vendor portal access created
```

### SIDE B: Finding Buyers

```
┌─────────────────────────────────────────────────────────────────┐
│                    BUYER ACQUISITION FLOW                       │
└─────────────────────────────────────────────────────────────────┘

[MULTI-CHANNEL CAPTURE]
     │
     ├──► TradeMe enquiry → Auto-response + CRM entry
     ├──► Website chatbot → Pre-qualification funnel
     ├──► Open home sign-in → QR code → Instant profile
     ├──► Referral form → Warm lead fast-track
     └──► Social media DM → Intent classification
     │
     ▼
[INSTANT ENGAGEMENT]
     │
     ├──► Welcome message (suburb-specific stats)
     ├──► Dream home questionnaire (10 questions)
     └──► Pre-approval guidance (if first home buyer)
     │
     ▼
[BUYER PROFILING AI]
     │
     ├──► Budget estimation (income × 5 rule + deposit)
     ├──► Preference extraction (must-have vs nice-to-have)
     ├──► Timeline determination (30/60/90/180+ days)
     └────► Segment classification
            │
            ├──► FHA (First Home Buyer) → KiwiSaver guidance, 
            │                        solicitor referrals
            ├──► Investor → Yield calculator, cashflow analysis
            ├──► Upsizer → Value-add renovation suggestions
            └──► Relocator → Virtual tour priority, area guides
     │
     ▼
[PROPERTY MATCH ENGINE]
     │
     Real-time monitoring of:
     ├──► TradeMe new listings (every 15 minutes)
     ├──► Off-market opportunities (pocket listings)
     └──► Price reduction alerts
     │
     ▼
[ALERT SYSTEM]
     │
     Match Score > 90% → Instant SMS + Email
     Match Score 70-89% → Daily digest email
     Match Score 50-69% → Weekly newsletter inclusion
     │
     ▼
[VIEWING AUTOMATION]
     │
     ├──► Self-service booking (calendar integration)
     ├──► Reminder sequence (24h → 2h → 15min)
     ├──► Post-viewing feedback form
     └──► Follow-up nurture based on interest level
     │
     ▼
[OFFER COORDINATION]
     │
     ├──► Comparable sales report (last 90 days)
     ├──► Offer strategy recommendations
     ├──► Multi-offer scenario guidance
     └──► LIM/builder inspector coordination
```

---

## 3. DATA SOURCES & INTEGRATIONS

### Primary Data Providers

| Source | Purpose | Access Method | Cost Estimate |
|--------|---------|---------------|---------------|
| **TradeMe API** | Listings, enquiries, market data | Official API (requires approval) | $2,500-5,000/mo |
| **QV CoreLogic** | Property records, RVs, sales history | Business subscription | $500-1,500/mo |
| **OneRoof** | Comparable sales, estimates | API partnership | $300-800/mo |
| **NZ Gazette** | Mortgagee sales, legal notices | RSS/API | Free |
| **LinkedIn Sales Nav** | Owner/prospect research | Premium subscription | $100/mo |

### Secondary Data Sources

- **Neighbourly.co.nz** - Community posts, FSBO mentions
- **Facebook Marketplace** - Owner listings (scraping or manual monitoring)
- **Harcourts / Bayleys websites** - Competitor listing analysis
- **Tenancy Tribunal** - Landlord/tenant issue tracking (investor leads)
- **Companies Office** - Property ownership via company structures

### Internal System Integrations

```
┌──────────────────────────────────────────────────────────────┐
│                      INTEGRATION HUB                         │
└──────────────────┬───────────────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┬──────────────┬─────────────┐
    │              │              │              │             │
    ▼              ▼              ▼              ▼             ▼
┌───────┐    ┌──────────┐   ┌───────┐    ┌──────────┐  ┌──────────┐
│  CRM  │    │  Email   │   │Calendar│    │  Cloud   │  │Payment   │
│       │    │          │   │        │    │ Storage  │  │          │
│Huru/  │    │Outlook/  │   │Google/ │    │Google/   │  │Stripe/   │
│Re-     │    │Gmail API │   │Outlook │    │AWS S3    │  │Xero      │
│Imagine│    │          │   │        │    │          │  │          │
└───────┘    └──────────┘   └───────┘    └──────────┘  └──────────┘
    │              │              │              │             │
    ▼              ▼              ▼              ▼             ▼
[Lead Data]  [Automated    [Viewing     [Document    [Commission]
[Activity   │  Sequences] │  Booking]  │  Storage]  │  Tracking]
[Scores]    │  [Drip       │  [Open      │  [CMA       │  [Agent    │
            │  Campaigns] │  Home Mgmt] │  Library]  │  Payouts]  │
```

### API Specifications

**TradeMe Integration**
```yaml
Rate Limits: 1000 requests/hour
Webhook Support: Yes (new listings, price changes)
Authentication: OAuth 2.0
Data Available:
  - Listing metadata (price, beds, baths, location)
  - Enquiry messages (with permission)
  - Vendor analytics (views, watchlists)
  - Suburb performance dashboards
```

**QV CoreLogic**
```yaml
Data Points:
  - Rating Value (RV) and valuations
  - Sales history (last 15 years)
  - Property details (land area, floor area, construction)
  - Comparable sales algorithm
Batch Processing: Supported (1000 properties/batch)
Update Frequency: Daily
```

---

## 4. TECHNICAL STACK

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                      │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │
│  │ Agent Web │  │  Vendor   │  │  Buyer    │  │  Admin    │    │
│  │  Portal   │  │  Portal   │  │  Portal   │  │ Dashboard │    │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ REST API / GraphQL
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (Kong/AWS)                     │
│         Rate limiting, Auth (JWT), Request routing              │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌────────────────┐    ┌───────────────┐
│   AI AGENT    │    │  WORKFLOW      │    │  INTEGRATION  │
│   SERVICES    │    │  ENGINE        │    │  LAYER        │
│               │    │                │    │               │
│ 7 agent       │    │ Node-RED /     │    │ API adapters  │
│ containers    │    │ Temporal       │    │ for external  │
│ (Python/TS)   │    │ (orchestration)│    │ services      │
└───────────────┘    └────────────────┘    └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ PostgreSQL   │  │    Redis     │  │ Elasticsearch│          │
│  │  (Primary DB)│  │   (Cache/    │  │  (Search/    │          │
│  │              │  │   Sessions)  │  │   Analytics) │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  S3/MinIO    │  │   Pinecone   │  │   InfluxDB   │          │
│  │ (Documents/  │  │  (Vector DB  │  │  (TimeSeries │          │
│  │   Images)    │  │   for RAG)   │  │   Metrics)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Selection

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Backend API** | Node.js (Express/NestJS) + Python (FastAPI) | Speed + ML ecosystem |
| **AI/ML Engine** | Python (LangChain, OpenAI/Claude APIs) | Rapid agent development |
| **Database** | PostgreSQL 16 (Aurora/RDS) | ACID compliance, JSON support |
| **Vector DB** | Pinecone / Weaviate | Semantic search, RAG |
| **Cache** | Redis | Session, rate limiting |
| **Search** | Elasticsearch | Property search, fuzzy matching |
| **Queue** | RabbitMQ / AWS SQS | Async task processing |
| **Containers** | Docker + Kubernetes (EKS) | Scalability, isolation |
| **Frontend** | Next.js 14 (React) | SSR, great DX |
| **Mobile** | React Native | Code sharing |
| **Infrastructure** | Terraform + AWS | IaC, NZ regions available |

### AI Model Stack

```yaml
Text Generation:
  Primary: OpenAI GPT-4-turbo
  Fallback: Anthropic Claude 3
  Local: Ollama/Llama3 (for sensitive data)

Embeddings:
  Provider: OpenAI text-embedding-3-large
  Dimensions: 3072
  Use case: Property descriptions, buyer preferences

Vision:
  Provider: GPT-4 Vision, Claude 3 Opus
  Use case: Property photo analysis, condition assessment

Speech:
  TTS: ElevenLabs (NZ accent fine-tuning)
  ASR: Whisper local deployment

Fine-tuned Models:
  - NZ real estate language model (domain adaptation)
  - Email response generator (agent voice matching)
  - Property description optimizer
```

### DevOps & Deployment

```yaml
CI/CD: GitHub Actions → ArgoCD
Monitoring: Datadog / New Relic
Logging: ELK Stack (Elasticsearch, Logstash, Kibana)
Alerting: PagerDuty + Slack
Backup: Automated daily + point-in-time recovery
Security:
  - Encryption at rest (AES-256)
  - TLS 1.3 in transit
  - SOC 2 Type II compliance target
  - NZ Privacy Act compliance

Environments:
  - Development (local)
  - Staging (AWS ap-southeast-2)
  - Production (AWS ap-southeast-2)
```

---

## 5. IMPLEMENTATION ROADMAP

### Phase 1: MVP (Months 1-3)
**Goal:** One agency pilot, core automations live

#### Deliverables:
- [ ] Lead Scout AI (TradeMe FSBO monitoring)
- [ ] Outreach AI (email sequences, basic qualification)
- [ ] Simple CRM integration (Real Estate CRM API)
- [ ] Buyer Match AI (basic property alerts)
- [ ] Web dashboard for agents
- [ ] 3 pilot agents, 2 admins

#### Success Criteria:
- 50 qualified leads generated/week
- 70% email open rate on sequences
- 5 listing presentations scheduled by AI
- < 2 hour response time on enquiries

#### Budget: $75,000 - $100,000

---

### Phase 2: Scale (Months 4-8)
**Goal:** Multi-agency deployment, full workflow automation

#### Deliverables:
- [ ] Valuation AI with CMA generation
- [ ] Content Assistant AI (listings, social)
- [ ] Schedule Assistant (open home coordination)
- [ ] Contract Coordinator (document management)
- [ ] Vendor Portal (seller access)
- [ ] Buyer Portal (saved searches, favorites)
- [ ] Mobile app for agents
- [ ] 5 agency partnerships

#### Success Criteria:
- 500+ qualified leads/week across all agencies
- 25% reduction in agent admin time
- 40% faster time-to-listing
- 85% buyer match accuracy
- $500K+ ARR

#### Budget: $200,000 - $300,000

---

### Phase 3: Enterprise (Months 9-15)
**Goal:** Enterprise offering, predictive analytics

#### Deliverables:
- [ ] Market Analyst AI (price prediction, trend analysis)
- [ ] Advanced analytics (churn prediction, LTV modeling)
- [ ] White-label solution for large franchises
- [ ] API platform for third-party integrations
- [ ] Compliance automation (REA standards)
- [ ] National rollout (all NZ metros)

#### Success Criteria:
- 50+ agencies onboarded
- 20% market penetration (Auckland)
- $2M+ ARR
- 60% average admin reduction
- NZ-wide market intelligence reports

#### Budget: $500,000 - $750,000

---

### Gantt Chart Overview

```
MONTH    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15
         ├────┴────┤
         │ Phase 1 │
         └─────────┴──────────────────────────────────────┐
                                │        Phase 2          │
                                └─────────────────────────┴──────────────────────┐
                                                           │     Phase 3       │
                                                           └───────────────────┘

Milestone Timeline:
  ▲                              ▲                              ▲
  │ M1: Architecture complete    │ M4: Pilot live               │ M9: Enterprise launch
  │ M2: Lead AI v1 shipped       │ M6: 3 agencies live          │ M12: National expansion
  │ M3: First listing from AI    │ M8: 500+ weekly leads        │ M15: Profitability
```

---

## 6. ROI METRICS & SUCCESS MEASUREMENT

### Key Performance Indicators (KPIs)

#### Lead Generation Metrics
| Metric | Baseline | Phase 1 Target | Phase 2 Target | Phase 3 Target |
|--------|----------|----------------|----------------|----------------|
| Qualified leads/week | 10 (manual) | 50 | 500 | 5,000 |
| Lead response time | 4 hours | < 2 hours | < 30 min | < 5 min |
| Email open rate | 25% | 70% | 75% | 80% |
| Conversion to listing | 5% | 8% | 12% | 15% |

#### Operational Efficiency
| Metric | Baseline | Phase 1 | Phase 2 | Phase 3 |
|--------|----------|---------|---------|---------|
| Admin hours/property | 15 hrs | 12 hrs | 8 hrs | 4 hrs |
| CMA generation time | 3 hours | 2 hours | 30 min | 10 min |
| Listing description time | 45 min | 30 min | 5 min | 2 min |
| Agent productivity (listings/month) | 4 | 5 | 8 | 12 |

#### Buyer Engagement
| Metric | Baseline | Phase 2 | Phase 3 |
|--------|----------|---------|---------|
| Property match accuracy | 40% | 75% | 90% |
| Buyer-to-viewing conversion | 15% | 25% | 35% |
| Time from enquiry to viewing | 3 days | 1 day | 4 hours |

---

### Financial ROI Projections

#### Agency Cost Savings (Annual)
```
Scenario: 10-agent agency

Cost Per Agent (Current):
  - Admin assistant (shared): $15,000
  - Marketing support (outsourced): $8,000
  - CRM/marketing tools: $6,000
  = $29,000/agent/year

With AI System:
  - AI platform subscription: $12,000/agent/year
  - Reduced admin needs: -$8,000/agent/year
  - Reduced marketing costs: -$4,000/agent/year
  = $20,000/agent/year

Net Savings: $9,000/agent/year
For 10 agents: $90,000/year

Additional Revenue (Productivity Gain):
  - Extra listing per agent per month
  - 10 agents × 12 months × $25,000 avg commission × 2% split
  = $60,000/month = $720,000/year incremental

Total ROI: $810,000/year
```

#### Platform Revenue Model
```
Pricing Tiers:

STARTER ($299/agent/month):
  - Lead Scout AI
  - Outreach AI (Basic sequences)
  - Buyer Match AI
  - Email support

PROFESSIONAL ($599/agent/month):
  - Everything in Starter
  - Valuation AI (CMA generation)
  - Content Assistant
  - Schedule Assistant
  - Priority support

ENTERPRISE ($999+/agent/month):
  - Everything in Professional
  - Contract Coordinator
  - Market Analyst AI
  - White-label option
  - Custom integrations
  - Dedicated success manager

Break-even: 50 agents at Professional tier = $360K ARR
Profitability target: 200 agents = $1.44M ARR
```

---

### Success Tracking Dashboard

**Real-time Metrics:**
- Active leads in pipeline
- AI-generated conversations today
- Properties matched this week
- Time saved vs. baseline (accumulated hours)
- Revenue attributed to AI (tracked via UTM/CRM)

**Weekly Reports:**
- Lead quality score distribution
- Conversion funnel analysis
- Agent satisfaction (NPS)
- System uptime SLAs

**Monthly Business Reviews:**
- ROI achievement vs. projections
- Feature adoption rates
- Churn analysis
- Expansion revenue

---

## 7. RISK ASSESSMENT & MITIGATION

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| TradeMe API access denied | Medium | High | Direct partnership outreach, alternative scraping (legal), cache strategy |
| Data privacy concerns (Privacy Act) | Low | High | Privacy by design, data minimization, audit logging |
| Agent resistance to AI | Medium | Medium | Change management program, prove value before rollout, opt-in initially |
| AI hallucination in valuations | Low | High | Human-in-the-loop for CMAs, confidence scoring, disclaimer requirements |
| NZ real estate market downturn | Medium | Medium | Freemium tier for lean times, efficiency gains still valuable |
| Competitor launch (similar product) | Medium | High | Speed to market, trade secret protection, exclusive partnerships |

---

## 8. COMPLIANCE & LEGAL CONSIDERATIONS

### New Zealand Regulatory Requirements

**Real Estate Agents Act 2008 (REAA)**
- All automated communications must be clearly identifiable as AI-assisted
- Licensee responsibility remains with human agent
- Record keeping requirements (7 years)

**Privacy Act 2020**
- Privacy Impact Assessment required
- Data breach notification procedures
- Individual data access/deletion rights
- Overseas transfer restrictions (cloud providers)

**Fair Trading Act**
- No misleading automated valuations
- Clear disclaimers on AI-generated content
- Truth in advertising standards apply to bot communications

**Anti-Money Laundering**
- Customer due diligence tracking
- Suspicious transaction flagging
- Record retention for 5 years

---

## 9. APPENDICES

### Appendix A: API Integration Specifications

[Detailed OpenAPI specs would be included here]

### Appendix B: Database Schema

[Entity-relationship diagrams and table definitions]

### Appendix C: User Interface Mockups

[Wireframes for agent dashboard, vendor portal, buyer app]

### Appendix D: Sample AI Conversations

[Example transcript of Lead Scout → Outreach → Qualification → Handoff]

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-12 | Enki AI | Initial framework |

**Next Review Date:** 2026-04-12

---

*This document is confidential and proprietary. Do not distribute without written permission.*
