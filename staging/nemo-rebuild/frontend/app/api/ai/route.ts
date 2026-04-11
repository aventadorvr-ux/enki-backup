import { NextResponse } from "next/server";

function extractSuburb(message: string): string {
  const knownSuburbs = [
    "Auckland Central",
    "Ponsonby",
    "Parnell",
    "Newmarket",
    "Remuera",
    "Mt Eden",
    "Takapuna",
    "Grey Lynn",
    "Manukau",
  ];

  const lower = message.toLowerCase();
  for (const suburb of knownSuburbs) {
    if (lower.includes(suburb.toLowerCase())) return suburb;
  }
  return "Ponsonby";
}

function extractBedrooms(message: string): number | null {
  const match = message.match(/(\d+)\s*(bed|bedroom)/i);
  return match ? Number(match[1]) : null;
}

function extractBathrooms(message: string): number {
  const match = message.match(/(\d+)\s*(bath|bathroom)/i);
  return match ? Number(match[1]) : 2;
}

function extractTone(message: string): string {
  const lower = message.toLowerCase();
  if (lower.includes("luxury")) return "luxury";
  if (lower.includes("friendly")) return "friendly";
  if (lower.includes("modern")) return "modern";
  return "professional";
}

function extractMaxPrice(message: string): number | null {
  const cleaned = message.replace(/,/g, "").toLowerCase();
  const underMatch = cleaned.match(/under\s*\$?\s*(\d+(?:\.\d+)?)\s*([km]?)/i);
  const maxMatch = cleaned.match(/max(?:imum)?\s*\$?\s*(\d+(?:\.\d+)?)\s*([km]?)/i);
  const match = underMatch || maxMatch;
  if (!match) return null;

  let value = Number(match[1]);
  const suffix = (match[2] || "").toLowerCase();
  if (suffix === "k") value *= 1000;
  if (suffix === "m") value *= 1000000;
  return Math.round(value);
}

function formatWorkflowResponse(data: any): string {
  const status = data?.status ?? "unknown";
  const workflow = data?.workflow ?? "workflow";
  const proof = Array.isArray(data?.proof) ? data.proof : [];
  const skipped = Array.isArray(data?.skipped) ? data.skipped : [];
  const results = data?.results ?? {};

  const lines: string[] = [];

  lines.push(`Workflow: ${workflow}`);
  lines.push(`Status: ${status.toUpperCase()}`);

  if (data?.failed_step) {
    lines.push(`Failed step: ${data.failed_step}`);
  }
  if (data?.reason) {
    lines.push(`Reason: ${data.reason}`);
  }

  if (proof.length > 0) {
    lines.push("");
    lines.push("Completed steps:");
    for (const step of proof) {
      lines.push(`• ${step.step}`);
    }
  }

  if (skipped.length > 0) {
    lines.push("");
    lines.push("Skipped steps:");
    for (const step of skipped) {
      lines.push(`• ${step.step} — ${step.reason}`);
    }
  }

  if (results.lead) {
    lines.push("");
    lines.push("Lead:");
    lines.push(`• Qualified: ${results.lead.qualified}`);
    lines.push(`• Score: ${results.lead.score}`);
    lines.push(`• Priority: ${results.lead.priority}`);
  }

  if (results.market) {
    lines.push("");
    lines.push("Market:");
    lines.push(`• Suburb: ${results.market.suburb}`);
    lines.push(`• Trend: ${results.market.trend}`);
    lines.push(`• Median price: $${results.market.median_price}`);
    lines.push(`• Price change: ${results.market.price_change}%`);
  }

  if (results.content) {
    lines.push("");
    lines.push("Content:");
    lines.push(`• Tone: ${results.content.tone}`);
    lines.push(`• Words: ${results.content.word_count}`);
    if (results.content.description) {
      const preview =
        results.content.description.length > 260
          ? results.content.description.slice(0, 260) + "..."
          : results.content.description;
      lines.push(`• Preview: ${preview}`);
    }
  }

  if (results.transaction?.progress) {
    lines.push("");
    lines.push("Transaction:");
    lines.push(`• Progress: ${results.transaction.progress.completion_percentage}%`);
    lines.push(`• Status: ${results.transaction.progress.status}`);
  }

  if (results.risk) {
    lines.push("");
    lines.push("Risk:");
    lines.push(`• Overall risk: ${results.risk.overall_risk}`);
    lines.push(`• High risks: ${results.risk.high_risk_count}`);
    lines.push(`• Medium risks: ${results.risk.medium_risk_count}`);
    if (Array.isArray(results.risk.recommendations) && results.risk.recommendations.length > 0) {
      lines.push(`• Next action: ${results.risk.recommendations[0]}`);
    }
  }

  if (status === "completed") {
    lines.push("");
    lines.push("Next action:");
    if (workflow === "lead_to_listing") {
      lines.push("• Review the generated listing copy and prepare the listing package.");
    } else if (workflow === "deal_execution") {
      lines.push("• Review risk/checklist output and move the deal to the next controlled step.");
    } else {
      lines.push("• Review workflow outputs and continue with the next operator-approved action.");
    }
  }

  return lines.join("\n");
}

