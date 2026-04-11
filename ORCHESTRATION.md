# ORCHESTRATION.md

## Purpose

Define how the main controller and sub-agents must operate.

## Roles

### Main controller
- receives the user task
- decides whether delegation is needed
- breaks work into bounded sub-tasks
- defines proof requirements
- checks heartbeat and outputs
- refuses to mark work done without evidence

### Sub-agents
- perform one bounded task each
- must have a defined task, output path, and proof method
- must not claim completion without evidence
- must report using TASK-REPORT.md format

## Delegation rules

A sub-agent task is valid only if all are defined:

- Task
- Output path
- Proof method
- Heartbeat evidence path
- Rollback path

If any are missing, task status = NOT READY

## Parallel execution policy

Parallel sub-agents are allowed only when:
- tasks are independent
- outputs do not overwrite each other
- each task has separate proof
- controller can verify each result independently

## Completion rules

Controller may mark overall task complete only if:
- every required sub-task is VERIFIED
- output paths exist where expected
- changed files or returned outputs are present
- no required sub-task is UNKNOWN / BLOCKED / FAILED

## Required final controller report

- Task
- Delegated sub-agents
- Output paths
- Verified results
- Unverified items
- Final status: VERIFIED / UNVERIFIED / BLOCKED / FAILED
