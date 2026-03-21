# NZ REAL ESTATE AI - 7 DAY SPRINT PLAN
## Frontend-First Prototype Delivery
**Start:** March 21, 2026 | **Delivery:** March 28, 2026

---

## FRONTEND REQUIREMENTS (Priority #1)

### Dashboard Components
| Feature | Description | Status |
|---------|-------------|--------|
| **Hero Section** | Real-time stats, active leads, system health | 🔄 DESIGN |
| **Agent Control Panel** | Start/stop agents, view logs, manual trigger | 🔄 DESIGN |
| **Lead Pipeline** | Visual kanban board (New → Qualified → Hot → Closed) | 🔄 DESIGN |
| **Content Generator** | Property description input, output preview, copy button | 🔄 DESIGN |
| **Market Intel View** | CMA charts, competitor tracking, trend graphs | 🔄 DESIGN |
| **Dark Mode** | Professional dark UI (easier on eyes for demos) | 🔄 DESIGN |

### Design System
- **Framework:** Next.js 14 + Tailwind CSS
- **Components:** shadcn/ui (Radix primitives)
- **Colors:** Blue primary (#2196F3), Green success, Gold accent
- **Typography:** Inter (clean, professional)
- **Animations:** Subtle 200ms transitions, loading states

---

## 7-DAY BREAKDOWN

### DAY 1 (Today) - Foundation
**Morning (4 hrs):**
- [ ] Fix Windows OpenClaw stability (systematic, not rushed)
- [ ] Create systemd services for all 5 agents on NEMO
- [ ] Test agent auto-restart

**Afternoon (4 hrs):**
- [ ] Initialize Next.js project in workspace
- [ ] Install shadcn/ui, configure Tailwind
- [ ] Set up color tokens, typography
- [ ] Create basic layout shell

**Deliverable:** Backend stable, frontend repo initialized

---

### DAY 2 - Core Components
**Full Day (8 hrs):**
- [ ] Build Agent Control Panel component
- [ ] Create system status widget (real-time API polling)
- [ ] Design navigation sidebar
- [ ] Implement dark mode toggle
- [ ] Connect to NEMO API (health check endpoint)

**Deliverable:** Dashboard shell + agent controls working

---

### DAY 3 - Lead Pipeline
**Full Day (8 hrs):**
- [ ] Build Lead Pipeline kanban board
- [ ] Create lead cards (budget, timeline, score badges)
- [ ] Implement drag-and-drop (optional: click-to-move)
- [ ] Connect to Lead Agent API
- [ ] Add lead detail modal

**Deliverable:** Working lead pipeline with real data

---

### DAY 4 - Content & Market
**Full Day (8 hrs):**
- [ ] Build Content Generator interface
- [ ] Property description form (beds, baths, location)
- [ ] AI output display with copy button
- [ ] Market Intel dashboard (charts placeholder)
- [ ] CMA generator interface

**Deliverable:** Content & Market modules functional

---

### DAY 5 - Polish & Animations
**Full Day (8 hrs):**
- [ ] Add loading skeletons
- [ ] Implement toast notifications
- [ ] Error states and empty states
- [ ] Responsive mobile layout
- [ ] Page transitions and micro-interactions

**Deliverable:** Polished, professional UI

---

### DAY 6 - Integration & Testing
**Full Day (8 hrs):**
- [ ] End-to-end workflow testing
- [ ] API error handling
- [ ] Performance optimization
- [ ] Browser testing (Chrome, Edge)
- [ ] Create demo data set

**Deliverable:** Stable, tested application

---

### DAY 7 - Demo Prep
**Full Day (8 hrs):**
- [ ] Record demo video (screen capture)
- [ ] Create presentation deck
- [ ] Document features
- [ ] Deploy to Vercel/Netlify (optional)
- [ ] Final bug fixes

**Deliverable:** Presentable prototype + documentation

---

## FRONTEND TECH STACK

```json
{
  "framework": "Next.js 14 (App Router)",
  "styling": "Tailwind CSS",
  "components": "shadcn/ui",
  "charts": "Recharts",
  "state": "React Query + Zustand",
  "forms": "React Hook Form + Zod",
  "animations": "Framer Motion",
  "icons": "Lucide React"
}
```

---

## DAILY REPORT SCHEDULE

**Every day at 20:00 UTC, I'll send:**
1. What was completed
2. What's in progress
3. Blockers (if any)
4. Screenshots of UI progress
5. Next day's plan

---

## SUCCESS CRITERIA

✅ Dashboard loads in < 2 seconds  
✅ All 5 agents controllable from UI  
✅ Lead pipeline shows real data  
✅ Content generator produces output  
✅ Dark mode works throughout  
✅ Mobile responsive  
✅ Demo video recorded  

---

## RISK MITIGATION

| Risk | Mitigation |
|------|------------|
| Windows unstable | Focus on NEMO backend, use Windows only for Telegram |
| API delays | Build with mock data first, swap to real API |
| Time overrun | Cut scope: Market Intel charts can be placeholder |
| shadcn/ui learning curve | Use pre-built components, minimal customization |

---

**STATUS: READY TO START**

**First action:** Initialize frontend project while fixing backend services in parallel.

**Waiting for GO signal.**