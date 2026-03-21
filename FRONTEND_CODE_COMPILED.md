# NEMO FRONTEND CODE - FULL DOCUMENTATION
## Generated: 2026-03-22

---

## page.tsx - Main Landing Page

```typescript
import { Metadata } from "next";
import { Search, TrendingUp, Shield, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import Link from "next/link";

export const metadata: Metadata = {
  title: "NEMO - AI-Powered Real Estate Platform",
  description: "Find, analyze, and close deals faster with AI-powered real estate tools for agents and investors.",
};

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative min-h-[80vh] flex items-center justify-center overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-background to-secondary-50 dark:from-primary-900/20 dark:via-background dark:to-secondary-900/20" />
        <div className="absolute inset-0 glass-hero" />
        
        {/* Content */}
        <div className="relative z-10 container mx-auto px-4 text-center">
          <Badge className="mb-6 px-4 py-1.5 text-sm glass-card" variant="secondary">
            <Sparkles className="h-4 w-4 mr-2" />
            Powered by AI
          </Badge>
          
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6">
            Find Your Perfect Property with AI
          </h1>
          
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
            NEMO combines advanced AI with real-time market data to help agents 
            and investors make smarter decisions faster.
          </p>

          {/* Search Bar */}
          <Card className="max-w-3xl mx-auto glass-card border-0 shadow-2xl">
            <CardContent className="p-4 md:p-6">
              <div className="flex flex-col md:flex-row gap-3">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                  <Input
                    placeholder="Enter location, suburb, or address..."
                    className="pl-10 h-12 text-lg glass-card border-0"
                  />
                </div>
                <div className="flex gap-2">
                  <Button size="lg" className="h-12 px-8" asChild>
                    <Link href="/search">Search</Link>
                  </Button>
                  <Button size="lg" variant="outline" className="h-12 px-6 glass-card">
                    AI Valuation
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <div className="flex flex-wrap justify-center gap-8 mt-12">
            <div className="text-center">
              <p className="text-3xl font-bold text-gradient">10K+</p>
              <p className="text-sm text-muted-foreground">Properties Listed</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-gradient">500+</p>
              <p className="text-sm text-muted-foreground">Active Agents</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-gradient">98%</p>
              <p className="text-sm text-muted-foreground">AI Accuracy</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Why Choose NEMO?
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Built specifically for the New Zealand real estate market with 
              powerful AI tools to accelerate your success.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="glass-card border-0">
              <CardContent className="p-8">
                <div className="h-12 w-12 rounded-xl bg-primary/10 flex items-center justify-center mb-6">
                  <Sparkles className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-3">AI-Powered Insights</h3>
                <p className="text-muted-foreground">
                  Get instant property valuations, market trends, and investment 
                  recommendations powered by advanced machine learning.
                </p>
              </CardContent>
            </Card>

            <Card className="glass-card border-0">
              <CardContent className="p-8">
                <div className="h-12 w-12 rounded-xl bg-secondary/10 flex items-center justify-center mb-6">
                  <TrendingUp className="h-6 w-6 text-secondary" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Market Intelligence</h3>
                <p className="text-muted-foreground">
                  Real-time data from TradeMe and NZ property databases to keep 
                  you ahead of market movements.
                </p>
              </CardContent>
            </Card>

            <Card className="glass-card border-0">
              <CardContent className="p-8">
                <div className="h-12 w-12 rounded-xl bg-accent/10 flex items-center justify-center mb-6">
                  <Shield className="h-6 w-6 text-accent" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Agent Tools</h3>
                <p className="text-muted-foreground">
                  Automated listing descriptions, lead qualification, and 
                  transaction coordination to close deals faster.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </div>
  );
}
```

---

## PropertyCard.tsx - Property Display Component

```typescript
"use client";

import { motion } from "framer-motion";
import { Heart, Bed, Bath, Square, MapPin } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface PropertyCardProps {
  id: string;
  title: string;
  address: string;
  price: number;
  bedrooms: number;
  bathrooms: number;
  sqft: number;
  imageUrl: string;
  type: "sale" | "rent";
  featured?: boolean;
  aiEstimate?: number;
  className?: string;
  onFavorite?: (id: string) => void;
  isFavorite?: boolean;
}

export function PropertyCard({...props}: PropertyCardProps) {
  const formatPrice = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={{ y: -4 }}
      className={cn("group", props.className)}
    >
      <Card className="overflow-hidden glass-card property-card-hover border-0">
        {/* Image Container */}
        <div className="relative aspect-[4/3] overflow-hidden">
          <img src={props.imageUrl} alt={props.title} />
          
          {/* Badges */}
          <div className="absolute top-3 left-3 flex gap-2">
            <Badge variant={props.type === "sale" ? "default" : "secondary"}>
              For {props.type}
            </Badge>
            {props.featured && <Badge variant="accent">Featured</Badge>}
          </div>

          {/* Price Overlay */}
          <div className="absolute bottom-3 left-3 right-3">
            <span className="text-2xl font-bold text-white">
              {formatPrice(props.price)}
            </span>
            {props.aiEstimate && (
              <Badge variant="glass" className="text-xs">
                AI Estimate: {formatPrice(props.aiEstimate)}
              </Badge>
            )}
          </div>
        </div>

        {/* Content */}
        <CardContent className="p-4">
          <h3 className="font-semibold text-lg">{props.title}</h3>
          <div className="flex items-center gap-1 text-muted-foreground text-sm mb-3">
            <MapPin className="h-3.5 w-3.5" />
            <span>{props.address}</span>
          </div>

          {/* Property Features */}
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <Bed className="h-4 w-4" />
              <span>{props.bedrooms}</span>
            </div>
            <div className="flex items-center gap-1">
              <Bath className="h-4 w-4" />
              <span>{props.bathrooms}</span>
            </div>
            <div className="flex items-center gap-1">
              <Square className="h-4 w-4" />
              <span>{props.sqft.toLocaleString()} sqft</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
```

---

## FRONTEND ARCHITECTURE

### Technology Stack:
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Components:** shadcn/ui (Radix UI primitives)
- **Animations:** Framer Motion
- **Icons:** Lucide React

### Key Components:
1. **Hero Section** - Search-first landing with AI valuation CTA
2. **PropertyCard** - Glassmorphism cards with AI estimates
3. **Dashboard** - Agent KPIs and activity feed
4. **Search Interface** - Map-first property discovery
5. **AI Chat Interface** - Property consultation

### Design System:
- **Primary:** Blue #2196F3 (trust)
- **Secondary:** Green #10B981 (growth)
- **Accent:** Gold #F59E0B (luxury)
- **Style:** Glassmorphism cards, subtle animations (200-300ms)
- **Dark Mode:** Fully supported from day one

---

## END OF FRONTEND DOCUMENTATION
