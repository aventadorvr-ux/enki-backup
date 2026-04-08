"use client";

import { useState } from "react";
import { Metadata } from "next";
import { MapSearch } from "@/components/map/MapSearch";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

// Mock properties (unchanged)
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
    coordinates: { lat: -36.8565, lng: 174.7455 },
  },
];

export default function SearchPage() {
  const [suburb, setSuburb] = useState("Auckland Central");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function runMarketIntel() {
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("/api/market-intel", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action: "trends",
          suburb,
        }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Failed to fetch market intel" });
    }

    setLoading(false);
  }

  return (
    <main className="p-6 space-y-6">
      {/* Market Intel Panel */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="text-xl font-bold">Market Intelligence</h2>

          <input
            className="border px-3 py-2 rounded w-full"
            value={suburb}
            onChange={(e) => setSuburb(e.target.value)}
          />

          <Button onClick={runMarketIntel}>
            {loading ? "Loading..." : "Get Market Trends"}
          </Button>

          {result && (
            <pre className="text-sm whitespace-pre-wrap">
              {JSON.stringify(result, null, 2)}
            </pre>
          )}
        </CardContent>
      </Card>

      {/* Existing Map */}
      <MapSearch properties={mockProperties} />
    </main>
  );
}
