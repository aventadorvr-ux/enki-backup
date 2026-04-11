# TASK-REPORT.md

Use this exact structure when reporting meaningful work.

## Required fields

Task:
Start state:
Action taken:
Output path:
Changed files:
Heartbeat evidence:
Status: VERIFIED | UNVERIFIED | BLOCKED | FAILED
Next action:

## Rules

- If Output path is empty, status cannot be VERIFIED
- If Changed files is empty for a file-producing task, status cannot be VERIFIED
- If Heartbeat evidence is empty for a delegated/long-running task, status cannot be VERIFIED
- Never claim completion without evidence

## Enforcement

- Use the field names exactly as written.
- Do not replace the format with tables, prose summaries, or custom headings.
- If a field has no value, write: NONE
- Final status must be one of:
  VERIFIED
  UNVERIFIED
  BLOCKED
  FAILED
