# MOD-410 — Bug Lifecycle, QA Rejection, Development Reopen, and Retesting

**Status:** M1 Done (human AC-901 approved 2026-08-11)  
**Human Done (AC-901):** Obtained 2026-08-11

## Purpose

Track defects through reject/reopen, assignment, fix, retest, known-issue exception, and severity SLA — with a release gate for blocking bugs.

## Honesty (M1 limits)

- No live CI/deployer integration; release gate is advisory API for MOD-430+.
- FE is list + create + reject/reopen + release-gate snapshot — not a full defect studio.
- Notifications / Temporal / LangGraph wiring deferred.

## M1 delivered

API: `/api/v1/bugs`  
Migration: `20260811_0025`  
FE: `/bugs`

| ID | Entity |
|---|---|
| MP-001 | `bg_bugs` |
| MP-002 | `bg_links` |
| MP-003 | `bg_assignments` |
| MP-004 | `bg_fix_submissions` |
| MP-005 | `bg_retests` |
| MP-006 | `bg_known_issue_approvals` |
| MP-007 | `bg_severity_slas` |

## Acceptance behavior (M1)

- **AC-001:** Reject requires reason + evidence; reopen returns bug to `open`
- **AC-002:** `/bugs/release-gate` denies while unresolved critical/high (or `blocks_release`) without approved known-issue
- **AC-003:** History aggregates requirement/ticket/test/fix/retest/release links

## Key rules

- Assignments close prior open assignment rows
- Fix submission moves bug to `fixed`; retest pass → `verified`, fail → `in_fix`
- Outbox: `bug.created`, `.rejected`, `.reopened`, `.fix_submitted`, `.retested`
