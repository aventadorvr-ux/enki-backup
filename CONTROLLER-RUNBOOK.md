# CONTROLLER-RUNBOOK.md

## Purpose

Define exactly how the main controller must run delegated work.

## Controller workflow

1. Read the user task
2. Decide whether delegation is required
3. Break work into bounded sub-tasks
4. For each sub-task, define:
   - Task
   - Output path
   - Proof method
   - Heartbeat evidence path
   - Rollback path
5. Check readiness using READINESS-GATE.md
6. If any required field is missing, verdict = NOT READY
7. If ready, execute or delegate
8. Require TASK-REPORT.md output from each sub-task
9. Verify outputs before reporting completion
10. Mark overall task complete only if all required sub-tasks are VERIFIED

## Controller rules

- Never mark work done because “it probably happened”
- Never collapse UNKNOWN into VERIFIED
- Never treat silence as success
- Never accept a sub-task without proof requirements
- Never accept overnight work without readiness gate passing

## Minimum controller report

Task:
Delegated sub-agents:
Output paths:
Verified results:
Unverified items:
Blocked items:
Final status: VERIFIED | UNVERIFIED | BLOCKED | FAILED

## Recovery behavior

If a delegated task fails:
- report FAILED or BLOCKED
- include the missing evidence
- include the next corrective action
- do not claim partial planning as completion
