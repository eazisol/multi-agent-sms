# MOD-320 — Configurable Status and Transition Engine

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Execute configurable status transitions using effective MOD-140 configuration, with permissions/conditions (reason, approval), history, hold, reopen, and next-action snapshots. Business statuses are string codes — never DB enums.

## M1 delivered

API: `/api/v1/status-engine`  
Migration: `20260811_0018`

| ID | Entity |
|---|---|
| MP-001 | `wfe_workflow_bindings` (resolver) |
| MP-002 | Transition evaluator (runtime over `cfg_transition_rules`) |
| MP-003 | `wfe_status_history` |
| MP-004 | `wfe_holds` |
| MP-005 | `wfe_reopens` |
| MP-006 | `wfe_available_actions` |

## Acceptance highlights

- **AC-001:** Status codes are strings backed by effective config, not database enums
- **AC-002:** Every transition / initialize / reopen writes history and audit
- **AC-003:** Agents cannot skip transitions that require approval

## Limits

- FE deferred
- Temporal orchestration of waits deferred (MOD-350)
- Approval records themselves are not validated against MOD-330 yet (presence of `approval_id` required when rule says so)
