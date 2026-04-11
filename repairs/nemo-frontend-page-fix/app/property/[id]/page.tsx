import { Metadata } from "next";
import { PropertyDetailView } from "@/components/property/PropertyDetailView";

// This would normally fetch from an API
const mockProperty = {
  id: "1",
  title: "Modern Villa in Ponsonby",
  address: "123 Richmond Road, Ponsonby, Auckland 1011",
  price: 1850000,
  bedrooms: 4,
  bathrooms: 3,
  sqft: 2400,
  lotSize: "650 sqm",
  yearBuilt: 2018,
  propertyType: "Villa",
  description: `Stunning modern villa in the heart of Ponsonby, featuring contemporary design with premium finishes throughout. This exceptional property offers spacious open-plan living with seamless indoor-outdoor flow to a beautifully landscaped garden.

The chef's kitchen includes Miele appliances, stone benchtops, and a butler's pantry. The master suite features a walk-in wardrobe and luxury ensuite. Additional highlights include a separate media room, double garage, and proximity to Ponsonby's vibrant dining and shopping precinct.

Perfect for families seeking luxury living in one of Auckland's most sought-after locations.`,
  images: [
    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200",
    "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1200",
    "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=1200",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200",
  ],
  features: [
    "Open plan living",
    "Miele appliances",
    "Butler's pantry",
    "Master with ensuite",
    "Walk-in wardrobes",
    "Media room",
    "Double garage",
    "Landscaped garden",
    "Ducted heating",
    "Alarm system",
    "LED lighting",
    "Water filtration",
  ],
  agent: {
    name: "Sarah Johnson",
    phone: "+64 21 123 4567",
    email: "sarah@nemorealestate.co.nz",
    image: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200",
    company: "NEMO Real Estate",
  },
  aiInsights: {
    estimate: 1820000,
    confidence: 87,
    trend: "up" as const,
    trendValue: "+3.2% this quarter",
  },
};

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  return {
    title: `${mockProperty.title} - NEMO`,
    description: mockProperty.description.slice(0, 160),
  };
}

export default function PropertyDetailPage({ params }: { params: { id: string } }) {
  return (
    <main className="container mx-auto px-4 py-8">
      <PropertyDetailView property={mockProperty} />
    </main>
  );
}
