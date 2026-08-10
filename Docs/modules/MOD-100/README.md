# MOD-100 — Organizations, Actors, Human Users, Agents, Teams, and Departments

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Shared organization and actor model for ownership, reporting, escalation, approval, assignment, and audit.

## M1 delivered

| ID | Entity | Location |
|---|---|---|
| MP-001 | Organizations | `org_organizations` |
| MP-002 | Actors | `org_actors` |
| MP-003 | Human users | `org_human_users` |
| MP-004 | Agents | `org_agents` + supervisor rule |
| MP-005 | Roles | `org_roles` |
| MP-006 | Departments | `org_departments` |
| MP-007 | Teams | `org_teams` |
| MP-008 | Team members | `org_team_members` |
| MP-009 | Reporting lines | `org_reporting_lines` |

API prefix: `/api/v1/identity`  
Migration: `20260810_0004`

## Acceptance notes

- AC-002: creating an active agent requires an active human supervisor  
- AC-003: human and agent use distinct actor rows  

## Limits

- Auth0 user linking deferred to MOD-110  
- Full permission matrix deferred  
- FE admin screens deferred (see TEMPLATE_TASK_RATIONALE)
