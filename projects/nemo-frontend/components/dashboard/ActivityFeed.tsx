"use client";

import { motion } from "framer-motion";
import { formatDistanceToNow } from "date-fns";
import { Card, CardContent, CardHeader, CardTitle } from "@components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { 
  UserPlus, 
  Home, 
  Calendar, 
  MessageSquare, 
  FileText, 
  TrendingUp,
  CheckCircle 
} from "lucide-react";

interface ActivityItem {
  id: string;
  type: "lead" | "property" | "appointment" | "message" | "document" | "milestone" | "task";
  title: string;
  description: string;
  timestamp: Date;
  user?: {
    name: string;
    avatar?: string;
  };
  metadata?: {
    propertyAddress?: string;
    leadName?: string;
    amount?: string;
  };
}

interface ActivityFeedProps {
  activities: ActivityItem[];
  className?: string;
  maxItems?: number;
}

const activityIcons = {
  lead: UserPlus,
  property: Home,
  appointment: Calendar,
  message: MessageSquare,
  document: FileText,
  milestone: TrendingUp,
  task: CheckCircle,
};

const activityColors = {
  lead: "bg-secondary",
  property: "bg-primary",
  appointment: "bg-accent",
  message: "bg-blue-500",
  document: "bg-purple-500",
  milestone: "bg-secondary",
  task: "bg-muted",
};

export function ActivityFeed({ activities, className, maxItems = 10 }: ActivityFeedProps) {
  const displayActivities = activities.slice(0, maxItems);

  return (
    <Card className={cn("glass-card border-0", className)}>
      <CardHeader>
        <CardTitle className="text-lg">Recent Activity</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="space-y-1">
          {displayActivities.map((activity, index) => {
            const Icon = activityIcons[activity.type];
            return (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-start gap-4 p-4 hover:bg-muted/50 transition-colors cursor-pointer"
              >
                {/* Icon */}
                <div
                  className={cn(
                    "h-10 w-10 rounded-full flex items-center justify-center flex-shrink-0",
                    activityColors[activity.type]
                  )}
                >
                  <Icon className="h-5 w-5 text-white" />
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <p className="font-medium text-sm">{activity.title}</p>
                      <p className="text-sm text-muted-foreground line-clamp-1">
                        {activity.description}
                      </p>
                      {activity.metadata?.propertyAddress && (
                        <p className="text-xs text-muted-foreground mt-1">
                          {activity.metadata.propertyAddress}
                        </p>
                      )}
                    </div>
                    <span className="text-xs text-muted-foreground flex-shrink-0">
                      {formatDistanceToNow(activity.timestamp, { addSuffix: true })}
                    </span>
                  </div>
                </div>

                {/* User Avatar */}
                {activity.user && (
                  <Avatar className="h-8 w-8 flex-shrink-0">
                    {activity.user.avatar ? (
                      <img src={activity.user.avatar} alt={activity.user.name} />
                    ) : null}
                    <AvatarFallback className="text-xs bg-muted">
                      {activity.user.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </AvatarFallback>
                  </Avatar>
                )}
              </motion.div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

// Example/mock data generator
export function generateMockActivities(count: number = 10): ActivityItem[] {
  const types: ActivityItem["type"][] = ["lead", "property", "appointment", "message", "document", "milestone", "task"];
  const actions = {
    lead: ["New lead assigned", "Lead qualified", "Lead contacted", "Lead converted"],
    property: ["New listing added", "Price updated", "Property sold", "Listing expired"],
    appointment: ["Open home scheduled", "Private viewing booked", "Inspection completed"],
    message: ["New inquiry received", "Follow-up sent", "Client replied"],
    document: ["Contract signed", "Disclosure uploaded", "CMA generated"],
    milestone: ["Monthly target reached", "Quarterly goal achieved"],
    task: ["Task completed", "Task overdue", "Task assigned"],
  };

  return Array.from({ length: count }, (_, i) => {
    const type = types[Math.floor(Math.random() * types.length)];
    const action = actions[type][Math.floor(Math.random() * actions[type].length)];
    
    return {
      id: `activity-${i}`,
      type,
      title: action,
      description: `Related to ${["property in Auckland", "buyer inquiry", "listing update", "client request"][Math.floor(Math.random() * 4)]}`,
      timestamp: new Date(Date.now() - Math.random() * 86400000 * 7),
      user: Math.random() > 0.3 ? {
        name: ["Sarah Johnson", "Mike Chen", "Emma Wilson", "David Park"][Math.floor(Math.random() * 4)],
      } : undefined,
      metadata: Math.random() > 0.5 ? {
        propertyAddress: "123 Queen Street, Auckland",
      } : undefined,
    };
  }).sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
}

export default ActivityFeed;
