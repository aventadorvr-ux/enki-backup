# NEMO Real Estate AI Platform - Critical User Flows

**Date:** March 2026  
**Version:** 1.0  
**Primary Persona:** Sarah Chen (Lead Agent)  
**Secondary:** Emma Taylor (First-Time Investor)

---

## Flow 1: Agent Lead Qualification Workflow

**Goal:** Rapidly qualify and route leads to appropriate action
**Trigger:** New lead enters system (website form, phone call, referral)
**Success Criteria:** Lead scored and routed within 2 minutes

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  LEAD ARRIVES                                                  │
│  [* Form submission SMS: New lead from Webchat *]              │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  AI ANALYSIS                                                   │
│  • Parse inquiry details                                       │
│  • Cross-reference with past interactions                      │
│  • Score: Hot / Warm / Cold (0-100)                           │
│  • Recommend: Call / Email / Nurture / Auto-respond            │
└──────────────────────┬──────────────────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      ┌──────┐   ┌──────┐    ┌──────┐
      │ HOT  │   │ WARM │    │ COLD │
      │ 75+  │   │ 50-74│    │ <50  │
      └──┬───┘   └──┬───┘    └──┬───┘
         │          │           │
         ▼          ▼           ▼
┌─────────────────────────────────────────────────────────────────┐
│  ROUTING & ACTIONS                                             │
│                                                                 │
│  HOT: ────────────────────────                                  │
│  • Push notification to agent                                 │
│  • Auto-generate call script with context                     │
│  • Schedule attempt for within 4 hours                        │
│  • Add to "Hot Leads" board                                   │
│                                                                 │
│  WARM: ───────────────────────                                  │
│  • Queue for agent review                                     │
│  • Send automated personalised email                          │
│  • Add to drip sequence                                       │
│  • Schedule follow-up in 24 hours                             │
│                                                                 │
│  COLD: ───────────────────────                                  │
│  • Add to nurture sequence                                    │
│  • Monthly market update emails                               │
│  • Re-score monthly                                           │
│  • Flag if engagement increases                               │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  AGENT INTERFACE                                               │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐                   │
│  │ LEAD CARD       │    │ AI INSIGHTS     │                   │
│  │                 │    │                 │                   │
│  │ John & Sarah    │    │ • Buying in 3-6 │                   │
│  │ Chen            │    │   months        │                   │
│  │ Score: 87 HOT   │    │ • Finance       │                   │
│  │                 │    │   pre-approved  │                   │
│  │ [Call Now]      │    │ • Viewed 12     │                   │
│  │ [Schedule]      │    │   properties    │                   │
│  │ [Qualify]       │    │ • Price range:  │                   │
│  │                 │    │   $800-950K     │                   │
│  └─────────────────┘    └─────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Interaction Points

**1. Lead Ingestion**
- System receives lead via API/webhook
- Enrichment: Lookup ph
}