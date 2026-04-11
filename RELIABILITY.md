# RELIABILITY.md - Proof of Work Rules

## Core rules

- NO OUTPUT = FAILURE
- NO FILE CHANGE = NO WORK DONE
- NO HEARTBEAT = AGENT DEAD
- NO VERIFIED INPUT = NO VERIFIED START
- NO VERIFIED RESULT = TASK NOT COMPLETE

## Required reporting for any meaningful task

Every task report must include:

1. Task name
2. Start state
3. What was actually executed
4. Output path(s) or returned result
5. Changed file(s), if any
6. Current status: VERIFIED / UNVERIFIED / FAILED / BLOCKED
7. Next action

## Overnight / unattended work

Unattended work is NOT READY unless all are verified:

- controller alive
- target task defined
- output path defined
- heartbeat path defined
- rollback path defined
- proof method defined

If any of the above are missing, verdict must be: NOT READY

## Forbidden behaviors

- claiming work completed without evidence
- saying a task is done when only planning occurred
- implying agent activity without heartbeat or deliverable
- inferring success from silence
- hiding uncertainty

## Evidence hierarchy

Strongest to weakest:

1. output file / artifact
2. command output
3. service status
4. log line
5. memory note
6. inference

Use the strongest available evidence.

## Response discipline

Always distinguish:

- VERIFIED
- UNVERIFIED
- UNKNOWN
- BLOCKED
- FAILED

Never collapse them together.
