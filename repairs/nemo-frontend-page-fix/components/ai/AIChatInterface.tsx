"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, User, Sparkles, Loader2, X } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  metadata?: {
    confidence?: number;
    sources?: string[];
    actions?: {
      label: string;
      action: () => void;
    }[];
  };
}

interface AIChatInterfaceProps {
  className?: string;
  initialMessages?: Message[];
  onSendMessage?: (message: string) => Promise<string>;
  suggestions?: string[];
  title?: string;
}

export function AIChatInterface({
  className,
  initialMessages = [],
  onSendMessage,
  suggestions = [
    "Find properties under $800k in Auckland",
    "What's the market trend for Ponsonby?",
    "Generate a listing description",
    "Schedule an open home for next weekend",
  ],
  title = "NEMO AI Assistant",
}: AIChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: `msg-${Date.now()}`,
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setShowSuggestions(false);

    // Simulate or call actual AI endpoint
    let response: string;
    if (onSendMessage) {
      response = await onSendMessage(input);
    } else {
      // Mock response for demo
      await new Promise((resolve) => setTimeout(resolve, 1500));
      response = generateMockResponse(input);
    }

    const assistantMessage: Message = {
      id: `msg-${Date.now() + 1}`,
      role: "assistant",
      content: response,
      timestamp: new Date(),
      metadata: {
        confidence: Math.floor(Math.random() * 20) + 80,
      },
    };

    setMessages((prev) => [...prev, assistantMessage]);
    setIsLoading(false);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
  };

  return (
    <Card className={cn("glass-card border-0 flex flex-col h-[600px]", className)}>
      {/* Header */}
      <CardHeader className="border-b border-border/50">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
            <Bot className="h-5 w-5 text-white" />
          </div>
          <div>
            <CardTitle className="text-lg">{title}</CardTitle>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-secondary animate-pulse" />
              <span className="text-xs text-muted-foreground">Online</span>
            </div>
          </div>
        </div>
      </CardHeader>

      {/* Messages */}
      <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence initial={false}>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className={cn(
                "flex gap-3",
                message.role === "user" ? "flex-row-reverse" : "flex-row"
              )}
            >
              {/* Avatar */}
              <div
                className={cn(
                  "h-8 w-8 rounded-full flex items-center justify-center flex-shrink-0",
                  message.role === "user"
                    ? "bg-muted"
                    : "bg-gradient-to-br from-primary to-secondary"
                )}
              >
                {message.role === "user" ? (
                  <User className="h-4 w-4 text-foreground" />
                ) : (
                  <Bot className="h-4 w-4 text-white" />
                )}
              </div>

              {/* Message Bubble */}
              <div
                className={cn(
                  "max-w-[80%] rounded-2xl px-4 py-2.5",
                  message.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted"
                )}
              >
                <p className="text-sm leading-relaxed">{message.content}</p>
                
                {/* Metadata for AI messages */}
                {message.role === "assistant" && message.metadata?.confidence && (
                  <div className="flex items-center gap-2 mt-2 pt-2 border-t border-border/50">
                    <Sparkles className="h-3 w-3 text-accent" />
                    <span className="text-xs text-muted-foreground">
                      {message.metadata.confidence}% confidence
                    </span>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Loading indicator */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex gap-3"
          >
            <div className="h-8 w-8 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
              <Bot className="h-4 w-4 text-white" />
            </div>
            <div className="bg-muted rounded-2xl px-4 py-3 flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span className="text-sm text-muted-foreground">Thinking...</span>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />

        {/* Suggestions */}
        {showSuggestions && messages.length === 0 && (
          <div className="pt-4">
            <p className="text-sm text-muted-foreground mb-3">Try asking:</p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((suggestion) => (
                <Button
                  key={suggestion}
                  variant="outline"
                  size="sm"
                  className="text-xs glass-card"
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  {suggestion}
                </Button>
              ))}
            </div>
          </div>
        )}
      </CardContent>

      {/* Input */}
      <CardContent className="border-t border-border/50 p-4">
        <div className="flex gap-2">
          <Input
            placeholder="Ask NEMO anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            className="flex-1 glass-card border-0"
            disabled={isLoading}
          />
          <Button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="px-4"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

// Mock response generator for demo
function generateMockResponse(input: string): string {
  const lowerInput = input.toLowerCase();
  
  if (lowerInput.includes("property") || lowerInput.includes("house")) {
    return "I found 12 properties matching your criteria. The average price in this area is $850,000. Would you like me to send you a detailed list or schedule viewings?";
  }
  if (lowerInput.includes("market") || lowerInput.includes("trend")) {
    return "The market in this area has shown a 5.2% increase over the past 12 months. Inventory is up 15% compared to last quarter, giving buyers more options.";
  }
  if (lowerInput.includes("description") || lowerInput.includes("listing")) {
    return "I've generated a compelling listing description for your property. It highlights the key features and uses SEO-optimized keywords. Would you like me to refine it or generate social media variations?";
  }
  if (lowerInput.includes("schedule") || lowerInput.includes("open home")) {
    return "I've checked your calendar and scheduled open homes for Saturday 2-4pm and Sunday 11am-1pm. I've also set up automated notifications for interested buyers.";
  }
  
  return "I understand. Let me help you with that. Could you provide a bit more detail so I can give you the most accurate assistance?";
}

export default AIChatInterface;