export async function POST(req: Request) {
  try {
    const { message } = await req.json();
    const text = String(message || "");
    const lower = text.toLowerCase();

    const suburb = extractSuburb(text);
    const bedrooms = extractBedrooms(text) ?? 3;
    const bathrooms = extractBathrooms(text);
    const tone = extractTone(text);
    const maxPrice = extractMaxPrice(text);

    // WORKFLOW: lead_to_listing
    if (
      lower.includes("lead to listing") ||
      lower.includes("listing workflow") ||
      lower.includes("run listing workflow")
    ) {
      const res = await fetch("http://127.0.0.1:8000/api/v1/orchestrate/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          workflow: "lead_to_listing",
          data: {
            lead_id: "dashboard_listing_lead",
            property_id: "dashboard_listing_property",
            location: suburb,
            bedrooms,
            bathrooms,
            budget: maxPrice ?? 900000,
          },
        }),
      });

      const data = await res.json();
      return NextResponse.json({
        response: formatWorkflowResponse(data),
      });
    }

    // WORKFLOW: deal_execution
    if (
      lower.includes("deal execution") ||
      lower.includes("run deal workflow") ||
      lower.includes("execute deal")
    ) {
      const res = await fetch("http://127.0.0.1:8000/api/v1/orchestrate/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          workflow: "deal_execution",
          data: {
            lead_id: "dashboard_deal_lead",
            property_id: "dashboard_deal_property",
            location: suburb,
            bedrooms,
            bathrooms,
            budget: maxPrice ?? 900000,
            pre_approved: true,
            days_to_settlement: 30,
            finance_approved: true,
            building_report_complete: true,
            lawyer_assigned: true,
          },
        }),
      });

      const data = await res.json();
      return NextResponse.json({
        response: formatWorkflowResponse(data),
      });
    }

    // PROPERTY SEARCH
    const looksLikePropertySearch =
      lower.includes("find properties") ||
      lower.includes("find property") ||
      lower.includes("show properties") ||
      lower.includes("search properties") ||
      lower.includes("property search") ||
      (lower.includes("properties") &&
        (lower.includes("under $") ||
          lower.includes("bedroom") ||
          lower.includes("bed ") ||
          lower.includes("in ")));

    if (looksLikePropertySearch) {
      const body: any = { suburb };
      if (maxPrice) body.max_price = maxPrice;
      if (bedrooms) body.bedrooms = bedrooms;

      const res = await fetch("http://127.0.0.1:8000/api/v1/enki/property/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await res.json();
      const results = Array.isArray(data?.results) ? data.results : [];

      if (!results.length) {
        return NextResponse.json({
          response: `No matching properties found for ${suburb}${maxPrice ? ` under $${maxPrice}` : ""}${bedrooms ? ` with ${bedrooms} bedrooms` : ""}.`,
        });
      }

      const lines = results.slice(0, 5).map((p: any, i: number) =>
        `${i + 1}. ${p.title} — $${p.price} — ${p.bedrooms} bed / ${p.bathrooms} bath`
      );

      return NextResponse.json({
        response: `Found ${results.length} matching propert${results.length === 1 ? "y" : "ies"}:\n${lines.join("\n")}`,
      });
    }

    // MARKET
    if (lower.includes("trend") || lower.includes("market")) {
      const res = await fetch("http://127.0.0.1:8000/api/v1/agents/market_intel/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "trends",
          data: { suburb },
        }),
      });

      const data = await res.json();
      const result = data?.result || {};
      return NextResponse.json({
        response:
          `${suburb} market update:\n` +
          `• Median price: $${result.median_price ?? "N/A"}\n` +
          `• Price change: ${result.price_change ?? "N/A"}%\n` +
          `• Inventory: ${result.inventory_level ?? "N/A"}\n` +
          `• Trend: ${result.trend ?? "N/A"}\n` +
          `• Insight: ${result.ai_insights ?? "No insight available."}`,
      });
    }

    // CONTENT
    if (lower.includes("description") || lower.includes("listing")) {
      const res = await fetch("http://127.0.0.1:8000/api/v1/agents/content/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "description_ai",
          data: {
            bedrooms,
            bathrooms,
            location: suburb,
            tone,
            features: ["modern kitchen", "garage", "outdoor entertaining"],
          },
        }),
      });

      const data = await res.json();
      const output = data?.result?.description || data?.description || "No description returned.";
      return NextResponse.json({ response: output });
    }

    // SCHEDULING
    if (lower.includes("schedule") || lower.includes("open home") || lower.includes("booking")) {
      const res = await fetch("http://127.0.0.1:8000/api/v1/agents/scheduling/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "inspection",
          data: { property_id: "prop_dashboard_demo" },
        }),
      });

      const data = await res.json();
      const slots = data?.result?.available_slots || [];
      if (Array.isArray(slots) && slots.length > 0) {
        const lines = slots.slice(0, 3).map((slot: any) =>
          `• ${slot.date}: ${(slot.times || []).join(", ")}`
        );
        return NextResponse.json({
          response: `Available open-home slots:\n${lines.join("\n")}`,
        });
      }

      return NextResponse.json({
        response: JSON.stringify(data?.result || data, null, 2),
      });
    }

    // RECENT CONTENT
    if (lower.includes("recent content") || lower.includes("show recent")) {
      const res = await fetch("http://127.0.0.1:8000/api/v1/enki/content/recent");
      const data = await res.json();

      if (Array.isArray(data?.items) && data.items.length > 0) {
        const lines = data.items.slice(0, 5).map((item: any, i: number) =>
          `${i + 1}. ${item.tone || "unknown"} tone at ${item.generated_at || "unknown time"}`
        );

        return NextResponse.json({
          response: `Recent content:\n${lines.join("\n")}`,
        });
      }

      return NextResponse.json({
        response: "Recent content is active, but no saved content entries were found yet.",
      });
    }

    // LEAD
    if (
      lower.includes("buyer") ||
      lower.includes("lead") ||
      lower.includes("qualify") ||
      lower.includes("sentiment") ||
      lower.includes("client")
    ) {
      let action = "respond";
      if (lower.includes("qualify")) action = "qualify";
      if (lower.includes("sentiment")) action = "analyze_sentiment";

      const res = await fetch("http://127.0.0.1:8000/api/v1/agents/lead/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action,
          data: {
            message: text,
            text,
            source: "dashboard",
            lead_id: "dashboard_lead",
            type: lower.includes("buyer") || lower.includes("looking for") ? "buying" : "general",
            budget: lower.includes("900000") ? 900000 : 0,
            timeline: lower.includes("1-3 month") || lower.includes("1-3 months") ? "1-3 months" : "",
            pre_approved: lower.includes("pre-approved") || lower.includes("pre approved"),
          },
        }),
      });

      const data = await res.json();
      const result = data?.result || {};

      if (action === "qualify") {
        return NextResponse.json({
          response:
            `Lead qualification:\n` +
            `• Qualified: ${result.qualified ?? "N/A"}\n` +
            `• Score: ${result.score ?? "N/A"}\n` +
            `• Priority: ${result.priority ?? "unknown"}`,
        });
      }

      if (action === "analyze_sentiment") {
        const sentiment = result.sentiment_analysis || {};
        return NextResponse.json({
          response:
            `Sentiment analysis:\n` +
            `• Sentiment: ${sentiment.sentiment ?? "unknown"}\n` +
            `• Urgency: ${sentiment.urgency ?? "unknown"}\n` +
            `• Recommended action: ${result.recommended_action ?? "none"}`,
        });
      }

      return NextResponse.json({
        response:
          result.response ||
          result.reply ||
          `Lead response:\n• Next step: ${result.next_step ?? "unknown"}\n• Priority: ${result.priority ?? "unknown"}`,
      });
    }

    // TRANSACTION
    if (
      lower.includes("transaction") ||
      lower.includes("compliance") ||
      lower.includes("checklist") ||
      lower.includes("risk") ||
      lower.includes("deadline") ||
      lower.includes("settlement")
    ) {
      let action = "checklist";
      if (lower.includes("compliance")) action = "compliance";
      if (lower.includes("risk")) action = "risk_assessment";
      if (lower.includes("deadline")) action = "track_deadline";
      if (lower.includes("milestone")) action = "milestone_status";

      const res = await fetch("http://127.0.0.1:8000/api/v1/agents/transaction/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action,
          data: {
            transaction_id: "txn_dashboard_demo",
            property_id: "prop_dashboard_demo",
            days_to_settlement: 10,
            finance_approved: false,
            building_report_complete: false,
            lawyer_assigned: true,
          },
        }),
      });

      const data = await res.json();
      const result = data?.result || {};

      if (action === "checklist") {
        const items = result.checklist || [];
        const lines = items.slice(0, 5).map((i: any) => `${i.completed ? "✅" : "⬜"} ${i.item}`);
        return NextResponse.json({
          response: `Transaction checklist:\n${lines.join("\n")}\nProgress: ${result.progress?.completion_percentage ?? "N/A"}%`,
        });
      }

      if (action === "compliance") {
        return NextResponse.json({
          response:
            `Compliance status:\n` +
            `• Compliant: ${result.compliant}\n` +
            `• Score: ${result.compliance_percentage}%`,
        });
      }

      if (action === "risk_assessment") {
        return NextResponse.json({
          response:
            `Risk assessment:\n` +
            `• Overall risk: ${result.overall_risk}\n` +
            `• High risks: ${result.high_risk_count}\n` +
            `• Medium risks: ${result.medium_risk_count}`,
        });
      }

      if (action === "track_deadline") {
        const deadlines = result.deadlines || [];
        const lines = deadlines.slice(0, 3).map((d: any) => `• ${d.task} (${d.days_remaining} days)`);
        return NextResponse.json({
          response: `Upcoming deadlines:\n${lines.join("\n")}`,
        });
      }

      return NextResponse.json({
        response: JSON.stringify(result, null, 2),
      });
    }

    return NextResponse.json({
      response:
        "I can help with workflows, property search, market trends, property descriptions, scheduling open homes, recent content, leads, or transaction support.",
    });
  } catch (e: any) {
    return NextResponse.json(
      {
        error: "AI proxy failed",
        detail: e?.message || "Unknown error",
      },
      { status: 500 }
    );
  }
}
