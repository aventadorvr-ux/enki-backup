"use client";

import { AIChatInterface } from "@/components/ai/AIChatInterface";
import { ActivityFeed, generateMockActivities } from "@/components/dashboard/ActivityFeed";
import { ActiveListingsCard, TotalLeadsCard, RevenueCard, ConversionRateCard } from "@/components/dashboard/KPICards";

const mockActivities = generateMockActivities(10);

export default function DashboardPage() {
  async function handleAI(message: string): Promise<string> {
    const res = await fetch("/api/ai", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    return data.response || data.error || "No response";
  }

  return (
    <main className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <ActiveListingsCard count={24} change="+3 this week" />
        <TotalLeadsCard count={156} change="+12 this week" />
        <RevenueCard amount="$128.5K" change="+8.2%" />
        <ConversionRateCard rate="12.4%" change="+1.2%" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <ActivityFeed activities={mockActivities} />
        </div>

        <div>
          <AIChatInterface onSendMessage={handleAI} />
        </div>
      </div>
    </main>
  );
}
