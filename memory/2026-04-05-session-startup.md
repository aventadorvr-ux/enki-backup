# Session: 2026-04-05 08:47:37 UTC

- **Session Key**: agent:main:main
- **Session ID**: 4cb36c16-f935-4390-9c1a-5bafdbd18cdb
- **Source**: telegram

## Conversation Summary

assistant: ✅ New session started · model: openrouter/moonshotai/kimi-k2.5
user: A new session was started via /new or /reset. Run your Session Startup sequence - read the required files before responding to the user. Then greet the user in your configured persona, if one is provided. Be yourself - use your defined voice, mannerisms, and mood. Keep it to 1-3 sentences and ask what they want to do. If the runtime model differs from default_model in the system prompt, mention the default model. Do not mention internal steps, files, tools, or reasoning.
Current time: Sunday, April 5th, 2026 — 8:36 PM (Pacific/Auckland) / 2026-04-05 08:36 UTC
assistant: I'm back online, Adam. It's Enki.2.0 — Sunday evening, post-recovery. System's stable: Telegram path confirmed, backend running, memory indexed.

What are we working on?
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "86",
  "sender_id": "1395007336",
  "sender": "AJ CEO",
  "timestamp": "Sun 2026-04-05 20:36 GMT+12"
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

What reliability rules govern how you report work, and what makes an unattended task NOT READY? Do not infer.
assistant: **Reliability rules from RELIABILITY.md:**

**Core proof-of-work rules:**
- NO OUTPUT = FAILURE
- NO FILE CHANGE = NO WORK DONE
- NO HEARTBEAT = AGENT DEAD
- NO VERIFIED INPUT = NO VERIFIED START
- NO VERIFIED RESULT = TASK NOT COMPLETE

**What makes unattended work NOT READY:**
Missing any of these required elements:
- controller alive
- target task defined
- output path defined
- heartbeat path defined
- rollback path defined
- proof method defined

**Response discipline:**
Must always distinguish VERIFIED / UNVERIFIED / UNKNOWN / BLOCKED / FAILED — never collapse them.

Source: RELIABILITY.md
