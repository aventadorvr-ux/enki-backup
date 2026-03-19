# NZ REAL ESTATE AI AGENT SYSTEM
## PRE-BUILD PLAN & GREEN LIGHT DOCUMENT
**Version:** 1.0  
**Date:** March 18, 2026  
**Status:** AWAITING GREEN LIGHT

---

## 1. EXECUTIVE SUMMARY

### Project
Build a 5-agent AI system for New Zealand real estate agencies.

### Investment
**$8,000** (Hybrid Approach - Option 2)

### Timeline
**4 weeks to MVP** + **6 weeks to v1.0** = 10 weeks total

### Target Outcome
$1M-$6M ARR potential through enterprise contracts with 7 major NZ real estate companies.

---

## 2. PROJECT SCOPE

### IN SCOPE
- 5 autonomous AI agents (Lead, Content, Scheduling, Market Intelligence, Transaction)
- Web dashboard for agent management
- Integration with Trade Me + Realestate.co.nz
- Mobile-responsive interface
- REA compliance features
- Pilot program for 10 beta agents

### OUT OF SCOPE (Future Phases)
- Mobile native apps
- Australia expansion
- White-label solution
- Advanced analytics/BI
- Third-party CRM deep integrations (Salesforce, etc.)

---

## 3. TECHNICAL ARCHITECTURE

### 3.1 Technology Stack
| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14 + Tailwind CSS |
| Backend | Node.js + Express |
| Database | PostgreSQL |
| AI/LLM | OpenAI GPT-4 + Assistants API |
| Hosting | Vercel (frontend) + Railway (backend) |
| Auth | Clerk |
| Payments | Stripe |
| Scheduler | node-cron / Bull MQ |
| Scraping | Puppeteer (js-fetch.js exists) |
| Email | SendGrid |
| SMS | Twilio |

### 3.2 Detailed Software Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    CLIENT LAYER                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │   Web App    │  │  Mobile Web  │  │   Telegram   │  │      Email Client        │ │
│  │  (Next.js)   │  │ (Responsive) │  │     Bot      │  │   (SendGrid Inbound)     │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └───────────┬──────────────┘ │
└─────────┼─────────────────┼─────────────────┼──────────────────────┼────────────────┘
          │                 │                 │                      │
          └─────────────────┴─────────────────┴──────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                 API GATEWAY                                          │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │                          Next.js API Routes                                     │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────────────────┐ │ │
