# Agent Spawn & Management Protocol

**Purpose:** Prevent resource waste, timeouts, and data loss when delegating to sub-agents.

---

## Pre-Spawn Checklist

Before spawning any agent:
- [ ] **Define the deliverable** — What exact output is expected?
- [ ] **Estimate complexity** — Small task (<10 min), Medium (10-30 min), Large (30+ min)?
- [ ] **Set timeout** — Start conservative, scale with complexity
- [ ] **Checkpoint strategy** — How will progress be saved mid-task?

---

## Timeout Guidelines

| Task Type | Initial Timeout | Check-in Interval | Extension Rule |
|-----------|-----------------|-------------------|----------------|
| Quick research | 5-10 min | 5 min | +5 min if progress shown |
| Code review | 10-15 min | 8 min | +10 min if actively reviewing |
| Feature build | 20-30 min | 15 min | +15 min if structure visible |
| Large refactor | 30-45 min | 20 min | +20 min if progress logged |
| Complex multi-step | 45-60 min | 25 min | +30 min with checkpoint proof |

**Rule:** Never set timeout >60 min without mandatory checkpoints.

---

## Spawn Configuration Template

```javascript
sessions_spawn({
  task: "Clear, specific task description",
  runtime: "subagent", // or "acp" for Codex/Claude Code
  mode: "run",         // "run" = one-shot, "session" = persistent
  timeoutSeconds: XX,  // Conservative estimate
  streamTo: "parent",  // Watch output in real-time
  // For critical tasks, save checkpoint files:
  cwd: "/path/to/checkpoint/dir"
})
```

---

## Active Monitoring Protocol

1. **Poll at intervals** — Use `subagents(action: "list")` to check status
2. **Watch for stalls** — No output for >50% of timeout = likely stuck
3. **Check logs** — `sessions_history()` if agent seems slow
4. **Kill early if stuck** — Don't wait for timeout if clearly looping/failing

---

## Checkpoint Strategy (Critical for Long Tasks)

**Agents MUST write progress to disk periodically:**

```
// In agent task instructions, include:
"Save checkpoint files every 10 minutes to:
- progress.log (what's done)
- partial-results.json (intermediate data)
- errors.log (any issues encountered)"
```

**Recovery process if agent dies:**
1. Read checkpoint files
2. Resume from last saved state
3. Spawn new agent with remaining work only

---

## Post-Spawn Actions

| Status | Action |
|--------|--------|
| Completed successfully | Verify output, save to permanent location |
| Timeout | Check checkpoints, resume if salvageable |
| Error/Killed | Read logs, diagnose, decide retry or abort |
| Silent stall | Kill immediately, investigate logs |

---

## Red Flags — Kill Immediately

- No output for >10 min on simple task
- Repeated same error >3 times
- Memory/CPU spike without progress
- Output indicates wrong understanding of task

---

## Resource Protection Rules

1. **One major agent at a time** — Don't parallelize large tasks blindly
2. **Disk before network** — Save locally, then upload/push
3. **Git commits mid-task** — For code work, commit every checkpoint
4. **Log everything** — Agent output saved to `logs/YYYY-MM-DD-agent-task.log`

---

## Emergency Recovery

If agent dies with unsaved work:
1. Check `~/.openclaw/logs/` for session traces
2. Check workspace for any `.tmp` or `.partial` files
3. If no checkpoint exists → document failure, adjust protocol for next time

---

*Last updated: 2026-03-18*
