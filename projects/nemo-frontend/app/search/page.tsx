import { Metadata } from "next";
import { MapSearch } from "@/components/map/MapSearch";

export const metadata: Metadata = {
  title: "Search Properties - NEMO",
  description: "Search properties with AI-powered filters and map view.",
};

// Mock properties data
const mockProperties = [
  {
    id: "1",
    title: "Modern Villa in Ponsonby",
    address: "123 Richmond Road, Ponsonby, Auckland",
    price: 1850000,
    bedrooms: 4,
    bathrooms: 3,
    sqft: 2400,
    imageUrl: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800",
    type: "sale" as const,
    featured: true,
    aiEstimate: 1820000,
    coordinates: { lat: -36.8565, lng: 174.7455 },
  },
  {
    id: "2",
    title: "Harbor View Apartment",
    address: "45 Albert Street, Auckland CBD",
    price: 950000,
    bedrooms: 2,
    bathrooms: 2,
    sqft: 1200,
    imageUrl: "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800",
    type: "sale" as const,
    aiEstimate: 975000,
    coordinates: { lat: -36.8485, lng: 174.7633 },
  },
  {
    id: "3",
    title: "Family Home in Remuera",
    address: "78 Remuera Road, Remuera",
    price: 2200000,
    bedrooms: 5,
    bathrooms: 3,
    sqft: 3200,
    imageUrl: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800",
    type: "sale" as const,
    featured: true,
    aiEstimate: 2150000,
    coordinates: { lat: -36.8705, lng: 174.7875 },
  },
  {
    id: "4",
    title: "Investment Property in Grey Lynn",
    address: "34 Tuarangi Road, Grey Lynn",
    price: 1200000,
    bedrooms: 3,
    bathrooms: 2,
    sqft: 1600,
    imageUrl: "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800",
    type: "rent" as const,
    aiEstimate: 1180000,
    coordinates: { lat: -36.8615, lng: 174.7355 },
  },
  {
    id: "5",
    title: "Luxury Penthouse",
    address: "101 Customs Street West, Viaduct Harbour",
    price: 3500000,
    bedrooms: 3,
    bathrooms: 3,
    sqft: 2800,
    imageUrl: "https://images.unsplash.com/photo-1600573472592-401b489a3cdc?w=800",
    type: "sale" as const,
    featured: true,
    aiEstimate: 3400000,
    coordinates: { lat: -36.8405, lng: 174.7555 },
  },
  {
    id: "6",
    title: "Townhouse in Parnell",
    address: "256 Parnell Road, Parnell",
    price: 1450000,
    bedrooms: 3,
    bathrooms: 2.5,
    sqft: 1800,
    imageUrl: "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=800",
    type: "sale" as const,
    aiEstimate: 1480000,
    coordinates: { lat: -36.8555, lng: 174.7775 },
  },
];

export default function SearchPage() {
  return (
    <main className="h-[calc(100vh-4rem)]">
      <MapSearch properties={mockProperties} />
    </main>
  );
}
