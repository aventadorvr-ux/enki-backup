"use client";

import { motion } from "framer-motion";
import { Heart, MapPin, Bed, Bath, Maximize, Share2 } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface PropertyCardProps {
  id: string;
  title: string;
  address: string;
  price: number;
  beds: number;
  baths: number;
  sqft: number;
  imageUrl: string;
  isFeatured?: boolean;
  isNew?: boolean;
  agentName?: string;
  agentImage?: string;
  className?: string;
  onClick?: () => void;
  onFavorite?: (id: string) => void;
}

export function PropertyCard({
  id,
  title,
  address,
  price,
  beds,
  baths,
  sqft,
  imageUrl,
  isFeatured = false,
  isNew = false,
  agentName,
  agentImage,
  className,
  onClick,
  onFavorite,
}: PropertyCardProps) {
  const [isFavorited, setIsFavorited] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);

  const handleFavorite = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsFavorited(!isFavorited);
    onFavorite?.(id);
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("en-NZ", {
      style: "currency",
      currency: "NZD",
      maximumFractionDigits: 0,
    }).format(price);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
      className={cn(
        "group cursor-pointer overflow-hidden rounded-2xl bg-white dark:bg-slate-800",
        "shadow-sm hover:shadow-xl transition-shadow duration-300",
        className
      )}
      onClick={onClick}
    >
      {/* Image Container */}
      <div className="relative aspect-[4/3] overflow-hidden">
        {/* Loading Skeleton */}
        {!imageLoaded && (
          <div className="absolute inset-0 animate-pulse bg-gray-200 dark:bg-slate-700" />
        )}
        
        {/* Property Image */}
        <img
          src={imageUrl}
          alt={title}
          className={cn(
            "h-full w-full object-cover transition-transform duration-500",
            "group-hover:scale-105",
            imageLoaded ? "opacity-100" : "opacity-0"
          )}
          onLoad={() => setImageLoaded(true)}
        />

        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

        {/* Badges */}
        <div className="absolute top-3 left-3 flex gap-2">
          {isFeatured && (
            <span className="inline-flex items-center gap-1 rounded-full bg-accent-500 px-2.5 py-1 text-xs font-semibold text-white shadow-lg">
              <span className="text-[10px]">★</span> Featured
            </span>
          )}
          {isNew && (
            <span className="inline-flex items-center rounded-full bg-secondary-500 px-2.5 py-1 text-xs font-semibold text-white shadow-lg">
              New
            </span>
          )}
        </div>

        {/* Action Buttons */}
        <div className="absolute top-3 right-3 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleFavorite}
            className={cn(
              "flex h-8 w-8 items-center justify-center rounded-full shadow-lg transition-colors",
              isFavorited
                ? "bg-red-500 text-white"
                : "bg-white/90 text-gray-600 hover:bg-white hover:text-red-500"
            )}
          >
            <Heart
              className={cn("h-4 w-4", isFavorited && "fill-current")}
            />
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            className="flex h-8 w-8 items-center justify-center rounded-full bg-white/90 text-gray-600 shadow-lg hover:bg-white hover:text-primary-500"
          >
            <Share2 className="h-4 w-4" />
          </motion.button>
        </div>

        {/* Price Tag */}
        <div className="absolute bottom-3 left-3">
          <p className="text-2xl font-bold text-white drop-shadow-lg">
            {formatPrice(price)}
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="p-5">
        {/* Title */}
        <h3 className="mb-1 text-lg font-semibold text-gray-900 dark:text-white line-clamp-1">
          {title}
        </h3>

        {/* Address */}
        <div className="mb-3 flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400">
          <MapPin className="h-4 w-4 flex-shrink-0" />
          <span className="line-clamp-1">{address}</span>
        </div>

        {/* Property Features */}
        <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
          <div className="flex items-center gap-1.5">
            <Bed className="h-4 w-4" />
            <span className="font-medium">{beds}</span>
            <span className="text-gray-400">beds</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Bath className="h-4 w-4" />
            <span className="font-medium">{baths}</span>
            <span className="text-gray-400">baths</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Maximize className="h-4 w-4" />
            <span className="font-medium">{sqft}</span>
            <span className="text-gray-400">m²</span>
          </div>
        </div>

        {/* Agent Info (if provided) */}
        {agentName && (
          <div className="mt-4 flex items-center gap-3 border-t border-gray-100 dark:border-gray-700 pt-4">
            {agentImage ? (
              <img
                src={agentImage}
                alt={agentName}
                className="h-8 w-8 rounded-full object-cover"
              />
            ) : (
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400 text-sm font-semibold">
                {agentName.charAt(0)}
              </div>
            )}
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {agentName}
            </span>
          </div>
        )}
      </div>
    </motion.div>
  );
}

// Skeleton Loading State
export function PropertyCardSkeleton() {
  return (
    <div className="overflow-hidden rounded-2xl bg-white dark:bg-slate-800 shadow-sm">
      <div className="aspect-[4/3] animate-pulse bg-gray-200 dark:bg-slate-700" />
      <div className="p-5">
        <div className="mb-2 h-6 w-3/4 animate-pulse rounded bg-gray-200 dark:bg-slate-700" />
        <div className="mb-4 h-4 w-1/2 animate-pulse rounded bg-gray-200 dark:bg-slate-700" />
        <div className="flex gap-4">
          <div className="h-4 w-16 animate-pulse rounded bg-gray-200 dark:bg-slate-700" />
          <div className="h-4 w-16 animate-pulse rounded bg-gray-200 dark:bg-slate-700" />
          <div className="h-4 w-16 animate-pulse rounded bg-gray-200 dark:bg-slate-700" />
        </div>
      </div>
    </div>
  );
}

export default PropertyCard;
