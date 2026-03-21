import { SearchBar } from "@/components/search-bar";
import { PropertyCard } from "@/components/property-card";
import { Sparkles } from "lucide-react";

const featuredProperties = [
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
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-secondary-50 pb-20 pt-32 dark:from-slate-900 dark:via-slate-900 dark:to-slate-800">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -right-40 -top-40 h-96 w-96 rounded-full bg-primary-200/30 blur-3xl dark:bg-primary-500/10" />
          <div className="absolute -bottom-40 -left-40 h-96 w-96 rounded-full bg-secondary-200/30 blur-3xl dark:bg-secondary-500/10" />
        </div>

        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-primary-100 px-4 py-2 text-sm font-medium text-primary-700 dark:bg-primary-900/30 dark:text-primary-300">
              <Sparkles className="h-4 w-4" />
              Powered by AI Agents
            </div>

            <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-5xl md:text-6xl">
              Find Your Dream Home with AI Intelligence
            </h1>

            <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600 dark:text-gray-300">
              Search thousands of properties across New Zealand. Our AI agents help you find your perfect property.
            </p>

            <div className="mx-auto mt-10 max-w-3xl">
              <SearchBar variant="hero" />
            </div>
          </div>
        </div>
      </section>

      {/* Featured Properties */}
      <section className="bg-white py-20 dark:bg-slate-900">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mb-10">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
              Featured Properties
            </h2>
            <p className="mt-2 text-gray-600 dark:text-gray-400">
              Hand-picked properties selected by our AI for you
            </p>
          </div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {featuredProperties.map((property) => (
              <PropertyCard key={property.id} {...property} />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