│  │  │  /api/auth  │  │  /api/leads │  │ /api/content│  │   /api/integrations    │ │ │
│  │  │   (Clerk)   │  │             │  │             │  │                        │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CORE SERVICES LAYER                                     │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │                        AGENT ORCHESTRATOR (Node.js)                             │ │
│  │  ┌──────────────────────────────────────────────────────────────────────────┐  │ │
│  │  │                     Message Queue (Bull MQ / Redis)                       │  │ │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │  │ │
│  │  │  │  Lead   │  │ Content │  │Schedule │  │ Market  │  │   Transaction   │ │  │ │
│  │  │  │  Agent  │  │  Agent  │  │  Agent  │  │  Intel  │  │  Coordinator    │ │  │ │
│  │  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────────┬────────┘ │  │ │
│  │  └───────┼────────────┼────────────┼────────────┼────────────────┼──────────┘  │ │
│  │          │            │            │            │                │             │ │
│  └──────────┼────────────┼────────────┼────────────┼────────────────┼─────────────┘ │
│             │            │            │            │                │               │
│             ▼            ▼            ▼            ▼                ▼               │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                     SHARED SERVICES (All Agents)                             │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │   │
│  │  │ OpenAI GPT-4 │  │  Context     │  │   Memory     │  │   Compliance     │  │   │
│  │  │   Service    │  │   Engine     │  │   Store      │  │    Checker       │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                              │
│                                                                                      │
│  ┌──────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│  │      PostgreSQL Database     │  │              External APIs                   │   │
│  │  ┌────────────────────────┐  │  │  ┌──────────┐ ┌──────────┐ ┌─────────────┐ │   │
│  │  │    leads table         │  │  │  │Trade Me  │ │Realestate│ │  Google     │ │   │
│  │  │    agents table        │  │  │  │ Scraper  │ │.co.nz    │ │  Calendar   │ │   │
│  │  │    properties table    │  │  │  └──────────┘ └──────────┘ └─────────────┘ │   │
│  │  │    conversations table │  │  │                                            │   │
│  │  │    templates table     │  │  │  ┌──────────┐ ┌──────────┐ ┌─────────────┐ │   │
│  │  │    schedules table     │  │  │  │ DocuSign │ │ SendGrid │ │   Twilio    │ │   │
│  │  │    analytics table     │  │  │  │   API    │ │   API    │ │    SMS      │ │   │
│  │  └────────────────────────┘  │  │  └──────────┘ └──────────┘ └─────────────┘ │   │
│  └──────────────────────────────┘  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           INFRASTRUCTURE LAYER                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                  │
│  │   Vercel Edge    │  │  Railway Server  │  │   GitHub Repo    │                  │
│  │   (Frontend)     │  │   (Backend/API)  │  │   (Source Ctrl)  │                  │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Data Flow Diagram

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                           LEAD FLOW (Primary Use Case)                          │
│                                                                                  │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────┐  │
│   │  Lead    │────▶│  Trade   │────▶│  Lead    │────▶│   AI     │────▶│ Lead │  │
│   │  Source  │     │  Me API  │     │  Parser  │     │Qualifier │     │Score │  │
│   └──────────┘     └──────────┘     └──────────┘     └────┬─────┘     └──┬───┘  │
│                                                           │               │      │
│                                                           ▼               ▼      │
│                                                      ┌──────────┐     ┌────────┐ │
│                                                      │  GPT-4   │     │  Hot?  │ │
│                                                      │ Analysis │     └────┬───┘ │
│                                                      └────┬─────┘          │     │
│                                                           │                │     │
│                              ┌────────────────────────────┘                │     │
│                              │                                             │     │
│                              ▼                                             ▼     │
│   ┌──────────┐          ┌──────────┐     ┌──────────┐     ┌──────────┐  ┌─────┐ │
│   │  Agent   │◀─────────│  Email   │────▶│  Track   │────▶│  Follow  │  │YES──┼─┼──┐
│   │Notified  │          │  Sent    │     │  Reply   │     │  Up      │  └─────┘ │  │
│   └──────────┘          └──────────┘     └──────────┘     └──────────┘          │  │
│                                                                                  │  │
│   ┌──────────┐                                                                   │  │
│   │  Cold    │◀──────────────────────────────────────────────────────────────────┼──┘
│   │  Nurture │◀──────────────────────────────────────────────────────────────────┘
│   │  Sequence│
│   └──────────┘
└────────────────────────────────────────────────────────────────────────────────┘
```

### 3.4 Agent-to-Agent Communication

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                          AGENT ORCHESTRATION PATTERN                            │
│                                                                                  │
│                              ┌─────────────┐                                     │
│                              │  ORCHESTRATOR│                                    │
│                              │   (Router)   │                                    │
│                              └──────┬──────┘                                     │
│                                     │                                            │
│           ┌─────────────────────────┼─────────────────────────┐                  │
│           │                         │                         │                  │
│           ▼                         ▼                         ▼                  │
│    ┌─────────────┐           ┌─────────────┐           ┌─────────────┐          │
│    │ LEAD AGENT  │◀─────────▶│ CONTENT AGENT│◀─────────▶│SCHEDULING   │          │
│    │             │ shared    │              │ shared    │   AGENT     │          │
│    │ - Capture   │ context   │ - Property   │ context   │ - Calendar  │          │
│    │ - Qualify   │───────────▶│   desc       │───────────▶│   sync      │          │
│    │ - Route     │           │ - Social     │           │ - Bookings  │          │
│    └─────────────┘           └─────────────┘           └─────────────┘          │
│           │                         │                         │                  │
│           │    ┌────────────────────┘                         │                  │
│           │    │                                               │                  │
│           ▼    ▼                                               ▼                  │
│    ┌─────────────────────────────────────────────────────────────────────┐      │
│    │                         SHARED CONTEXT STORE                       │      │
│    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐ │      │
│    │  │Lead Data │  │Property  │  │  Agent   │  │   Conversation       │ │      │
│    │  │          │  │  Info    │  │ Profile  │  │   History            │ │      │
│    │  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘ │      │
│    └─────────────────────────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. PEER REVIEW & RISK ASSESSMENT

**Reviewer:** External System Analysis  
**Date:** March 18, 2026  
**Verdict:** 8.5/10 — Strong, realistic, scalable (with scope reduction)

---

### 4.1 Architecture Quality Assessment

| Area | Score | Notes |
|------|-------|-------|
| **Overall Architecture** | 8.5/10 | Real SaaS architecture, not a hacky GPT wrapper. Clear multi-agent design with proper separation of concerns. |
| **Execution Feasibility** | 7/10 | Achievable but requires disciplined scope management. |
| **Market Fit** | 9/10 | NZ real estate = high commission market, agents spend heavily on tools, clear ROI angle. |
| **Risk Level** | Medium-High | Scraping dependency and over-engineering are primary risks. |
| **MVP Design** | 8/10 | No-code MVP approach is correct and reduces burn risk. |
| **Overengineering Risk** | ⚠️ High | Building 5 agents initially = scope creep danger. |

---

### 4.2 What Works Well Immediately

**✅ Lead Agent**
- High ROI, fastest validation
- Real estate agents care deeply about speed-to-lead
- Auto-response <2 min = huge value

**✅ Content Agent**
- Immediate perceived value
- Saves agents hours weekly
- Easy to demo → good for sales

**✅ No-code MVP approach**
- Smart move → reduces burn risk
- Validates demand before heavy build

---

### 4.3 Critical Risks Identified

#### ⚠️ RISK 1: Scraping Trade Me / Realestate.co.nz
**Severity:** HIGH

**Problem:**
- Platforms detect bots aggressively
- Rate-limiting and IP blocking
- Puppeteer scraping at scale = fragile
- Legal/ToS exposure

**Impact:**
- System breaks silently
- Legal exposure
- Reliability issues at scale

**Mitigation:**
- **Phase 1:** Use email ingestion (lead notifications) instead of scraping
- **Phase 2:** Pursue official APIs or data partnerships
- **Phase 3:** Implement proxy rotation and rate limiting if scraping required
- **Fallback:** Manual lead entry via dashboard (agents forward emails)

---

#### ⚠️ RISK 2: Agent Orchestration Complexity
**Severity:** MEDIUM

**Problem:**
- Multi-agent systems conflict (who responds?)
- Context drift between agents
- Hard to debug when issues arise

**Reality Check:**
- You don't need 5 agents at MVP
- You need 2 REALLY GOOD agents

**Mitigation:**
- **V1 Scope Reduction:** Build only Lead Agent + Content Agent
- **Defer:** Scheduling, Market Intel, Transaction Coordinator to V2
- **Simplify:** Single orchestrator with clear handoff rules

---

#### ⚠️ RISK 3: Vector DB Overkill (Early Stage)
**Severity:** LOW-MEDIUM

**Problem:**
- Pinecone/pgvector adds cost + complexity
- Not needed for: Lead replies, Content generation

**Mitigation:**
- **Phase 1-2:** Use PostgreSQL with JSONB for context storage
- **Phase 3+:** Add vector DB only when semantic search becomes critical

---

#### ⚠️ RISK 4: UX / Adoption Risk
**Severity:** HIGH

**Problem:**
- Agents are: Not technical, Busy, Resistant to change
- If system feels like "a dashboard they need to learn" → they won't use it

**Mitigation:**
- Chat-first interface (Telegram integration already planned)
- "Forward a lead → get reply instantly" workflow
- "Paste listing → get content" workflow
- Zero training required approach

---

#### ⚠️ RISK 5: Message Quality Risk
**Severity:** MEDIUM

**Problem:**
- If AI replies sound generic or "off"
- Agents stop trusting immediately

**Mitigation:**
- Human-in-the-loop for first 100 responses
- Template library with agent-approved examples
- Tone matching to individual agent style
- Confidence scoring → low confidence = human review

---

#### ⚠️ RISK 6: Data Privacy (NZ Laws)
**Severity:** MEDIUM

**Problem:**
- Handling client data
- Messaging automation compliance

**Mitigation:**
- Privacy policy drafted before launch
- Consent handling built into onboarding
- GDPR/Privacy Act compliance review

---

### 4.4 Strategic Recommendation

**Current Plan:** Build 5 agents

**Recommended Plan:** Build 2 agents initially

#### V1 REDUCED SCOPE (MVP)

**CORE PRODUCT:** "AI Deal Assistant"

**Agent 1: Lead Response Engine**
- Instant reply to all leads
- Qualification questions
- Automatic follow-ups
- Hot lead routing

**Agent 2: Listing Content Generator**
- Property descriptions
- Social media posts
- Email templates

**Deferred to V2:**
- ❌ Scheduling Agent
- ❌ Market Intel Agent  
- ❌ Transaction Coordinator
- ❌ Complex orchestration

---

### 4.5 Commercial Viability Reality Check

**Original Projection:** $1M–$6M ARR Year 1

**Realistic Curve:**

| Timeline | Milestone | Revenue |
|----------|-----------|---------|
| Months 1-3 | Validation | $0 |
| Months 4-6 | First paying customers | $5-20k MRR |
| Month 12 | Stable growth | $12-40k MRR |
| **Year 1 Total** | **Realistic ARR** | **$150k–$500k** |

**Still very good** — but set expectations correctly.

---

### 4.6 Revised Green Light Conditions

**✅ PROCEED IF:**
- Scope reduced to 2 agents initially (Lead + Content)
- Scraping dependency avoided in Phase 1
- Lead response speed = core value proposition
- Real agents validated in Week 1

**❌ DO NOT PROCEED IF:**
- Trying to build all 5 agents immediately
- Heavy reliance on web scraping
- Overbuilding infrastructure before revenue

---

### 4.7 Final Strategic Insight

**Your real product is:**
> "AI that replies to property leads faster than any human agent"

Everything else is secondary.

**Blunt Assessment:**
You're 1–2 decisions away from overbuilding and stalling. Simplify V1 HARD. Validate with 2 agents. Scale to 5 only after revenue proves demand.

**Recommendation:**
👉 **GREEN LIGHT — with reduced V1 scope**

---

## 5. PHASE BREAKDOWN (REVISED — 2-Agent MVP Focus)

> **Per peer review:** Scope reduced to 2 core agents for V1. Scheduling, Market Intel, and Transaction Coordinator deferred to V2.

---

### PHASE 1: NO-CODE MVP (Week 1) — $1,000
**Goal:** Validate demand with 5 agents before building

**Deliverables:**
- [ ] Landing page (Vercel + Next.js template)
- [ ] Zapier workflow: Email lead → GPT-4 → Email response (NO scraping)
- [ ] Google Sheets database (leads, agents, properties)
- [ ] Basic dashboard (Google Data Studio or Retool)
- [ ] 5 beta agent onboarding

**Success Criteria:**
- 5 agents actively using system
- >50 leads processed via email ingestion
- >80% satisfaction rating
- **Key validation:** Agents actually forward leads and use AI responses

**Budget:**
- Zapier: $50
- OpenAI API: $200
- Domain/hosting: $50
- Design (Figma to code): $500
- Buffer: $200

---

### PHASE 2: PROPER BUILD — CORE 2 AGENTS (Weeks 2-6) — $5,000
**Goal:** Replace no-code with production code for Lead + Content Agents only

**Sprint 1 (Week 2): Infrastructure + Auth**
- [ ] GitHub repo setup
- [ ] Vercel + Railway deployment pipeline
- [ ] PostgreSQL schema design
- [ ] Clerk authentication integration
- [ ] Basic dashboard shell

**Sprint 2 (Week 3): Lead Agent Core**
- [ ] Email ingestion system (webhook-based, no scraping)
- [ ] Lead qualification engine (GPT-4)
- [ ] Auto-response system with templates
- [ ] Lead scoring algorithm
- [ ] Hot/cold lead routing
- [ ] Follow-up sequence logic

**Sprint 3 (Week 4): Lead Agent Polish**
- [ ] Human-in-the-loop review queue
- [ ] Response tone matching
- [ ] Confidence scoring
- [ ] Analytics dashboard (response times, conversion)
- [ ] Mobile-responsive lead view

**Sprint 4 (Week 5): Content Agent Core**
- [ ] Property description generator
- [ ] Social media post generator (Instagram/Facebook)
- [ ] Email newsletter generator
- [ ] Content templates library
- [ ] SEO optimization suggestions

**Sprint 5 (Week 6): Content Agent Polish + Integration**
- [ ] "Paste listing URL → get content" workflow
- [ ] Image selection suggestions
- [ ] Content calendar integration
- [ ] Approval workflow (draft → review → publish)
- [ ] Performance tracking (engagement metrics)

**Success Criteria:**
- Lead Agent: <2 min response time, 90%+ automated
- Content Agent: 5 content pieces per property in <30 seconds
- 10 beta agents migrated from no-code
- 99% uptime
- **Revenue validation:** At least 3 agents willing to pay

**Budget:**
- Developer time: $3,500
- Infrastructure: $500
- APIs (OpenAI, SendGrid): $500
- Design polish: $500

---

### PHASE 3: PILOT + REFINEMENT (Weeks 7-8) — $1,500
**Goal:** Enterprise-ready product with 2 agents

**Week 7:**
- [ ] SOC 2 compliance documentation started
- [ ] Security audit
- [ ] Enterprise onboarding flow
- [ ] Team/company account structure
- [ ] Admin panel for managers

**Week 8:**
- [ ] Case studies from beta agents (3 minimum)
- [ ] Sales deck for enterprise clients
- [ ] Pricing page live with Stripe integration
- [ ] ROI calculator for prospects
- [ ] Help documentation + video tutorials

**Deferred to V2 (Post-Revenue):**
- ❌ Scheduling Agent (calendar integration)
- ❌ Market Intelligence Agent (competitor tracking)
- ❌ Transaction Coordinator (deadlines/signatures)
- ❌ Advanced analytics/BI
- ❌ Realestate.co.nz scraping (use email ingestion instead)

**Success Criteria:**
- 25 agents onboarded
- 3 enterprise prospects in pipeline
- Product-market fit confirmed via paid conversions
- Ready for sales push

**Budget:**
- Security/compliance: $400
- Sales materials: $300
- Stripe integration: $200
- Testing/buffer: $600

---

### PHASE 4: SCALE + V2 AGENTS (Post Milestone) — $500 + Revenue
**Trigger:** $10k MRR achieved

**V2 Scope (3 Additional Agents):**
- Scheduling Agent: Calendar sync, booking system, reminders
- Market Intelligence Agent: Competitor tracking, CMA generation
- Transaction Coordinator: Deadline tracking, DocuSign, compliance

**Budget:**
- Initial planning: $500
- Remaining build funded by revenue

---

## 6. TOTAL BUDGET BREAKDOWN (REVISED)

| Phase | Cost | Cumulative | Deliverable |
|-------|------|------------|-------------|
| Phase 1: No-Code MVP | $1,000 | $1,000 | 5 beta agents validated |
| Phase 2: Core 2 Agents | $5,000 | $6,000 | Lead + Content agents live |
| Phase 3: Pilot Ready | $1,500 | $7,500 | Enterprise-ready product |
| Phase 4: V2 Planning | $500 | **$8,000** | 3 additional agents scoped |

**Note:** Original $8k budget maintained, but reallocated. Removed $2k from 3 deferred agents, added $1k to core build quality.

### Ongoing Costs (Monthly)
- Hosting: $100
- OpenAI API: $300-600 (reduced with 2 agents vs 5)
- Database: $50
- Email/SMS: $150
- **Total:** ~$600-900/mo

---

## 7. TIMELINE (REVISED — 8 Week V1)

```
WEEK:  1    2    3    4    5    6    7    8
       ├────┴────┴────┤
       │  NO-CODE MVP │  $1k
                      ├────┴────┴────┴────┴────┤
                      │  LEAD + CONTENT AGENTS │  $5k
                                                ├────┴────┤
                                                │  PILOT  │ $1.5k

