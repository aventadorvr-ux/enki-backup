import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const { message } = await req.json();
    const lower = String(message || "").toLowerCase();

    let endpoint = "";
    let payload: any = {};

    if (lower.includes("trend") || lower.includes("market")) {
      endpoint = "/api/v1/agents/market_intel/process";
      payload = {
        action: "trends",
        suburb: "Auckland Central",
      };
    } else if (lower.includes("description") || lower.includes("listing")) {
      endpoint = "/api/v1/agents/content/process";
      payload = {
        action: "description_ai",
        bedrooms: 3,
        bathrooms: 2,
        location: "Auckland",
        features: ["modern", "garage"],
      };
    } else {
      return NextResponse.json({
        response: "I can help with market trends or property descriptions.",
      });
    }

    const res = await fetch("http://127.0.0.1:8000" + endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    const output =
      data?.result?.description ||
      data?.result?.ai_insights ||
      JSON.stringify(data, null, 2);

    return NextResponse.json({ response: output });
  } catch (e: any) {
    return NextResponse.json(
      { error: "AI proxy failed", detail: e?.message || "Unknown error" },
      { status: 500 }
    );
  }
}
