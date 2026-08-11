# MOD-340 — Bidirectional Follow-Ups, Reminders, SLA Pauses, and Escalations

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Track bidirectional clarifications and blockers with owner, deadline, rule version, reminders, escalations, parent-child return routing, SLA pauses, and closure evidence.

## M1 delivered

API: `/api/v1/follow-ups`  
Migration: `20260811_0020`

| ID | Entity |
|---|---|
| MP-001 | `flu_followups` |
| MP-002 | `flu_reminders` |
| MP-003 | `flu_escalations` |
| MP-004 | `flu_parent_child_links` |
| MP-005 | `flu_sla_pauses` |
| MP-006 | `flu_business_deadlines` |
| MP-007 | `flu_closure_evidence` |

## Acceptance highlights

- **AC-001:** Create requires owner, deadline, rule version, closure condition (+ required response)
- **AC-002:** `process-overdue` fires reminder and escalation when thresholds met
- **AC-003:** Parent-child links preserve `return_to_followup_id` / `return_route`

## Limits

- FE deferred
- Temporal scheduled waits deferred (MOD-350)
- Notification delivery deferred (MOD-440)
- Business-time calendar is weekday skip heuristic (not full MOD-130 calendar matrix)
