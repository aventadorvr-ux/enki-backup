# Enki Real Estate Design System

**Project:** Enki_Real_Estate_26 (NEMO Platform)  
**Version:** 1.0.0  
**Last Updated:** March 22, 2026

---

## Brand Identity

### Company
- **Name:** Enki Agentic
- **Domain:** www.enkiagentic.si
- **Tagline:** AI-Powered Solutions for Real Estate
- **Industry:** Real Estate Technology / AI Agents

### Brand Personality
- **Trustworthy:** Professional, reliable, secure
- **Innovative:** AI-forward, cutting-edge technology
- **Approachable:** Clean, modern, human-centered
- **Premium:** Quality-focused, luxury-ready

---

## Color System

### Primary Palette (Trust Blue)

| Token | Hex | HSL | Usage |
|-------|-----|-----|-------|
| `primary-50` | #E3F2FD | 205 100% 95% | Lightest backgrounds |
| `primary-100` | #BBDEFB | 205 100% 88% | Hover states, subtle fills |
| `primary-200` | #90CAF9 | 205 91% 77% | Borders, dividers |
| `primary-300` | #64B5F6 | 205 90% 67% | Secondary accents |
| `primary-400` | #42A5F5 | 205 90% 61% | Highlights |
| `primary-500` | #2196F3 | 207 90% 55% | **Primary brand color** |
| `primary-600` | #1E88E5 | 207 83% 51% | Primary hover |
| `primary-700` | #1976D2 | 207 79% 46% | Primary active |
| `primary-800` | #1565C0 | 207 80% 42% | Strong emphasis |
| `primary-900` | #0D47A1 | 207 85% 33% | Text on light |

### Secondary Palette (Growth Green)

| Token | Hex | HSL | Usage |
|-------|-----|-----|-------|
| `secondary-50` | #ECFDF5 | 152 82% 96% | Success backgrounds |
| `secondary-100` | #D1FAE5 | 152 81% 90% | Light success states |
| `secondary-200` | #A7F3D0 | 152 79% 80% | Progress indicators |
| `secondary-300` | #6EE7B7 | 152 76% 70% | Charts, graphs |
| `secondary-400` | #34D399 | 152 69% 64% | Positive trends |
| `secondary-500` | #10B981 | 160 84% 39% | **Secondary brand color** |
| `secondary-600` | #059669 | 161 94% 30% | Success actions |
| `secondary-700` | #047857 | 161 94% 24% | Dark success |
| `secondary-800` | #065F46 | 162 88% 20% | Text on light |
| `secondary-900` | #064E3B | 163 88% 14% | Deep emphasis |

### Accent Palette (Luxury Gold)

| Token | Hex | HSL | Usage |
|-------|-----|-----|-------|
| `accent-50` | #FFFBEB | 48 100% 96% | Featured backgrounds |
| `accent-100` | #FEF3C7 | 48 96% 89% | Premium highlights |
| `accent-200` | #FDE68A | 48 97% 77% | Warnings, featured |
| `accent-300` | #FCD34D | 46 97% 65% | Premium indicators |
| `accent-400` | #FBBF24 | 45 93% 57% | Star ratings |
| `accent-500` | #F59E0B | 38 92% 50% | **Accent brand color** |
| `accent-600` | #D97706 | 36 91% 37% | Gold hover |
| `accent-700` | #B45309 | 27 96% 30% | Dark gold |
| `accent-800` | #92400E | 24 95% 25% | Text gold |
| `accent-900` | #78350F | 22 92% 21% | Deep gold |

### Semantic Colors

| Purpose | Light Mode | Dark Mode |
|---------|------------|-----------|
| Background | #F9FAFB | #0F172A |
| Elevated | white | #1E293B |
| Card | white | #1E293B |
| Border | #E5E7EB | #334155 |
| Text Primary | #111827 | white |
| Text Secondary | #6B7280 | #9CA3AF |

---

## Typography System

### Font Family
- **Primary:** Inter (Google Fonts)
- **Fallback:** system-ui, sans-serif

### Type Scale

| Token | Size | Line Height | Weight | Usage |
|-------|------|-------------|--------|-------|
| `text-6xl` | 60px | 1 | 700 | Hero headlines |
| `text-5xl` | 48px | 1 | 700 | Large headlines |
| `text-4xl` | 36px | 1.1 | 700 | Page titles |
| `text-3xl` | 30px | 1.2 | 600 | Section headers |
| `text-2xl` | 24px | 1.3 | 600 | Card titles |
| `text-xl` | 20px | 1.4 | 600 | Subsection headers |
| `text-lg` | 18px | 1.5 | 500 | Lead paragraphs |
| `text-base` | 16px | 1.5 | 400 | Body text |
| `text-sm` | 14px | 1.5 | 400 | Secondary text |
| `text-xs` | 12px | 1.4 | 400 | Captions, labels |

---

## Spacing System

Base Unit: 4px (0.25rem)

| Token | Value | Pixels | Usage |
|-------|-------|--------|-------|
| `space-1` | 0.25rem | 4px | Tight spacing |
| `space-2` | 0.5rem | 8px | Icon gaps |
| `space-3` | 0.75rem | 12px | Small gaps |
| `space-4` | 1rem | 16px | Standard gaps |
| `space-6` | 1.5rem | 24px | **Base unit** |
| `space-8` | 2rem | 32px | Section gaps |
| `space-12` | 3rem | 48px | Large sections |

---

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `rounded-lg` | 8px | Buttons, cards |
| `rounded-xl` | 12px | Large cards |
| `rounded-2xl` | 16px | Modals, panels |
| `rounded-3xl` | 24px | Hero sections |
| `rounded-full` | 9999px | Pills, avatars |

**Default:** `--radius: 0.75rem` (12px)

---

## Component Specs

### Primary Button
```
Background: primary-500 (#2196F3)
Hover: primary-600 (#1E88E5)
Text: white
Padding: 12px 24px
Border Radius: 8px
Font Weight: 500
Transition: all 200ms ease-out
```

### Property Card
```
Background: white / dark: slate-800
Border Radius: 16px
Padding: 0 (image bleeds)
Shadow: shadow on hover
Hover: -translate-y-1 + shadow-xl
Transition: all 300ms ease-out
```

### Text Input
```
Background: white / dark: slate-800
Border: 1px solid gray-200
Border Radius: 8px
Padding: 12px 16px
Focus: ring-2 ring-primary-500
```

---

## Responsive Breakpoints

| Breakpoint | Width | Usage |
|------------|-------|-------|
| `sm` | 640px | Large phones |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small laptops |
| `xl` | 1280px | Desktops |

---

## Icons (Lucide React)

| Usage | Icon Name |
|-------|-----------|
| Search | `Search` |
| Location | `MapPin` |
| Bed | `Bed` |
| Bath | `Bath` |
| Area | `Maximize` |
| Heart | `Heart` |
| Filter | `SlidersHorizontal` |
| Share | `Share2` |
| Calendar | `Calendar` |
| Phone | `Phone` |
| Mail | `Mail` |

---

*Design System v1.0 - Enki Agentic*
