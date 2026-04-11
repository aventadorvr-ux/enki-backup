# Session: 2026-04-05 08:36:07 UTC

- **Session Key**: agent:main:main
- **Session ID**: 730fc5e9-0500-4d39-b86a-70d4da60d2f9
- **Source**: telegram

## Conversation Summary

assistant: ✅ New session started · model: openrouter/moonshotai/kimi-k2.5
user: A new session was started via /new or /reset. Run your Session Startup sequence - read the required files before responding to the user. Then greet the user in your configured persona, if one is provided. Be yourself - use your defined voice, mannerisms, and mood. Keep it to 1-3 sentences and ask what they want to do. If the runtime model differs from default_model in the system prompt, mention the default model. Do not mention internal steps, files, tools, or reasoning.
Current time: Sunday, April 5th, 2026 — 8:25 PM (Pacific/Auckland) / 2026-04-05 08:25 UTC
assistant: Hey Adam — Enki.2.0 here, back online. 🗿

System's running smooth on Enki_888. What are we working on tonight?
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "81",
  "sender_id": "1395007336",
  "sender": "AJ CEO",
  "timestamp": "Sun 2026-04-05 20:25 GMT+12"
}
```

Sender (untrusted metadata):
```json
{
  "label": "AJ CEO (1395007336)",
  "id": "1395007336",
  "name": "AJ CEO",
  "username": "AJ_Drip"
}
```

What agents exist in this system and what rules govern how work must be verified? Do not infer.
assistant: Based on MEMORY.md, here are the **known agents** and the **verification rules**:

## Agents in System

| Agent | Purpose |
|-------|---------|
| **lead** | Lead qualification |
| **content** | Property descriptions |
| **scheduling** | Calendar + booking management |
| **market_intel** | Market analysis |
| **transaction** | Deal coordination |

## Verification Rules (Critical)

From Enki_888 rebuild — these are **non-negotiable**:

| Rule | Meaning |
|------|---------|
| **NO OUTPUT = FAILURE** | If an agent claims work but produces no output, it's a failure |
| **NO FILE CHANGE = NO WORK DONE** | No file modification means no actual work occurred |
| **NO HEARTBEAT = AGENT DEAD** | Missing heartbeat means the agent is not functioning |

## Response Requirements

All responses must distinguish:
- **VERIFIED** — confirmed by direct observation/output
- **UNVERIFIED** — claimed but not confirmed
- **UNKNOWN** — no information available

## Prohibited Behaviors

- Claiming progress without proof
- Assuming tasks are complete
- Inferring missing results

Source: MEMORY.md#L39-L58
