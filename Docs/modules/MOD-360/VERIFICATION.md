# MOD-360 Verification

**Date:** 2026-08-11  
**Human Done (AC-901):** NOT obtained

## Commands

| Check | Command | Result |
|---|---|---|
| Alembic | `.\.venv\Scripts\python.exe -m alembic upgrade head` | passed (`20260811_0021 → 20260811_0022`) |
| Tests | `.\.venv\Scripts\python.exe -m pytest tests/integration/agents -q --tb=short` | 1 passed |
| Integration suite | `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line` | 34 passed |
| OpenAPI | path count via `create_app().openapi()` | **223** (was 210; +13) |
| Meta | `GET /api/v1/meta` modules | includes `MOD-360` |
| Web build | `npm run build` (in `apps/web`) | passed |
| Alembic current | `.\.venv\Scripts\python.exe -m alembic current` | `20260811_0022 (head)` |

## Behaviors verified in tests

- Definitions seed to 6 approved codes
- High-confidence stub run completes with model/prompt/sources
- Low-confidence run enters `review_required`; approve → `completed`
- Evaluation create succeeds
- Unknown `agent_code` rejected (422)
- Run list page shape includes `items` + `page`
