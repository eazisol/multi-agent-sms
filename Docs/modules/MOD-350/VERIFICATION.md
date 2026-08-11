# MOD-350 Verification

**Date:** 2026-08-11  
**Human Done (AC-901):** Approved 2026-08-11 by workspace owner

## Commands

| Check | Command | Result |
|---|---|---|
| Alembic | `.\.venv\Scripts\python.exe -m alembic upgrade head` | passed (`20260811_0020 → 20260811_0021`) |
| Tests | `.\.venv\Scripts\python.exe -m pytest tests/integration/orchestrator -q --tb=short` | 1 passed |
| Integration suite | `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line` | 33 passed |
| OpenAPI | path count via `create_app().openapi()` | **210** (was 200; +10) |
| Web build | `npm run build` (in `apps/web`) | passed (`/workflows` in route table) |
| Alembic current | `.\.venv\Scripts\python.exe -m alembic current` | `20260811_0021 (head)` |
| Ruff | `ruff check` orchestrator + tests | passed |
| Mypy | `mypy apps/api/src/masms_api/modules/orchestrator` | passed |

## Behaviors verified in tests

- Definitions seed to 12 approved codes
- Create + activate version, start instance with stub Temporal run id
- Signal applied; duplicate idempotency key returns `status=duplicate` without a second row
- Failure marks instance `failed`; cancel intervention resolves to `cancelled`
- Unknown `workflow_code` rejected (422)
- Instance list page shape includes `items` + `page`
