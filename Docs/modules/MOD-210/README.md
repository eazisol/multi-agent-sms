# MOD-210 — Client Queries, Qualification, and Opportunities

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Capture, classify, qualify, reject, convert, and trace client inquiries with original communication and qualification evidence.

## M1 delivered

API: `/api/v1/queries`  
Migration: `20260811_0010`

| ID | Entity |
|---|---|
| MP-001 | `crm_queries` (nullable `project_id`) |
| MP-002 | `crm_opportunities` |
| MP-003 | `crm_qualification_answers` |
| MP-004 | `crm_query_sources` |
| MP-005 | `crm_query_status_history` |
| MP-006 | first-response SLA fields on query |

## Limits

- FE deferred; Temporal SLA wait deferred (row fields only)
- Transition map is starter config in code (full cfg engine is MOD-140/MOD-320)
