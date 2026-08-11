# MOD-400 Verification

**Date:** 2026-08-11  
**Human Done (AC-901):** NOT obtained

## Commands

| Check | Command | Result |
|---|---|---|
| Alembic | `.\.venv\Scripts\python.exe -m alembic upgrade head` | passed (`20260811_0023 → 20260811_0024`) |
| Tests | `.\.venv\Scripts\python.exe -m pytest tests/integration/testcases -q --tb=short` | 1 passed |
| Integration suite | `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line` | 36 passed |
| OpenAPI | path count via `create_app().openapi()` | **246** (was 234; +12) |
| Meta | `GET /api/v1/meta` modules | includes `MOD-400` |
| Web build | `npm run build` (in `apps/web`) | passed (`/test-cases` in route table) |
| Alembic current | `.\.venv\Scripts\python.exe -m alembic current` | `20260811_0024 (head)` |

## Behaviors verified in tests

- Create case + steps; draft cannot run; approve then run
- Suite + plan with environment/build
- Complete run with evidence tied to environment + build
- Coverage link + Must-Have summary; permission case counted
- Optimistic concurrency conflict on stale run complete
