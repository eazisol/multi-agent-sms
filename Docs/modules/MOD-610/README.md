# MOD-610 Performance, Reliability, Idempotency, Resilience, and Disaster Recovery (M1)

**Status:** M1 Done (human AC-901 approved 2026-08-12)  
**Human Done (AC-901):** Obtained 2026-08-12

## Scope delivered in M1

- API SLO gate (`GET /reliability/api-slo`) computed from the latest recorded performance-test p95 (or samples). `slo_met` is true only when p95_ms ≤ 2000.
- Dashboard SLO gate (`GET /reliability/dashboard-slo`) from the latest/active dashboard p95. `slo_met` is true only when dashboard_p95_ms ≤ 3000.
- Workflow replay registry with idempotency keys: fail → resume → complete, duplicate key 409.
- Registries for resilience tests, index reviews, integration failure tests, and DR runbooks.

## Backend components

- Module: `apps/api/src/masms_api/modules/reliability`
  - `models.py`: `rlb_*` tables (prefix avoids clash with releases `rl_*`)
  - `service.py`: SLO computation, replay state machine, DR approve, tenant RLS, audit, outbox
  - `router.py`: `/api/v1/reliability/*` endpoints
  - `domain.py`: `API_P95_BUDGET_MS`, `DASHBOARD_P95_BUDGET_MS`, replay transitions
  - `schemas.py`: transport contracts

## Frontend components

- Desk page route: `apps/web/src/app/reliability/page.tsx`
- Desk UI: `apps/web/src/components/reliability-desk-page.tsx`
- API helpers: `apps/web/src/lib/api.ts`
- Navigation entry: `apps/web/src/lib/navigation.ts` (`ready: true`)

## API endpoints (M1)

- `GET /api/v1/reliability/api-slo`
- `GET /api/v1/reliability/dashboard-slo`
- `POST|GET /api/v1/reliability/performance-tests`
- `POST|GET /api/v1/reliability/resilience-tests`
- `POST|GET /api/v1/reliability/index-reviews`
- `POST|GET /api/v1/reliability/slo-dashboards`
- `POST|GET /api/v1/reliability/replays`
- `POST /api/v1/reliability/replays/{id}/fail`
- `POST /api/v1/reliability/replays/{id}/resume`
- `POST /api/v1/reliability/replays/{id}/complete`
- `POST|GET /api/v1/reliability/integration-failure-tests`
- `POST /api/v1/reliability/integration-failure-tests/{id}/recover`
- `POST|GET /api/v1/reliability/dr-runbooks`
- `POST /api/v1/reliability/dr-runbooks/{id}/approve`

## Honesty / known limitations

- No live load tests or k6 runs are executed in M1; SLO values are recorded measurements, not observed production latency.
- Workflow replay is a registry and status machine. Temporal resume/replay remains a stub.
- DR runbooks are documents. They are not executed disaster-recovery procedures.
- AC-901 obtained 2026-08-12 (human owner sign-off).
