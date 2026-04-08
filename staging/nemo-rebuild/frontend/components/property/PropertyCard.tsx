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

export function PropertyCard({
  id,
  title,
  address,
  price,
  bedrooms,
  bathrooms,
  sqft,
  imageUrl,
  type,
  featured = false,
  aiEstimate,
  className,
  onFavorite,
  isFavorite = false,
}: PropertyCardProps) {
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
      className={cn("group", className)}
    >
      <Card className="overflow-hidden glass-card property-card-hover border-0">
        {/* Image Container */}
        <div className="relative aspect-[4/3] overflow-hidden">
          <img
            src={imageUrl}
            alt={title}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
          
          {/* Badges */}
          <div className="absolute top-3 left-3 flex gap-2">
            <Badge
              variant={type === "sale" ? "default" : "secondary"}
              className="capitalize"
            >
              For {type}
            </Badge>
            {featured && (
              <Badge variant="accent" className="bg-accent text-accent-foreground">
                Featured
              </Badge>
            )}
          </div>

          {/* Favorite Button */}
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-3 right-3 h-8 w-8 rounded-full bg-white/90 dark:bg-dark-elevated/90 hover:bg-white dark:hover:bg-dark-elevated"
            onClick={(e) => {
              e.preventDefault();
              onFavorite?.(id);
            }}
          >
            <Heart
              className={cn(
                "h-4 w-4 transition-colors",
                isFavorite ? "fill-destructive text-destructive" : "text-muted-foreground"
              )}
            />
          </Button>

          {/* Price Overlay */}
          <div className="absolute bottom-3 left-3 right-3">
            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-bold text-white">
                {formatPrice(price)}
              </span>
              {type === "rent" && (
                <span className="text-white/80 text-sm">/month</span>
              )}
            </div>
            {aiEstimate && (
              <div className="flex items-center gap-1 mt-1">
                <Badge variant="glass" className="text-xs">
                  AI Estimate: {formatPrice(aiEstimate)}
                </Badge>
              </div>
            )}
          </div>
        </div>

        {/* Content */}
        <CardContent className="p-4">
          <h3 className="font-semibold text-lg line-clamp-1 mb-1">{title}</h3>
          <div className="flex items-center gap-1 text-muted-foreground text-sm mb-3">
            <MapPin className="h-3.5 w-3.5" />
            <span className="line-clamp-1">{address}</span>
          </div>

          {/* Property Features */}
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <Bed className="h-4 w-4" />
              <span>{bedrooms}</span>
            </div>
            <div className="flex items-center gap-1">
              <Bath className="h-4 w-4" />
              <span>{bathrooms}</span>
            </div>
            <div className="flex items-center gap-1">
              <Square className="h-4 w-4" />
              <span>{sqft.toLocaleString()} sqft</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

export default PropertyCard;
