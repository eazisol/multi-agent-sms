# MOD-200 — Client and Contact Management

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Manage client organizations, contacts with explicit authority, project contacts, communication preferences, duplicate suggestions, and merge history.

## M1 delivered

API: `/api/v1/clients`  
Migration: `20260811_0009`

| ID | Entity |
|---|---|
| MP-001 | `crm_clients` |
| MP-002 | `crm_contacts` (+ authority_level, is_primary) |
| MP-003 | `crm_project_contacts` (soft project_id) |
| MP-004 | `crm_communication_preferences` |
| MP-005 | `crm_duplicate_suggestions` |
| MP-006 | `crm_merge_history` (snapshot preserved) |

## Acceptance

- AC-001: multiple contacts with distinct authority levels  
- AC-002: merge stores snapshot history  
- AC-003: org/client isolation + audit on create/merge  

## Limits

- FE deferred; auto duplicate detection heuristics deferred (manual suggestion create)
