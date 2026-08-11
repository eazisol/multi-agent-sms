# MOD-300 — Tickets, User Stories, Subtasks, Dependencies, Readiness, and Completion

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Create traceable work items with acceptance criteria, estimates, dependencies, Definition of Ready / Definition of Done checks, evidence, and controlled lifecycle including authorized reopen.

## M1 delivered

API: `/api/v1/tickets`  
Migration: `20260811_0016`

| ID | Entity |
|---|---|
| MP-001 | `tkt_tickets` |
| MP-002 | `tkt_subtasks` |
| MP-003 | `tkt_ticket_dependencies` |
| MP-004 | `tkt_requirement_links` |
| MP-005 | `tkt_ticket_evidence` |
| MP-006 | `tkt_readiness_checks` |
| MP-007 | `tkt_done_checks` |

## Acceptance highlights

- **AC-001:** Ready blocked until DoR fields + required readiness checks are satisfied
- **AC-002:** Tickets require project, phase (before Ready), owner or queue, and requirement link
- **AC-003:** Done reopen requires human actor, reason, and evidence

## Limits

- FE deferred
- Full board filters/pagination deferred (list by project only)
- Temporal assignment/escalation workflows deferred (local status transitions + outbox)
- MOD-310 assignment engine not integrated
