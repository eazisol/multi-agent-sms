# MOD-240 — Projects, Requirements, Requirement Versions, and SRS Management

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Create project records with unique requirement IDs, versioned requirement statements, acceptance criteria, business rules, assumptions, constraints, and human-approved SRS baselines.

## M1 delivered

API: `/api/v1/projects`  
Migration: `20260811_0013`

| ID | Entity |
|---|---|
| MP-001 | `prj_projects` |
| MP-002 | `prj_requirements` (unique `requirement_code` per project) |
| MP-003 | `prj_requirement_versions` (approved immutable) |
| MP-004 | `prj_business_rules` |
| MP-005 | `prj_acceptance_criteria` |
| MP-006 | `prj_assumptions` |
| MP-007 | `prj_constraints` |
| MP-008 | `prj_srs_baselines` (authoritative only after human approve) |

## Dependency note

MOD-250 / MOD-330 deferred; local human-actor approval marks SRS authoritative.

## Limits

- FE deferred; full change-request (MOD-420) linkage deferred (change_reason text only)
- Document attachments deferred to MOD-250
