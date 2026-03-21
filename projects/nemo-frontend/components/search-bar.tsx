"use client";

import { motion } from "framer-motion";
import { Search, MapPin, SlidersHorizontal, X } from "lucide-react";
import { useState, useRef } from "react";
import { cn } from "@/lib/utils";

interface SearchBarProps {
  onSearch?: (query: string) => void;
  className?: string;
  variant?: "default" | "hero" | "minimal";
  placeholder?: string;
}

export function SearchBar({
  onSearch,
  className,
  variant = "default",
  placeholder = "Search by location, property type...",
}: SearchBarProps) {
  const [query, setQuery] = useState("");
  const [isFocused, setIsFocused] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSearch = () => {
    onSearch?.(query);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  const clearSearch = () => {
    setQuery("");
    inputRef.current?.focus();
  };

  if (variant === "minimal") {
    return (
      <div className={cn("relative", className)}>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            className={cn(
              "h-10 w-full rounded-lg border border-gray-200 bg-white pl-9 pr-4",
              "text-sm placeholder:text-gray-400",
              "focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20",
              "dark:border-gray-700 dark:bg-slate-800 dark:text-white"
            )}
          />
          {query && (
            <button
              onClick={clearSearch}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    );
  }

  if (variant === "hero") {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className={cn("w-full max-w-4xl mx-auto", className)}
      >
        <div
          className={cn(
            "relative rounded-2xl bg-white dark:bg-slate-800 shadow-2xl transition-all duration-300",
            isFocused && "ring-4 ring-primary-500/20"
          )}
        >
          <div className="flex items-center p-2">
            <div className="flex flex-1 items-center gap-3 px-4">
              <Search className="h-5 w-5 text-primary-500" />
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                placeholder={placeholder}
                className="flex-1 bg-transparent py-4 text-lg text-gray-900 placeholder:text-gray-400 focus:outline-none dark:text-white"
              />
              {query && (
                <button
                  onClick={clearSearch}
                  className="rounded-full p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-slate-700"
                >
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleSearch}
              className="rounded-xl bg-primary-500 px-8 py-4 font-semibold text-white shadow-lg transition-colors hover:bg-primary-600"
            >
              Search
            </motion.button>
          </div>

          {/* Quick Location Chips */}
          <div className="border-t border-gray-100 px-4 py-3 dark:border-gray-700">
            <div className="flex items-center gap-3">
              <MapPin className="h-4 w-4 text-gray-400" />
              <div className="flex gap-2 overflow-x-auto pb-1">
                {["Auckland", "Wellington", "Christchurch", "Queenstown"].map(
                  (city) => (
                    <button
                      key={city}
                      onClick={() => {
                        setQuery(city);
                        onSearch?.(city);
                      }}
                      className={cn(
                        "whitespace-nowrap rounded-full px-3 py-1 text-sm transition-colors",
                        query === city
                          ? "bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300"
                          : "bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-slate-700 dark:text-gray-300 dark:hover:bg-slate-600"
                      )}
                    >
                      {city}
                    </button>
                  )
                )}
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    );
  }

  // Default variant
  return (
    <div className={cn("relative", className)}>
      <div className="relative flex items-center">
        <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className={cn(
            "h-12 w-full rounded-xl border border-gray-200 bg-white pl-12 pr-24",
            "text-base placeholder:text-gray-400",
            "focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20",
            "dark:border-gray-700 dark:bg-slate-800 dark:text-white"
          )}
        />
        <div className="absolute right-2 flex items-center gap-1">
          {query && (
            <button
              onClick={clearSearch}
              className="rounded-full p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-slate-700"
            >
              <X className="h-4 w-4" />
            </button>
          )}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSearch}
            className="rounded-lg bg-primary-500 p-2.5 text-white transition-colors hover:bg-primary-600"
          >
            <Search className="h-5 w-5" />
          </motion.button>
        </div>
      </div>
    </div>
  );
}

// Advanced Search with Filters
export function AdvancedSearchBar({
  onSearch,
  className,
}: {
  onSearch?: (query: string, filters: any) => void;
  className?: string;
}) {
  const [showFilters, setShowFilters] = useState(false);
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState({
    propertyType: "",
    minPrice: "",
    maxPrice: "",
    beds: "",
  });

  return (
    <div className={cn("space-y-4", className)}>
      <div className="relative">
        <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search location..."
          className={cn(
            "h-14 w-full rounded-xl border border-gray-200 bg-white pl-12 pr-32",
            "text-base placeholder:text-gray-400",
            "focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20",
            "dark:border-gray-700 dark:bg-slate-800 dark:text-white"
          )}
        />
        <div className="absolute right-2 top-1/2 flex -translate-y-1/2 items-center gap-2">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowFilters(!showFilters)}
            className={cn(
              "flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition-colors",
              showFilters
                ? "bg-primary-100 text-primary-700 dark:bg-primary-900/30"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-slate-700 dark:text-gray-300"
            )}
          >
            <SlidersHorizontal className="h-4 w-4" />
            Filters
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onSearch?.(query, filters)}
            className="rounded-lg bg-primary-500 px-6 py-2.5 font-medium text-white hover:bg-primary-600"
          >
            Search
          </motion.button>
        </div>
      </div>

      {/* Expandable Filters */}
      <motion.div
        initial={false}
        animate={{ height: showFilters ? "auto" : 0, opacity: showFilters ? 1 : 0 }}
        transition={{ duration: 0.3 }}
        className="overflow-hidden"
      >
        <div className="grid grid-cols-2 gap-3 rounded-xl bg-gray-50 p-4 dark:bg-slate-800/50 md:grid-cols-4">
          <select
            value={filters.propertyType}
            onChange={(e) => setFilters({ ...filters, propertyType: e.target.value })}
            className="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-slate-800 dark:text-white"
          >
            <option value="">Property Type</option>
            <option value="house">House</option>
            <option value="apartment">Apartment</option>
            <option value="townhouse">Townhouse</option>
            <option value="land">Land</option>
          </select>
          <select
            value={filters.minPrice}
            onChange={(e) => setFilters({ ...filters, minPrice: e.target.value })}
            className="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-slate-800 dark:text-white"
          >
            <option value="">Min Price</option>
            <option value="500000">$500k</option>
            <option value="750000">$750k</option>
            <option value="1000000">$1M</option>
            <option value="1500000">$1.5M</option>
          </select>
          <select
            value={filters.maxPrice}
            onChange={(e) => setFilters({ ...filters, maxPrice: e.target.value })}
            className="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-slate-800 dark:text-white"
          >
            <option value="">Max Price</option>
            <option value="750000">$750k</option>
            <option value="1000000">$1M</option>
            <option value="1500000">$1.5M</option>
            <option value="2000000">$2M+</option>
          </select>
          <select
            value={filters.beds}
            onChange={(e) => setFilters({ ...filters, beds: e.target.value })}
            className="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-slate-800 dark:text-white"
          >
            <option value="">Bedrooms</option>
            <option value="1">1+</option>
            <option value="2">2+</option>
            <option value="3">3+</option>
            <option value="4">4+</option>
          </select>
        </div>
      </motion.div>
    </div>
  );
}

export default SearchBar;
