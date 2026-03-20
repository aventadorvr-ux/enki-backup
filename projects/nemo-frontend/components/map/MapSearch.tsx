"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { MapPin, List, Map as MapIcon, Layers } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";
import { PropertyCard } from "../property/PropertyCard";

interface Property {
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
  coordinates: {
    lat: number;
    lng: number;
  };
}

interface MapSearchProps {
  properties: Property[];
  className?: string;
  onPropertySelect?: (property: Property) => void;
  onFavoriteToggle?: (id: string) => void;
  favoriteIds?: string[];
}

export function MapSearch({
  properties,
  className,
  onPropertySelect,
  onFavoriteToggle,
  favoriteIds = [],
}: MapSearchProps) {
  const [viewMode, setViewMode] = useState<"map" | "list" | "split">("split");
  const [selectedPropertyId, setSelectedPropertyId] = useState<string | null>(null);

  const handlePropertyClick = (property: Property) => {
    setSelectedPropertyId(property.id);
    onPropertySelect?.(property);
  };

  return (
    <div className={cn("flex flex-col h-full", className)}>
      {/* Toolbar */}
      <div className="flex items-center justify-between p-4 border-b border-border/50">
        <div className="flex items-center gap-4">
          <h2 className="text-lg font-semibold">
            {properties.length} Properties Found
          </h2>
          <Badge variant="secondary" className="glass-card">
            Auckland, NZ
          </Badge>
        </div>

        <Tabs value={viewMode} onValueChange={(v) => setViewMode(v as typeof viewMode)}>
          <TabsList className="glass-card">
            <TabsTrigger value="map" className="flex items-center gap-2">
              <MapIcon className="h-4 w-4" />
              <span className="hidden sm:inline">Map</span>
            </TabsTrigger>
            <TabsTrigger value="split" className="flex items-center gap-2">
              <Layers className="h-4 w-4" />
              <span className="hidden sm:inline">Split</span>
            </TabsTrigger>
            <TabsTrigger value="list" className="flex items-center gap-2">
              <List className="h-4 w-4" />
              <span className="hidden sm:inline">List</span>
            </TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        <div
          className={cn(
            "grid h-full",
            viewMode === "map" && "grid-cols-1",
            viewMode === "list" && "grid-cols-1",
            viewMode === "split" && "grid-cols-1 lg:grid-cols-2"
          )}
        >
          {/* Map Section */}
          {(viewMode === "map" || viewMode === "split") && (
            <div className={cn("relative bg-muted", viewMode === "split" && "hidden lg:block")}>
              {/* Placeholder for actual map integration */}
              <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-muted to-muted/50">
                <div className="text-center">
                  <MapIcon className="h-16 w-16 mx-auto mb-4 text-muted-foreground/50" />
                  <p className="text-muted-foreground">Map Integration</p>
                  <p className="text-sm text-muted-foreground/70 mt-1">
                    Connect Mapbox GL JS here
                  </p>
                </div>
              </div>

              {/* Map Controls */}
              <div className="absolute bottom-4 right-4 flex flex-col gap-2">
                <Button variant="secondary" size="icon" className="glass-card shadow-lg">
                  <Layers className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          {/* List Section */}
          {(viewMode === "list" || viewMode === "split") && (
            <div className="overflow-y-auto p-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {properties.map((property, index) => (
                  <motion.div
                    key={property.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    onClick={() => handlePropertyClick(property)}
                    className={cn(
                      "cursor-pointer",
                      selectedPropertyId === property.id && "ring-2 ring-primary rounded-xl"
                    )}
                  >
                    <PropertyCard
                      {...property}
                      isFavorite={favoriteIds.includes(property.id)}
                      onFavorite={onFavoriteToggle}
                    />
                  </motion.div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default MapSearch;
