# MOD-620 Synthetic Sample Projects, Agent Evaluation, End-to-End Acceptance, and UAT (M1)

**Status:** M1 Done (human AC-901 approved 2026-08-12)  
**Human Done (AC-901):** Obtained 2026-08-12

## Scope delivered in M1

- Sample-project gate (`GET /uat/sample-gate`) from three synthetic codes (`SAMPLE-A`, `SAMPLE-B`, `SAMPLE-C`). `gate_passed` is true only when all three have `workflow_status=passed`.
- Agent quality gate (`GET /uat/agent-quality`) from the latest recorded evaluation. `meets_target` is true only when `accuracy_pct` ≥ 80.
- Human-only acceptance of UAT evidence. Agent actors receive 409 (`ApprovalRequiredError`).
- Registries for seed scripts, expected decisions, E2E test results, and role-based UAT results.

## Backend components

- Module: `apps/api/src/masms_api/modules/uateval`
  - `models.py`: `ua_*` tables plus supporting `ua_sample_projects`
  - `service.py`: sample seed/pass/gate, agent quality, evidence accept, tenant RLS, audit, outbox
  - `router.py`: `/api/v1/uat/*` endpoints
  - `domain.py`: `SAMPLE_REQUIRED`, `AGENT_QUALITY_TARGET_PCT`, `assert_human_approval_only`
  - `schemas.py`: transport contracts

## Frontend components

- Desk page route: `apps/web/src/app/uat/page.tsx`
- Desk UI: `apps/web/src/components/uat-desk-page.tsx`
- API helpers: `apps/web/src/lib/api.ts`
- Navigation entry: `apps/web/src/lib/navigation.ts` (`ready: true`)

## API endpoints (M1)

- `POST /api/v1/uat/sample-projects/seed`
- `GET /api/v1/uat/sample-projects`
- `GET /api/v1/uat/sample-projects/{code}`
- `POST /api/v1/uat/sample-projects/{code}/pass`
- `GET /api/v1/uat/sample-gate`
- `GET /api/v1/uat/agent-quality`
- `POST|GET /api/v1/uat/seed-scripts`
- `GET /api/v1/uat/seed-scripts/{id}`
- `POST|GET /api/v1/uat/expected-decisions`
- `POST|GET /api/v1/uat/agent-evaluations`
- `POST|GET /api/v1/uat/e2e-tests`
- `POST|GET /api/v1/uat/role-uat`
- `POST|GET /api/v1/uat/acceptance-evidence`
- `POST /api/v1/uat/acceptance-evidence/{id}/accept`

## Honesty / known limitations

- Seed is a registry of three synthetic project codes, not a full production data seeder.
- E2E and role-UAT rows are recorded results, not Playwright or live browser runs.
- Agent evaluation scores are recorded measurements, not live model-quality jobs.
- AC-901 obtained 2026-08-12 (human owner sign-off).
