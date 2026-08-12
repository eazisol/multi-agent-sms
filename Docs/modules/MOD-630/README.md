# MOD-630 Controlled Pilot, Production Release, Operations, and Final MVP Sign-Off (M1)

**Status:** M1 Done (human AC-901 approved 2026-08-12)  
**Human Done (AC-901):** Obtained 2026-08-12

## Scope delivered in M1

- Acceptance-test gate (`GET /pilot/acceptance-gate`) from recorded results. `gate_passed` is true only when no Critical or High tests are `failed` or `blocked`.
- Pilot-user approval gate (`GET /pilot/pilot-approval-gate`). `gate_passed` is true only when at least one registered user has `approved_production_use=true` and none remain pending.
- Cross-functional readiness gate (`GET /pilot/readiness-gate`) for `product`, `security`, `operations`, and `qa`. All four must be `signed` by a human actor.
- Production deployment `POST /pilot/deployments` persists a **record** with status `recorded` after all three gates pass and `human_approval_evidence` is non-empty. Agents cannot sign or record production deployments (409). This module does **not** perform a live production deploy.

## Backend components

- Module: `apps/api/src/masms_api/modules/pilot`
  - `models.py`: `pl_*` tables including supporting `pl_acceptance_tests`
  - `service.py`: plans, users, training, support, limitations, tests, sign-offs, deployment/rollback records, three gates, tenant RLS, audit, outbox
  - `router.py`: `/api/v1/pilot/*` endpoints
  - `domain.py`: `REQUIRED_SIGNOFF_FUNCTIONS`, `acceptance_gate_passed`, `pilot_approval_gate`, `readiness_gate`, `assert_human_signoff`, `assert_production_may_record`
  - `schemas.py`: transport contracts

## Frontend components

- Desk page route: `apps/web/src/app/pilot/page.tsx`
- Desk UI: `apps/web/src/components/pilot-desk-page.tsx`
- API helpers: `apps/web/src/lib/api.ts`
- Navigation entry: `apps/web/src/lib/navigation.ts` (`ready: true`)

## API endpoints (M1)

- `GET /api/v1/pilot/acceptance-gate`
- `GET /api/v1/pilot/pilot-approval-gate`
- `GET /api/v1/pilot/readiness-gate`
- `POST|GET /api/v1/pilot/plans`
- `GET /api/v1/pilot/plans/{id}`
- `POST|GET /api/v1/pilot/plans/{id}/users`
- `POST /api/v1/pilot/plans/{id}/users/{user_id}/approve`
- `POST|GET /api/v1/pilot/plans/{id}/training`
- `POST|GET /api/v1/pilot/plans/{id}/support`
- `POST|GET /api/v1/pilot/plans/{id}/limitations`
- `POST|GET /api/v1/pilot/plans/{id}/acceptance-tests`
- `POST /api/v1/pilot/plans/{id}/acceptance-tests/{test_id}/result`
- `POST|GET /api/v1/pilot/signoffs`
- `POST /api/v1/pilot/signoffs/{id}/sign`
- `POST|GET /api/v1/pilot/deployments`
- `POST /api/v1/pilot/deployments/{id}/rollback`

## Honesty / known limitations

- Production deployment is a persisted **record** only. Agents must not finalize production deployment; a human must supply evidence and perform any real release outside this API.
- Rollback is a recorded reason against a deployment record, not an automated infrastructure rollback.
- Training and support readiness are checklists, not live LMS or on-call systems.
- AC-901 obtained 2026-08-12 (human owner sign-off).
