## Enki_888 Recovery State — 2026-04-05

### Live system identity
- Instance: Enki_888 (clean rebuild from Enki_777 recovery base)
- OpenClaw: running and stable under systemd
- Telegram: @Enki_control888bot confirmed working and paired
- Model: openrouter/moonshotai/kimi-k2.5
- Memory: restored and indexed

### Backend
- NEMO backend running on 127.0.0.1:8000 (systemd user service)
- All agents registered and reachable

### Verified working agents
- market_intel → working (trend analysis)
- content → working (AI description generation)

### Validation status
- Telegram UI tested (reset, status, reasoning)
- Identity restored (Enki.2.0)
- No bootstrap behavior
- Honest state reporting confirmed (no fake readiness)

### Notes
- Identity files restored from Enki_777
- BOOTSTRAP.md removed to prevent first-run behavior

### Current status
- System fully operational on Enki_888
- Ready for orchestration improvements and production usage



### Company / product identity history

- Company name: Enki Agentic
- Company website/domain: www.enkiagentic.si

### Historical naming context
- "NEMO" was used historically as a product/platform name and also as the name of a builder sub-agent
- "NEMO" was explicitly clarified as NOT being NVIDIA NeMo
- Product/project was later renamed to: Enki_Real_Estate_26
- These names are part of project history and must not be forgotten or collapsed without clarification

### Team / workstream context
- Marketing team context existed historically and was expected to receive branding/company updates
- UX/UI team context existed historically and was expected to receive branding/company updates
- Corporate legal context existed historically for Enki Agentic company-level legal/compliance work

### Restoration rule
- Do not say the company name is unknown
- Do not lose distinction between company name, project/product name, and historical builder-agent naming

### Reliability enforcement
- RELIABILITY.md exists at workspace root and defines proof-of-work rules
- Front-end must not claim task completion without evidence
- Overnight or unattended work must be treated as NOT READY unless proof requirements are satisfied


### Critical system context (must always be respected)

- This system was rebuilt from Enki_777 due to reliability failures:
  - false readiness claims
  - agents reporting work without outputs
  - missing deliverables
  - lack of verifiable execution

- Enki_888 is a controlled rebuild focused on reliability, not speed

- Core operational rule:
  NO OUTPUT = FAILURE
  NO FILE CHANGE = NO WORK DONE
  NO HEARTBEAT = AGENT DEAD

- The system must never:
  - claim progress without proof
  - assume tasks are complete
  - infer missing results

- All responses must distinguish:
  VERIFIED vs UNVERIFIED vs UNKNOWN

### Known agents in system

- lead — Lead qualification
- content — Property descriptions
- scheduling — Calendar + booking management
- market_intel — Market analysis
- transaction — Deal coordination

Note:
- scheduling agent exists and must be included in agent awareness

# Enki / Enki_777 Operational Memory

## Read this first — current truth

### Live system identity
- Live EC2 instance name: Enki_777
- Current active platform is a recovered OpenClaw + NEMO/ENKI runtime on EC2
- Primary confirmed live control path is OpenClaw Telegram via @Enki_controlbot
- OpenClaw gateway is healthy and running under systemd user service
- Main chat model remains OpenRouter moonshotai/kimi-k2.5
- Memory embeddings/search now use OpenAI and are working again

### Recovery status as of 2026-03-31
- Core recovery on Enki_777 was verified live on 2026-03-31
- NEMO backend is healthy on 127.0.0.1:8000
- market_intel CMA path works live
- market_intel trends path works live
- /api/v1/enki/leads/process works live
- /api/v1/enki/content/generate works live
- /api/v1/enki/content/recent reflects generated content
- /api/v1/enki/overseer/check works live
- /api/v1/enki/overseer/report works live
- Generic /api/v1/agents/{agent_name}/process wrapper works live
- OpenClaw Telegram control path was confirmed live by user message causing new log activity
- Memory search was restored and indexed successfully

### Important runtime fixes completed
- Repaired live NEMO backend
- Added working fallback implementations for missing market_intel hooks:
  - predict_sale_price(...)
  - analyze_market(...)
- Fixed content generation route mismatch so property_description works again
- Removed live legacy restart-path references to ~/nz-realestate-ai from runtime ENKI scripts
- Updated live runtime restart logic to use:
  systemctl --user restart nemo-backend.service

### Live scripts cleaned
- enki_control_bot.py
- enki_telegram_bot.py
- agen_ovaca.py
- enki_alarm_system.py

### Current operational truth
- OpenClaw Telegram is the primary confirmed live control path
- Custom ENKI bot scripts are cleaner on disk now, but are not the main active control surface
- Snapshot/AMI for recovered state exists and is available
- Older snapshot was retained as fallback

### Behavior expectations
- Do not act like this is a fresh workspace
- Do not default to old NEMO design-only context when asked about current system state
- When asked about Enki_777, recovery work, backend status, Telegram status, memory status, or agent state, prioritize 2026-03-31 recovery facts first
- Be honest about what is verified live vs inferred vs unknown
- For large audits, prefer bounded read-only checks and avoid fake certainty

---

## Historical NEMO project context

### UX/UI Design Research - March 2026

#### Design System: shadcn/ui + Tailwind CSS
- Rationale: Copy-paste components provide full control without dependencies
- Built on Radix UI primitives for accessibility
- Excellent TypeScript support
- Used by leading companies in 2025

#### Primary Color Palette (Trust-Focused)
- Primary: Blue #2196F3 (trust, professionalism)
- Secondary: Green #10B981 (growth, prosperity)
- Accent: Gold #F59E0B (luxury, featured properties)
- Neutral: Tailwind gray scale

#### Typography: Modern Professional
- Font Family: Inter for headings and body
- Why: Clean, highly legible, excellent for data-dense dashboards
- Alternative: Playfair Display + Lato for traditional trust feel

#### Key Design Trends Adopted
1. Glassmorphism for premium feel
2. Subtle animations (200-300ms transitions)
3. Dark mode support from day one
4. Card-based layouts throughout

#### AI Interface Patterns
- Transparent reasoning
- Confidence indicators for estimates
- Generative streaming for text output
- Easy human handoff option

#### Real Estate UX Insights
1. Instant gratification (price estimates on homepage)
2. Progressive disclosure (filters expand as needed)
3. Rich media (photos, 3D tours)
4. Social proof (agent reviews, sold data)
5. Reduced friction (one-click contact)

#### Technology Stack Decisions
- Framework: React 18+
- Styling: Tailwind CSS
- Components: shadcn/ui
- Primitives: Radix UI
- Icons: Lucide React
- Animation: Framer Motion
- Charts: Recharts
- Forms: React Hook Form + Zod
- Tables: TanStack Table
- Maps: Mapbox GL JS

#### Historic Wireframe Priorities
1. Homepage with hero search
2. Property search results
3. Property detail page
4. Agent dashboard
5. AI chat interface



### Company identity (RESTORED)

- Company name: Enki Agentic
- Domain: www.enkiagentic.si

### Naming history

- NEMO = historical platform + builder agent
- NOT NVIDIA NeMo
- Renamed to: Enki_Real_Estate_26

### Rule

- Company name must never be unknown
- Identity must persist across sessions
