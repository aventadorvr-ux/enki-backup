"use client";

import { DashboardStats, RecentActivity, QuickActions, PerformanceChart } from "@/components/dashboard-widgets";
import { PageTransition } from "@/components/animations";

const recentActivities = [
  {
    id: "1",
    type: "view" as const,
    property: "Modern Villa with Ocean Views",
    user: "John Smith",
    timestamp: "2 minutes ago",
  },
  {
    id: "2",
    type: "inquiry" as const,
    property: "Luxury Apartment in CBD",
    user: "Sarah Johnson",
    timestamp: "15 minutes ago",
  },
  {
    id: "3",
    type: "sale" as const,
    property: "Family Home with Garden",
    user: "Mike Wilson",
    timestamp: "1 hour ago",
    value: "$980,000",
  },
  {
    id: "4",
    type: "listing" as const,
    property: "New Property Listed",
    user: "You",
    timestamp: "2 hours ago",
  },
];

const performanceData = [
  { label: "Jan", value: 45, color: "bg-primary-500" },
  { label: "Feb", value: 62, color: "bg-primary-500" },
  { label: "Mar", value: 58, color: "bg-primary-500" },
  { label: "Apr", value: 75, color: "bg-primary-500" },
  { label: "May", value: 82, color: "bg-secondary-500" },
  { label: "Jun", value: 95, color: "bg-secondary-500" },
];

export default function DashboardPage() {
  return (
    <PageTransition>
      <div className="min-h-screen bg-gray-50 py-8 dark:bg-slate-900">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Dashboard
            </h1>
            <p className="mt-2 text-gray-600 dark:text-gray-400">
              Welcome back! Here is what is happening with your properties.
            </p>
          </div>

          {/* Stats Grid */}
          <DashboardStats />

          {/* Main Content */}
          <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-3">
            {/* Left Column */}
            <div className="lg:col-span-2 space-y-6">
              <PerformanceChart data={performanceData} />
              <RecentActivity activities={recentActivities} />
            </div>

            {/* Right Column */}
            <div className="space-y-6">
              <QuickActions />
            </div>
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
