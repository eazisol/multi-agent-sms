# MOD-230 — Requirement Gathering, Completeness, Clarifications, Brief

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Run questionnaires, store structured answers, score completeness (≥95% mandatory), create owned clarifications for gaps, and approve versioned requirement briefs.

## M1 delivered

API: `/api/v1/requirements`  
Migration: `20260811_0012`

| ID | Entity |
|---|---|
| MP-001 | `req_questionnaires` |
| MP-002 | `req_questionnaire_versions` (published immutable) |
| MP-003 | `req_answers` |
| MP-004 | `req_requirement_briefs` (approved immutable / new version) |
| MP-005 | `req_clarification_requests` |
| MP-006 | `req_completeness_scores` |

## Dependency note

MOD-250 (files) and MOD-330 (approval gates engine) deferred; brief approval is local human-actor mark with completeness gate.

## Limits

- FE deferred; LangGraph gap analysis deferred
- Clarification Temporal waits deferred
- Full RBAC permission matrix pending broader access wiring
