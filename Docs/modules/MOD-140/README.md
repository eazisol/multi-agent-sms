# MOD-140 — Configuration Administration and Versioned Operational Rules

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Approved, versioned configuration of workflows, statuses, transitions, follow-ups, reminders, escalations, and approval workflows — without requiring a code deploy for rule changes.

## M1 delivered

API: `/api/v1/config`  
Migration: `20260811_0008`

| ID | Capability |
|---|---|
| MP-001…008 | workflows, statuses, transitions, follow-up/reminder/escalation rules, approval workflows, version lifecycle |
| AC-001 | Live transition check uses **effective** config only |
| AC-002 | approve / activate / rollback + audit |
| AC-003 | draft is editable only; cannot control live checks |

Lifecycle: `draft` → `approved` → `effective` (prior effective → `superseded`); rollback → `rolled_back` with optional restore.

## Limits

- FE deferred
- Template content catalog beyond approval steps JSON deferred
- Temporal reminder/escalation execution deferred (rules storage only)
