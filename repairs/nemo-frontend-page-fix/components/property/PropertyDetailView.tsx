"use client";

import { motion } from "framer-motion";
import {
  Bed,
  Bath,
  Square,
  MapPin,
  Calendar,
  Home,
  Car,
  Thermometer,
  TreePine,
  Share2,
  Heart,
  Printer,
  Phone,
  Mail,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";

interface PropertyDetail {
  id: string;
  title: string;
  address: string;
  price: number;
  bedrooms: number;
  bathrooms: number;
  sqft: number;
  lotSize?: string;
  yearBuilt?: number;
  propertyType: string;
  description: string;
  images: string[];
  features: string[];
  agent: {
    name: string;
    phone: string;
    email: string;
    image: string;
    company: string;
  };
  aiInsights?: {
    estimate: number;
    confidence: number;
    trend: "up" | "down" | "stable";
    trendValue: string;
  };
}

interface PropertyDetailViewProps {
  property: PropertyDetail;
  className?: string;
}

export function PropertyDetailView({
  property,
  className,
}: PropertyDetailViewProps) {
  const formatPrice = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <div className={cn("space-y-6", className)}>
      {/* Hero Section with Image Gallery */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative rounded-2xl overflow-hidden"
      >
        <div className="aspect-[21/9] relative">
          <img
            src={property.images[0]}
            alt={property.title}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
        </div>

        {/* Overlay Content */}
        <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
          <div className="flex items-start justify-between">
            <div>
              <Badge className="mb-3 bg-primary text-white">For Sale</Badge>
              <h1 className="text-3xl md:text-4xl font-bold mb-2">
                {formatPrice(property.price)}
              </h1>
              <p className="text-xl text-white/90">{property.title}</p>
              <div className="flex items-center gap-2 mt-2 text-white/80">
                <MapPin className="h-4 w-4" />
                <span>{property.address}</span>
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                variant="ghost"
                size="icon"
                className="rounded-full bg-white/20 backdrop-blur-sm hover:bg-white/30 text-white"
              >
                <Share2 className="h-5 w-5" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="rounded-full bg-white/20 backdrop-blur-sm hover:bg-white/30 text-white"
              >
                <Heart className="h-5 w-5" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="rounded-full bg-white/20 backdrop-blur-sm hover:bg-white/30 text-white"
              >
                <Printer className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Property Details */}
        <div className="lg:col-span-2 space-y-6">
          {/* Key Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card className="glass-card border-0">
              <CardContent className="p-6">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                  <div className="text-center">
                    <Bed className="h-6 w-6 mx-auto mb-2 text-primary" />
                    <p className="text-2xl font-bold">{property.bedrooms}</p>
                    <p className="text-sm text-muted-foreground">Bedrooms</p>
                  </div>
                  <div className="text-center">
                    <Bath className="h-6 w-6 mx-auto mb-2 text-primary" />
                    <p className="text-2xl font-bold">{property.bathrooms}</p>
                    <p className="text-sm text-muted-foreground">Bathrooms</p>
                  </div>
                  <div className="text-center">
                    <Square className="h-6 w-6 mx-auto mb-2 text-primary" />
                    <p className="text-2xl font-bold">
                      {property.sqft.toLocaleString()}
                    </p>
                    <p className="text-sm text-muted-foreground">Sq Ft</p>
                  </div>
                  <div className="text-center">
                    <Home className="h-6 w-6 mx-auto mb-2 text-primary" />
                    <p className="text-2xl font-bold">{property.propertyType}</p>
                    <p className="text-sm text-muted-foreground">Type</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Tabs Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Tabs defaultValue="overview" className="w-full">
              <TabsList className="glass-card w-full justify-start">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="features">Features</TabsTrigger>
                <TabsTrigger value="history">Price History</TabsTrigger>
                <TabsTrigger value="ai-insights">AI Insights</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="mt-6">
                <Card className="glass-card border-0">
                  <CardHeader>
                    <CardTitle>Description</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground leading-relaxed">
                      {property.description}
                    </p>
                    <Separator className="my-6" />
                    <div className="grid grid-cols-2 gap-4">
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        <span className="text-sm">
                          Year Built: {property.yearBuilt || "N/A"}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <TreePine className="h-4 w-4 text-muted-foreground" />
                        <span className="text-sm">
                          Lot Size: {property.lotSize || "N/A"}
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="features" className="mt-6">
                <Card className="glass-card border-0">
                  <CardHeader>
                    <CardTitle>Property Features</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                      {property.features.map((feature, index) => (
                        <div
                          key={index}
                          className="flex items-center gap-2 p-3 rounded-lg bg-muted"
                        >
                          <div className="h-2 w-2 rounded-full bg-secondary" />
                          <span className="text-sm">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="ai-insights" className="mt-6">
                {property.aiInsights && (
                  <Card className="glass-card border-0 border-l-4 border-l-primary">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        AI Valuation Insights
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="flex items-center justify-between">
                        <span className="text-muted-foreground">
                          AI Estimate
                        </span>
                        <span className="text-2xl font-bold">
                          {formatPrice(property.aiInsights.estimate)}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-muted-foreground">
                          Confidence Score
                        </span>
                        <Badge variant="secondary">
                          {property.aiInsights.confidence}%
                        </Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-muted-foreground">
                          Market Trend
                        </span>
                        <div className="flex items-center gap-1">
                          {property.aiInsights.trend === "up" ? (
                            <span className="text-secondary">
                              ↗ {property.aiInsights.trendValue}
                            </span>
                          ) : property.aiInsights.trend === "down" ? (
                            <span className="text-destructive">
                              ↘ {property.aiInsights.trendValue}
                            </span>
                          ) : (
                            <span className="text-muted-foreground">
                              → {property.aiInsights.trendValue}
                            </span>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>
            </Tabs>
          </motion.div>
        </div>

        {/* Right Column - Agent & Actions */}
        <div className="space-y-6">
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card className="glass-card border-0 sticky top-6">
              <CardHeader>
                <CardTitle className="text-lg">Contact Agent</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="h-14 w-14 rounded-full overflow-hidden bg-muted">
                    <img
                      src={property.agent.image}
                      alt={property.agent.name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div>
                    <p className="font-semibold">{property.agent.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {property.agent.company}
                    </p>
                  </div>
                </div>
                <Separator />
                <Button className="w-full" size="lg">
                  <Phone className="h-4 w-4 mr-2" />
                  Call Agent
                </Button>
                <Button variant="outline" className="w-full" size="lg">
                  <Mail className="h-4 w-4 mr-2" />
                  Send Message
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

export default PropertyDetailView;
