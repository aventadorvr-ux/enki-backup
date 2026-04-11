# NEMO Frontend Architecture

**Phase:** 2 - Frontend Architecture Design  
**Status:** ✅ Complete  
**Date:** March 2026

---

## Overview

The NEMO frontend is a modern React application built with Next.js, TypeScript, and Tailwind CSS. It implements a glassmorphism design system with shadcn/ui components and supports both light and dark modes.

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Framework | Next.js 14+ (App Router) | Server-side rendering, routing |
| Language | TypeScript | Type safety |
| Styling | Tailwind CSS | Utility-first CSS |
| Components | shadcn/ui | Base UI components |
| Animation | Framer Motion | Declarative animations |
| Icons | Lucide React | Consistent iconography |

---

## Project Structure

```
projects/nemo-frontend/
├── app/                          # Next.js App Router
│   ├── globals.css              # Global styles, CSS variables
│   ├── layout.tsx               # Root layout with ThemeProvider
│   ├── page.tsx                 # Home page (hero search)
│   ├── search/
│   │   └── page.tsx             # Property search with map
│   ├── property/
│   │   └── [id]/
│   │       └── page.tsx         # Property detail view
│   └── dashboard/
│       └── page.tsx             # Agent dashboard
│
├── components/
│   ├── ui/                      # shadcn/ui base components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── badge.tsx
│   │   └── ...
│   │
│   ├── property/                # Property-specific components
│   │   ├── PropertyCard.tsx     # Listing card with glassmorphism
│   │   └── PropertyDetailView.tsx # Full property detail
│   │
│   ├── dashboard/               # Dashboard components
│   │   ├── KPICards.tsx         # Stats cards with trends
│   │   └── ActivityFeed.tsx     # Recent activity list
│   │
│   ├── ai/                      # AI interface components
│   │   └── AIChatInterface.tsx  # Chat UI with suggestions
│   │
│   └── map/                     # Map components
│       └── MapSearch.tsx        # Map/list split view
│
├── lib/
│   └── utils.ts                 # Utility functions (cn, etc.)
│
├── types/                       # TypeScript definitions
├── public/                      # Static assets
├── tailwind.config.ts           # Tailwind configuration
└── next.config.js               # Next.js configuration
```

---

## Design System

### Color Palette

**Primary Colors:**
- Primary Blue: `#2196F3` (Trust, professionalism)
- Secondary Green: `#10B981` (Growth, prosperity)
- Accent Gold: `#F59E0B` (Luxury, featured properties)

**Dark Mode:**
- Base: `#0F172A` (Not pure black)
- Elevated: `#1E293B`
- Border: `#334155`

### Typography

- **Font Family:** Inter (system-ui fallback)
- **Base Size:** 16px
- **Scale:** xs (12px) → 6xl (60px)

### Spacing

- **Grid System:** 24px base (1.5rem)
- **Card Padding:** 24px
- **Section Spacing:** 48-96px

### Glassmorphism

Implemented via Tailwind utilities:
```css
.glass {
  @apply bg-white/70 dark:bg-dark-elevated/70 backdrop-blur-glass;
}

.glass-card {
  @apply glass border border-white/20 dark:border-white/10 shadow-lg;
}
```

---

## Components

### PropertyCard
- **Purpose:** Display property listings
- **Features:**
  - Image with hover zoom
  - Price overlay with AI estimate
  - Favorite button
  - Key stats (beds, baths, sqft)
  - Glassmorphism styling

### PropertyDetailView
- **Purpose:** Full property page
- **Features:**
  - Hero image gallery
  - Key stats grid
  - Tabbed content (Overview, Features, History, AI)
  - Agent contact card
  - AI insights panel

### MapSearch
- **Purpose:** Map-first search experience
- **Features:**
  - Map/List/Split view modes
  - Property pins on map
  - List/grid toggle
  - Responsive layout

### AIChatInterface
- **Purpose:** AI assistant chat
- **Features:**
  - Message bubbles (user/assistant)
  - Confidence indicators
  - Suggested prompts
  - Loading states
  - Auto-scroll

### KPICards
- **Purpose:** Dashboard statistics
- **Features:**
  - Trend indicators (up/down/neutral)
  - Icon integration
  - Glassmorphism styling

### ActivityFeed
- **Purpose:** Recent activity stream
- **Features:**
  - Activity type icons
  - Timestamps (relative)
  - User avatars
  - Animated list

---

## Pages

### Home (`/`)
- Hero section with search
- Value proposition cards
- Stats counters
- Glassmorphism hero background

### Search (`/search`)
- Map/List split view
- Property filtering
- Results grid

### Property Detail (`/property/[id]`)
- Full property information
- Image gallery
- AI insights
- Agent contact

### Dashboard (`/dashboard`)
- KPI cards row
- Activity feed
- AI assistant sidebar
- Performance charts (placeholder)

---

## Key Design Decisions

### 1. shadcn/ui Copy-Paste Approach
**Why:** Full control, no dependency bloat, easy customization

### 2. Glassmorphism Aesthetic
**Why:** Modern, premium feel aligned with 2025/2026 trends

### 3. Dark Mode First
**Why:** Better for data-dense dashboards, professional appearance

### 4. Framer Motion for Animations
**Why:** Declarative, performant, excellent React integration

### 5. Mapbox Integration Placeholder
**Why:** Real map integration requires API keys; structure ready for Mapbox GL JS

---

## Build Commands

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

---

## Integration Points

### Backend API
- Base URL: `http://3.25.170.226:8000`
- Endpoints:
  - `GET /health` - Health check
  - `GET /api/v1/agents` - List agents
  - `POST /api/v1/agents/{name}/process` - Process tasks

### AI Chat
- Currently mock responses
- Replace `generateMockResponse()` with actual API call
- Endpoint: TBD

### Maps
- Placeholder for Mapbox GL JS
- Requires: Mapbox API token
- Component ready in `MapSearch.tsx`

---

## Next Steps (Phase 3)

1. **Connect to Backend**
   - Replace mock data with API calls
   - Implement authentication
   - Set up CORS

2. **Map Integration**
   - Add Mapbox GL JS
   - Implement property clustering
   - Add drawing tools for area search

3. **AI Integration**
   - Connect to AI agent endpoints
   - Implement streaming responses
   - Add context persistence

4. **Testing**
   - Unit tests for components
   - E2E tests for critical paths
   - Accessibility audit

5. **Performance**
   - Image optimization
   - Code splitting
   - Lazy loading for map

---

*Architecture documentation for NEMO Frontend Phase 2*
