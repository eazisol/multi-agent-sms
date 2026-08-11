# MOD-420 — Risks, Issues, Change Requests, Impact Analysis, and Baseline Updates

**Status:** M1 Done (human AC-901 approved 2026-08-11)
**Human Done (AC-901):** Obtained 2026-08-11

## Purpose

Govern out-of-scope work via risks, change requests, impact analysis, human approvals, and baseline/ticket version updates.

## Honesty (M1 limits)

- Baseline updates are recorded as links/version bumps — does not mutate MOD-000/240 artifact rows itself.
- FE is list + create/submit/approve/reject + development-gate — not a full CAB studio.
- Notifications / Temporal / LangGraph wiring deferred.
- AC-901 obtained 2026-08-11 (human owner sign-off).

## M1 delivered

API: `/api/v1/change-control`  
Migration: `20260811_0026`  
FE: `/change-requests`

| ID | Entity |
|---|---|
| MP-001 | `cc_risks` |
| MP-002 | `cc_risk_reviews` |
| MP-003 | `cc_change_requests` |
| MP-004 | `cc_impact_analyses` |
| MP-005 | `cc_change_approvals` |
| MP-006 | `cc_baseline_updates` |

## Acceptance behavior (M1)

- **AC-001:** Development gate + baseline updates require `approved` status
- **AC-002:** Approved CR can record artifact `to_version` and linked `ticket_id`
- **AC-003:** Rejected/deferred decisions keep rationale + evidence on CR and approval rows

## Key outbox events

`changecontrol.risk.created`, `.cr.created`, `.cr.submitted`, `.cr.approved|rejected|deferred`, `.baseline.updated`
