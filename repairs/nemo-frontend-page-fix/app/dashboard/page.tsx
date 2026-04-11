import { Metadata } from "next";
import { KPICard, ActiveListingsCard, TotalLeadsCard, RevenueCard, ConversionRateCard } from "@/components/dashboard/KPICards";
import { ActivityFeed, generateMockActivities } from "@/components/dashboard/ActivityFeed";
import { AIChatInterface } from "@/components/ai/AIChatInterface";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export const metadata: Metadata = {
  title: "Dashboard - NEMO",
  description: "Agent dashboard with KPIs, activity feed, and AI assistant.",
};

const mockActivities = generateMockActivities(10);

export default function DashboardPage() {
  return (
    <main className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">Welcome back! Here's what's happening today.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <ActiveListingsCard count={24} change="+3 this week" />
        <TotalLeadsCard count={156} change="+12 this week" />
        <RevenueCard amount="$128.5K" change="+8.2% vs last month" />
        <ConversionRateCard rate="12.4%" change="+1.2% vs last month" />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Activity Feed */}
        <div className="lg:col-span-2 space-y-8">
          <ActivityFeed activities={mockActivities} />
          
          {/* Quick Stats */}
          <Card className="glass-card border-0">
            <CardHeader>
              <CardTitle>Monthly Performance</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-64 flex items-center justify-center text-muted-foreground">
                <p>Chart component placeholder - integrate Recharts here</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column - AI Assistant */}
        <div className="lg:col-span-1">
          <AIChatInterface className="sticky top-8" />
        </div>
      </div>
    </main>
  );
}
