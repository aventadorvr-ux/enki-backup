"use client";

import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Users, Home, DollarSign, Activity } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface KPICardProps {
  title: string;
  value: string | number;
  change?: {
    value: string;
    trend: "up" | "down" | "neutral";
  };
  icon: React.ReactNode;
  description?: string;
  className?: string;
}

export function KPICard({
  title,
  value,
  change,
  icon,
  description,
  className,
}: KPICardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className={cn("glass-card border-0", className)}>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            {title}
          </CardTitle>
          <div className="h-8 w-8 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
            {icon}
          </div>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{value}</div>
          {change && (
            <div className="flex items-center gap-1 mt-1">
              {change.trend === "up" ? (
                <TrendingUp className="h-4 w-4 text-secondary" />
              ) : change.trend === "down" ? (
                <TrendingDown className="h-4 w-4 text-destructive" />
              ) : null}
              <span
                className={cn(
                  "text-sm",
                  change.trend === "up" && "text-secondary",
                  change.trend === "down" && "text-destructive",
                  change.trend === "neutral" && "text-muted-foreground"
                )}
              >
                {change.value}
              </span>
            </div>
          )}
          {description && (
            <p className="text-xs text-muted-foreground mt-2">{description}</p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}

// Pre-configured KPI cards for real estate dashboard
export function ActiveListingsCard({ count, change }: { count: number; change: string }) {
  return (
    <KPICard
      title="Active Listings"
      value={count}
      change={{ value: change, trend: "up" }}
      icon={<Home className="h-4 w-4" />}
      description="Properties currently listed"
    />
  );
}

export function TotalLeadsCard({ count, change }: { count: number; change: string }) {
  return (
    <KPICard
      title="Total Leads"
      value={count}
      change={{ value: change, trend: "up" }}
      icon={<Users className="h-4 w-4" />}
      description="New leads this month"
    />
  );
}

export function RevenueCard({ amount, change }: { amount: string; change: string }) {
  return (
    <KPICard
      title="Revenue"
      value={amount}
      change={{ value: change, trend: "up" }}
      icon={<DollarSign className="h-4 w-4" />}
      description="Commission revenue YTD"
    />
  );
}

export function ConversionRateCard({ rate, change }: { rate: string; change: string }) {
  return (
    <KPICard
      title="Conversion Rate"
      value={rate}
      change={{ value: change, trend: "neutral" }}
      icon={<Activity className="h-4 w-4" />}
      description="Leads to closed deals"
    />
  );
}

export default KPICard;
