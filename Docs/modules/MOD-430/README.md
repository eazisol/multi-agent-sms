# MOD-430 — Releases, Deployment Requests, Production Approval, Rollback, and Closure

**Status:** M1 Done (human AC-901 approved 2026-08-11)
**Human Done (AC-901):** Obtained 2026-08-11

## Purpose

Package release items, enforce production approval + backup evidence, record deployments/checks, rollback, and dual-acceptance closure.

## Honesty (M1 limits)

- No live deployer/CI; deployments and checks are recorded in PostgreSQL.
- FE is list + create/submit/approve — not a full release orchestration studio.
- Deployments nav remains separate placeholder; data lives under `/api/v1/releases`.
- AC-901 obtained 2026-08-11 (human owner sign-off).

## M1 delivered

API: `/api/v1/releases`  
Migration: `20260811_0027`  
FE: `/releases`

| ID | Entity |
|---|---|
| MP-001 | `rl_releases` |
| MP-002 | `rl_release_items` |
| MP-003 | `rl_deployments` |
| MP-004 | `rl_deployment_checks` |
| MP-005 | `rl_backup_confirmations` |
| MP-006 | `rl_migration_plans` |
| MP-007 | `rl_rollbacks` |
| MP-008 | `rl_completion_reports` |

## Acceptance behavior (M1)

- **AC-001:** Production deploy requires approved release + evidence + confirmed backup
- **AC-002:** Traceability summary covers requirement/ticket/test/bug/change/document links
- **AC-003:** Closure requires client + internal acceptance on completion report