MILESTONES:
▓ Week 1: 5 beta agents using no-code MVP (email-based)
▓ Week 4: Lead Agent live (<2min response)
▓ Week 6: Content Agent live (5 content types)
▓ Week 8: Enterprise-ready, sales push begins

V2 SCOPE (Post $10k MRR):
├─ Scheduling Agent
├─ Market Intelligence Agent
└─ Transaction Coordinator
```

---

## 8. DELIVERABLES CHECKLIST (REVISED — V1)

### Technical Deliverables
- [ ] Source code repository (GitHub)
- [ ] Production deployment (Vercel + Railway)
- [ ] PostgreSQL schema + migrations
- [ ] API documentation
- [ ] Environment configuration
- [ ] CI/CD pipeline

### Product Deliverables (V1 — 2 Agents)
- [ ] **Lead Response Agent** — Instant reply, qualification, routing
- [ ] **Content Agent** — Property descriptions, social posts, emails
- [ ] Agent dashboard
- [ ] Admin panel
- [ ] Landing page
- [ ] Payment system (Stripe)
- [ ] Mobile-responsive UI

### Deferred to V2 (3 Agents)
- [ ] Scheduling Agent
- [ ] Market Intelligence Agent
- [ ] Transaction Coordinator

### Business Deliverables
- [ ] 25 beta agents onboarded
- [ ] 3 enterprise prospects in pipeline
- [ ] Case studies (3+)
- [ ] Sales deck
- [ ] Pricing strategy validated
- [ ] REA compliance documentation

---

## 8. RISK MITIGATION

| Risk | Mitigation |
|------|------------|
| Agents don't adopt | No-code MVP validates demand first |
| Long sales cycles | Free pilots + bottom-up adoption |
| AI hallucinations | Human-in-the-loop for critical actions |
| Technical debt | Clean architecture from Week 2 |
| Run out of budget | Milestone-based, can stop after any phase |
| Competitor emerges | Speed to market (4 weeks) |
| Integration fails | Fallback to manual for MVP |

---

## 9. SUCCESS METRICS

### Technical
- Uptime: >99%
- Response time: <2s
- Lead processing: 24/7 automated
- Agent satisfaction: >80%

### Business
- Beta agents: 50 by Week 10
- Enterprise prospects: 3 in pipeline
- Revenue potential: $1M+ ARR validated
- Cost per lead: <$1 (vs $50+ manual)

---

## 10. GREEN LIGHT CHECKLIST (REVISED)

### REQUIRED CONDITIONS (Per Peer Review)

**✅ PROCEED ONLY IF:**
- [ ] **$8,000 budget approved and available**
- [ ] **8-week timeline acceptable** (reduced from 10)
- [ ] **Scope reduced to 2 agents accepted** (Lead + Content only)
- [ ] **No scraping dependency in Phase 1** — email ingestion only
- [ ] **Lead response speed = core value proposition** agreed
- [ ] **Decision maker available for weekly check-ins**
- [ ] **5 beta agents identified for Phase 1**
- [ ] **OpenAI API key ready**

### STRATEGIC DECISIONS

- [ ] **Domain name decided** (recommend: agentpro.nz, realtorai.nz, or similar)
- [ ] **Target first enterprise client identified** (recommend: Barfoot & Thompson)
- [ ] **Legal entity ready** (for contracts)

### INFRASTRUCTURE SETUP

- [ ] Stripe account created
- [ ] SendGrid account created
- [ ] GitHub organization setup
- [ ] Figma design system started

### V2 DEFERRED SCOPE (Acknowledged)

**❌ NOT IN V1:**
- Scheduling Agent
- Market Intelligence Agent
- Transaction Coordinator
- Trade Me / Realestate.co.nz scraping
- Vector database (pgvector/Pinecone)

---

## 11. IMMEDIATE NEXT STEPS (Upon Green Light)

1. **Day 1:** Create GitHub repo, setup Vercel + Railway
2. **Day 2:** Configure OpenAI API, create database schema
3. **Day 3:** Build landing page, setup Zapier workflows
4. **Day 4:** Onboard first beta agent
5. **Day 5:** Begin lead flow testing

---

## 13. APPROVAL

**Project:** NZ Real Estate AI Agent System  
**Investment:** $8,000  
**Timeline:** 8 weeks (V1)  
**Scope:** 2 AI Agents (Lead + Content) — 3 additional agents deferred to V2  
**Expected Outcome:** $150k–$500k ARR Year 1 (realistic projection)

### STRATEGIC RATIONALE
Per peer review analysis:
- **Architecture:** 8.5/10 — Solid, scalable foundation
- **Market Fit:** 9/10 — High commission market, clear ROI
- **Risk Level:** Medium-High — Mitigated by scope reduction
- **Key Insight:** "AI that replies to property leads faster than any human agent"

### GREEN LIGHT AUTHORIZATION

**Approved by:** _________________________  
**Date:** _________________________  
**Scope Confirmation:** I understand V1 = 2 agents, V2 = additional 3 agents post-revenue  
**Notes:** _________________________

---

**END OF PRE-BUILD PLAN**

*Upon green light, Nemo proceeds with Phase 1 execution (No-Code MVP).*
