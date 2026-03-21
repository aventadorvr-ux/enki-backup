"use client";

import { useState } from "react";
import { AdvancedSearchBar } from "@/components/search-bar";
import { PropertyCard } from "@/components/property-card";
import { PageTransition, StaggerContainer, StaggerItem } from "@/components/animations";
import { MapPin, List, Grid3X3, SlidersHorizontal } from "lucide-react";

const searchResults = [
  {
    id: "1",
    title: "Modern Villa with Ocean Views",
    address: "123 Beach Road, Auckland",
    price: 2450000,
    beds: 4,
    baths: 3,
    sqft: 320,
    imageUrl: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800",
    isFeatured: true,
    agentName: "Sarah Mitchell",
  },
  {
    id: "2",
    title: "Luxury Apartment in CBD",
    address: "45 Queen Street, Auckland",
    price: 1250000,
    beds: 2,
    baths: 2,
    sqft: 95,
    imageUrl: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800",
    isNew: true,
    agentName: "James Chen",
  },
  {
    id: "3",
    title: "Family Home with Garden",
    address: "78 Mountain View, Wellington",
    price: 980000,
    beds: 3,
    baths: 2,
    sqft: 180,
    imageUrl: "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800",
    agentName: "Emma Wilson",
  },
  {
    id: "4",
    title: "Contemporary Townhouse",
    address: "56 Park Avenue, Christchurch",
    price: 850000,
    beds: 3,
    baths: 2,
    sqft: 150,
    imageUrl: "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800",
    agentName: "David Brown",
  },
  {
    id: "5",
    title: "Waterfront Estate",
    address: "99 Harbour View, Queenstown",
    price: 3200000,
    beds: 5,
    baths: 4,
    sqft: 450,
    imageUrl: "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800",
    isFeatured: true,
    agentName: "Lisa Taylor",
  },
  {
    id: "6",
    title: "Cozy Suburban Home",
    address: "34 Maple Street, Hamilton",
    price: 720000,
    beds: 3,
    baths: 1,
    sqft: 140,
    imageUrl: "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800",
    agentName: "Tom Anderson",
  },
];

export default function SearchPage() {
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");

  return (
    <PageTransition>
      <div className="min-h-screen bg-gray-50 dark:bg-slate-900">
        {/* Search Header */}
        <div className="sticky top-0 z-10 border-b border-gray-200 bg-white/80 backdrop-blur-lg dark:border-gray-700 dark:bg-slate-900/80">
          <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
            <AdvancedSearchBar />
          </div>
        </div>

        {/* Results Header */}
        <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
                24 Properties Found
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                in Auckland, New Zealand
              </p>
            </div>
            <div className="flex items-center gap-3">
              <select className="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-slate-800 dark:text-white">
                <option>Sort by: Recommended</option>
                <option>Price: Low to High</option>
                <option>Price: High to Low</option>
                <option>Newest First</option>
              </select>
              <div className="flex rounded-lg border border-gray-200 bg-white p-1 dark:border-gray-700 dark:bg-slate-800">
                <button
                  onClick={() => setViewMode("grid")}
                  className={`rounded p-2 ${viewMode === "grid" ? "bg-primary-100 text-primary-600 dark:bg-primary-900/30" : "text-gray-400"}`}
                >
                  <Grid3X3 className="h-4 w-4" />
                </button>
                <button
                  onClick={() => setViewMode("list")}
                  className={`rounded p-2 ${viewMode === "list" ? "bg-primary-100 text-primary-600 dark:bg-primary-900/30" : "text-gray-400"}`}
                >
                  <List className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Results Grid */}
        <div className="mx-auto max-w-7xl px-4 pb-12 sm:px-6 lg:px-8">
          <StaggerContainer
            className={`grid gap-6 ${viewMode === "grid" ? "grid-cols-1 md:grid-cols-2 lg:grid-cols-3" : "grid-cols-1"}`}
          >
            {searchResults.map((property) => (
              <StaggerItem key={property.id}>
                <PropertyCard {...property} />
              </StaggerItem>
            ))}
          </StaggerContainer>
        </div>
      </div>
    </PageTransition>
  );
}
