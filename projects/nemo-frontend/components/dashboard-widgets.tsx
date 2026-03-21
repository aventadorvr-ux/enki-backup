"use client";

import { motion } from "framer-motion";
import {
  TrendingUp,
  TrendingDown,
  Users,
  Home,
  DollarSign,
  Calendar,
  Eye,
  MessageSquare,
  ArrowUpRight,
  ArrowDownRight,
} from "lucide-react";
import { cn } from "@/lib/utils";

// Types
interface StatCardProps {
  title: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  icon: React.ReactNode;
  trend?: "up" | "down" | "neutral";
  className?: string;
  delay?: number;
}

interface ActivityItem {
  id: string;
  type: "view" | "inquiry" | "sale" | "listing";
  property?: string;
  user?: string;
  timestamp: string;
  value?: string;
}

// Stat Card Widget
export function StatCard({
  title,
  value,
  change,
  changeLabel,
  icon,
  trend = "neutral",
  className,
  delay = 0,
}: StatCardProps) {
  const isPositive = trend === "up" || (change && change > 0);
  const isNegative = trend === "down" || (change && change < 0);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className={cn(
        "rounded-xl border border-gray-100 bg-white p-6 dark:border-gray-700 dark:bg-slate-800",
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
            {title}
          </p>
          <h3 className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
            {value}
          </h3>
          {change !== undefined && (
            <div className="mt-2 flex items-center gap-1">
              <span
                className={cn(
                  "flex items-center gap-0.5 text-sm font-medium",
                  isPositive && "text-secondary-600 dark:text-secondary-400",
                  isNegative && "text-red-600 dark:text-red-400",
                  !isPositive && !isNegative && "text-gray-600 dark:text-gray-400"
                )}
              >
                {isPositive && <ArrowUpRight className="h-4 w-4" />}
                {isNegative && <ArrowDownRight className="h-4 w-4" />}
                {Math.abs(change)}%
              </span>
              {changeLabel && (
                <span className="text-sm text-gray-400">{changeLabel}</span>
              )}
            </div>
          )}
        </div>
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 dark:bg-primary-900/30 dark:text-primary-400">
          {icon}
        </div>
      </div>
    </motion.div>
  );
}

// Recent Activity Widget
export function RecentActivity({
  activities,
  className,
}: {
  activities: ActivityItem[];
  className?: string;
}) {
  const getIcon = (type: ActivityItem["type"]) => {
    switch (type) {
      case "view":
        return <Eye className="h-4 w-4" />;
      case "inquiry":
        return <MessageSquare className="h-4 w-4" />;
      case "sale":
        return <DollarSign className="h-4 w-4" />;
      case "listing":
        return <Home className="h-4 w-4" />;
    }
  };

  const getColor = (type: ActivityItem["type"]) => {
    switch (type) {
      case "view":
        return "bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400";
      case "inquiry":
        return "bg-accent-100 text-accent-600 dark:bg-accent-900/30 dark:text-accent-400";
      case "sale":
        return "bg-secondary-100 text-secondary-600 dark:bg-secondary-900/30 dark:text-secondary-400";
      case "listing":
        return "bg-primary-100 text-primary-600 dark:bg-primary-900/30 dark:text-primary-400";
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.2 }}
      className={cn(
        "rounded-xl border border-gray-100 bg-white dark:border-gray-700 dark:bg-slate-800",
        className
      )}
    >
      <div className="border-b border-gray-100 p-6 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          Recent Activity
        </h3>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Latest actions on your properties
        </p>
      </div>
      <div className="divide-y divide-gray-100 dark:divide-gray-700">
        {activities.map((activity, index) => (
          <motion.div
            key={activity.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
            className="flex items-center gap-4 p-4 hover:bg-gray-50 dark:hover:bg-slate-700/50"
          >
            <div
              className={cn(
                "flex h-10 w-10 items-center justify-center rounded-full",
                getColor(activity.type)
              )}
            >
              {getIcon(activity.type)}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                {activity.property}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {activity.user} • {activity.timestamp}
              </p>
            </div>
            {activity.value && (
              <span className="text-sm font-semibold text-secondary-600 dark:text-secondary-400">
                {activity.value}
              </span>
            )}
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}

// Quick Actions Widget
export function QuickActions({ className }: { className?: string }) {
  const actions = [
    { icon: Home, label: "Add Property", color: "bg-primary-500" },
    { icon: Calendar, label: "Schedule Viewing", color: "bg-secondary-500" },
    { icon: Users, label: "Manage Leads", color: "bg-accent-500" },
    { icon: TrendingUp, label: "View Analytics", color: "bg-purple-500" },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.3 }}
      className={cn(
        "rounded-xl border border-gray-100 bg-white p-6 dark:border-gray-700 dark:bg-slate-800",
        className
      )}
    >
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
        Quick Actions
      </h3>
      <div className="mt-4 grid grid-cols-2 gap-3">
        {actions.map((action, index) => (
          <motion.button
            key={action.label}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.3 + index * 0.05 }}
            className="flex flex-col items-center gap-2 rounded-xl border border-gray-100 p-4 text-center transition-colors hover:bg-gray-50 dark:border-gray-700 dark:hover:bg-slate-700"
          >
            <div className={cn("flex h-10 w-10 items-center justify-center rounded-full text-white", action.color)}>
              <action.icon className="h-5 w-5" />
            </div>
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {action.label}
            </span>
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
}

// Performance Chart Widget (Simple Bar Chart)
export function PerformanceChart({
  data,
  className,
}: {
  data: { label: string; value: number; color?: string }[];
  className?: string;
}) {
  const maxValue = Math.max(...data.map((d) => d.value));

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.1 }}
      className={cn(
        "rounded-xl border border-gray-100 bg-white p-6 dark:border-gray-700 dark:bg-slate-800",
        className
      )}
    >
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Performance
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Monthly property views
          </p>
        </div>
        <div className="flex items-center gap-1 text-sm text-secondary-600 dark:text-secondary-400">
          <TrendingUp className="h-4 w-4" />
          <span>+12.5%</span>
        </div>
      </div>
      <div className="space-y-3">
        {data.map((item, index) => (
          <div key={item.label} className="space-y-1">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-400">{item.label}</span>
              <span className="font-medium text-gray-900 dark:text-white">
                {item.value}
              </span>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-gray-100 dark:bg-gray-700">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${(item.value / maxValue) * 100}%` }}
                transition={{ duration: 0.8, delay: index * 0.1, ease: "easeOut" }}
                className={cn(
                  "h-full rounded-full",
                  item.color || "bg-primary-500"
                )}
              />
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

// Dashboard Stats Grid
export function DashboardStats() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <StatCard
        title="Total Properties"
        value="24"
        change={8}
        changeLabel="vs last month"
        icon={<Home className="h-6 w-6" />}
        trend="up"
        delay={0}
      />
      <StatCard
        title="Active Listings"
        value="18"
        change={12}
        changeLabel="vs last month"
        icon={<Eye className="h-6 w-6" />}
        trend="up"
        delay={0.1}
      />
      <StatCard
        title="Total Value"
        value="$4.2M"
        change={5}
        changeLabel="vs last month"
        icon={<DollarSign className="h-6 w-6" />}
        trend="up"
        delay={0.2}
      />
      <StatCard
        title="New Leads"
        value="47"
        change={-3}
        changeLabel="vs last month"
        icon={<Users className="h-6 w-6" />}
        trend="down"
        delay={0.3}
      />
    </div>
  );
}

export {
  TrendingUp,
  TrendingDown,
  Users,
  Home,
  DollarSign,
  Calendar,
  Eye,
  MessageSquare,
};
