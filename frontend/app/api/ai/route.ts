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
    if (lower.includes(suburb.toLowerCase())) {
      return suburb;
    }
  }

  return "Auckland Central";
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

export async function POST(req: Request) {
  try {
    const { message } = await req.json();
    const text = String(message || "");
    const lower = text.toLowerCase();

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
      const suburb = extractSuburb(text);
      const max_price = extractMaxPrice(text);
      const bedrooms = extractBedrooms(text);

      const body: any = { suburb };
      if (max_price) body.max_price = max_price;
      if (bedrooms) body.bedrooms = bedrooms;

      const res = await fetch("http://127.0.0.1:8000/api/v1/enki/property/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      const data = await res.json();
      const results = Array.isArray(data?.results) ? data.results : [];

      if (!results.length) {
        return NextResponse.json({
          response: `No matching properties found for ${suburb}${max_price ? ` under $${max_price}` : ""}${bedrooms ? ` with ${bedrooms} bedrooms` : ""}.`,
        });
      }

      const lines = results.slice(0, 5).map((p: any, i: number) => {
        return `${i + 1}. ${p.title} — $${p.price} — ${p.bedrooms} bed / ${p.bathrooms} bath`;
      });

      return NextResponse.json({
        response: `Found ${results.length} matching propert${results.length === 1 ? "y" : "ies"}:\n${lines.join("\n")}`,
      });
    }

    if (lower.includes("trend") || lower.includes("market")) {
      const suburb = extractSuburb(text);

      const res = await fetch("http://127.0.0.1:8000/api/v1/agents/market_intel/process", {
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
      const result = data?.result || {};

      const responseText =
        `${suburb} market update:\n` +
        `• Median price: $${result.median_price ?? "N/A"}\n` +
        `• Price change: ${result.price_change ?? "N/A"}%\n` +
        `• Inventory: ${result.inventory_level ?? "N/A"}\n` +
        `• Trend: ${result.trend ?? "N/A"}\n` +
        `• Insight: ${result.ai_insights ?? "No insight available."}`;

      return NextResponse.json({ response: responseText });
    }

    if (lower.includes("description") || lower.includes("listing")) {
      const location = extractSuburb(text);
      const bedrooms = extractBedrooms(text) ?? 3;
      const bathrooms = extractBathrooms(text);
      const tone = extractTone(text);

      const res = await fetch("http://127.0.0.1:8000/api/v1/agents/content/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action: "description_ai",
          bedrooms,
          bathrooms,
          location,
          tone,
          features: ["modern kitchen", "garage", "outdoor entertaining"],
        }),
      });

      const data = await res.json();
      const output =
        data?.result?.description ||
        data?.description ||
        "No description returned.";

      return NextResponse.json({ response: output });
    }

    if (lower.includes("schedule") || lower.includes("open home") || lower.includes("booking")) {
      const res = await fetch("http://127.0.0.1:8000/api/v1/agents/scheduling/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action: "inspection",
          property_id: "prop_dashboard_demo",
        }),
      });

      const data = await res.json();
      const slots = data?.result?.available_slots || [];

      if (Array.isArray(slots) && slots.length > 0) {
        const lines = slots.slice(0, 3).map((slot: any) => {
          return `• ${slot.date}: ${(slot.times || []).join(", ")}`;
        });

        return NextResponse.json({
          response: `Available open-home slots:\n${lines.join("\n")}`,
        });
      }

      return NextResponse.json({
        response: JSON.stringify(data?.result || data, null, 2),
      });
    }

    if (lower.includes("recent content") || lower.includes("show recent")) {
      const res = await fetch("http://127.0.0.1:8000/api/v1/enki/content/recent");
      const data = await res.json();

      if (Array.isArray(data?.items) && data.items.length > 0) {
        const lines = data.items.slice(0, 5).map((item: any, i: number) => {
          return `${i + 1}. ${item.tone || "unknown"} tone at ${item.generated_at || "unknown time"}`;
        });

        return NextResponse.json({
          response: `Recent content:\n${lines.join("\n")}`,
        });
      }

      return NextResponse.json({
        response: "Recent content is active, but no saved content entries were found yet.",
      });
    }



    // 6. Lead intelligence
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
      if (lower.includes("chat")) action = "respond";

      const res = await fetch("http://127.0.0.1:8000/api/v1/agents/lead/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
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
            pre_approved: lower.includes("pre-approved") || lower.includes("pre approved")
          }
        }),
      });

      const data = await res.json();
      const result = data?.result || {};

      let responseText = "";

      if (action === "qualify") {
        responseText =
          `Lead qualification:\n` +
          `• Qualified: ${result.qualified ?? "N/A"}\n` +
          `• Score: ${result.score ?? "N/A"}\n` +
          `• Priority: ${result.priority ?? "unknown"}`;
      } else if (action === "analyze_sentiment") {
        const sentiment = result.sentiment_analysis || {};
        responseText =
          `Sentiment analysis:\n` +
          `• Sentiment: ${sentiment.sentiment ?? "unknown"}\n` +
          `• Urgency: ${sentiment.urgency ?? "unknown"}\n` +
          `• Recommended action: ${result.recommended_action ?? "none"}`;
      } else {
        responseText =
          result.response ||
          result.reply ||
          `Lead response:\n• Next step: ${result.next_step ?? "unknown"}\n• Priority: ${result.priority ?? "unknown"}`;
      }

      return NextResponse.json({ response: responseText });
    }



    // 7. Transaction management
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
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action,
          data: {
            transaction_id: "txn_dashboard_demo",
            property_id: "prop_dashboard_demo",
            days_to_settlement: 10,
            finance_approved: false,
            building_report_complete: false,
            lawyer_assigned: true
          }
        }),
      });

      const data = await res.json();
      const result = data?.result || {};

      let responseText = "";

      if (action === "checklist") {
        const items = result.checklist || [];
        const lines = items.slice(0, 5).map((i: any) =>
          `${i.completed ? "✅" : "⬜"} ${i.item}`
        );

        responseText =
          `Transaction checklist:\n` +
          lines.join("\n") +
          `\nProgress: ${result.progress?.completion_percentage ?? "N/A"}%`;
      }

      else if (action === "compliance") {
        responseText =
          `Compliance status:\n` +
          `• Compliant: ${result.compliant}\n` +
          `• Score: ${result.compliance_percentage}%`;
      }

      else if (action === "risk_assessment") {
        responseText =
          `Risk assessment:\n` +
          `• Overall risk: ${result.overall_risk}\n` +
          `• High risks: ${result.high_risk_count}\n` +
          `• Medium risks: ${result.medium_risk_count}`;
      }

      else if (action === "track_deadline") {
        const deadlines = result.deadlines || [];
        const lines = deadlines.slice(0, 3).map((d: any) =>
          `• ${d.task} (${d.days_remaining} days)`
        );

        responseText =
          `Upcoming deadlines:\n` +
          lines.join("\n");
      }

      else {
        responseText = JSON.stringify(result, null, 2);
      }

      return NextResponse.json({ response: responseText });
    }

    return NextResponse.json({
      response:
        "I can help with property search, market trends, property descriptions, scheduling open homes, or showing recent content.",
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
