# NEMO Project Memory

## UX/UI Design Research - March 2026

### Key Decisions Made

#### Design System: shadcn/ui + Tailwind CSS
- **Rationale:** Copy-paste components provide full control without dependencies
- Built on Radix UI primitives for accessibility
- Excellent TypeScript support
- Used by leading companies in 2025

#### Primary Color Palette (Trust-Focused)
- **Primary:** Blue #2196F3 (trust, professionalism)
- **Secondary:** Green #10B981 (growth, prosperity)
- **Accent:** Gold #F59E0B (luxury, featured properties)
- **Neutral:** Tailwind gray scale

#### Typography: Modern Professional
- **Font Family:** Inter for headings and body
- **Why:** Clean, highly legible, excellent for data-dense dashboards
- **Alternative:** Playfair Display + Lato for traditional trust feel

#### Key Design Trends Adopted
1. **Glassmorphism** for premium feel (cards, modals)
2. **Subtle animations** (200-300ms transitions)
3. **Dark mode** support from day one
4. **Card-based layouts** throughout

#### AI Interface Patterns
- Transparent reasoning (show how AI arrived at conclusions)
- Confidence indicators for estimates
- Generative streaming for text output
- Easy human handoff option

### Real Estate UX Insights

#### Conversion Factors (from Zillow, Redfin analysis)
1. Instant gratification (price estimates on homepage)
2. Progressive disclosure (filters expand as needed)
3. Rich media (photos, 3D tours)
4. Social proof (agent reviews, sold data)
5. Reduced friction (one-click contact)

#### TradeMe Strengths to Emulate
- Map-first search experience
- Property Insights integration
- Clean, mobile-first design

#### Critical Features
- Visual-first design (high-quality images)
- Data transparency (price history, comparables)
- Mobile-optimized (70%+ traffic is mobile)
- Trust signals (verified listings, agent credentials)

### Technology Stack Decisions

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Framework | React 18+ | Industry standard, ecosystem |
| Styling | Tailwind CSS | Utility-first, rapid iteration |
| Components | shadcn/ui | Copy-paste, customizable |
| Primitives | Radix UI | ARIA-compliant |
| Icons | Lucide React | Clean, consistent |
| Animation | Framer Motion | Declarative, performant |
| Charts | Recharts | React-native |
| Forms | React Hook Form + Zod | Performance, validation |
| Tables | TanStack Table | Feature-rich |
| Maps | Mapbox GL JS | Performance |

### Wireframe Priorities
1. Homepage with hero search
2. Property search results (list/map toggle)
3. Property detail page (with AI valuation)
4. Agent dashboard (KPIs + pipeline)
5. AI chat interface

### Next Steps
- [ ] Initialize shadcn/ui project
- [ ] Set up color tokens in Tailwind config
- [ ] Build PropertyCard component
- [ ] Create search interface
- [ ] Implement AI chat interface

---

*Last updated: March 2026*
