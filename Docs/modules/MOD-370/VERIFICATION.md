# MOD-370 Verification

**Date:** 2026-08-11  
**Human Done (AC-901):** NOT obtained

## Commands

| Check | Command | Result |
|---|---|---|
| Alembic | `.\.venv\Scripts\python.exe -m alembic upgrade head` | passed (`20260811_0022 → 20260811_0023`) |
| Tests | `.\.venv\Scripts\python.exe -m pytest tests/integration/knowledge -q --tb=short` | 1 passed |
| Integration suite | `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line` | 35 passed |
| OpenAPI | path count via `create_app().openapi()` | **234** (was 223; +11) |
| Meta | `GET /api/v1/meta` modules | includes `MOD-370` |
| Web build | `npm run build` (in `apps/web`) | passed (`/knowledge` in route table) |
| Alembic current | `.\.venv\Scripts\python.exe -m alembic current` | `20260811_0023 (head)` |

## Behaviors verified in tests

- Create item + version + activate → chunks created
- Search returns cited hits; unapproved draft excluded
- Conflict open + resolve
- Item list page shape includes `items` + `page`
