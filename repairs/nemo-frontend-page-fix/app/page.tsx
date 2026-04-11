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
          <div>
            <Badge className="mb-6 px-4 py-1.5 text-sm glass-card" variant="secondary">
              <Sparkles className="h-4 w-4 mr-2" />
              Powered by AI
            </Badge>
            
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6">
              <span className="text-gradient">Find Your Perfect</span>
              <br />
              <span className="text-foreground">Property with AI</span>
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
