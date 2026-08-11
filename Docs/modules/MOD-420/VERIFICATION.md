# MOD-420 Verification

**Date:** 2026-08-11  
**Human Done (AC-901):** NOT obtained

## Commands

| Check | Command | Result |
|---|---|---|
| Alembic | `.\.venv\Scripts\python.exe -m alembic upgrade head` | passed (`20260811_0025 → 20260811_0026`) |
| Tests | `.\.venv\Scripts\python.exe -m pytest tests/integration/changecontrol -q --tb=short` | 1 passed |
| Integration suite | `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line` | 38 passed |
| OpenAPI | path count via `create_app().openapi()` | **269** (was 260; +9) |
| Meta | `GET /api/v1/meta` modules | includes `MOD-420` |
| Web build | `npm run build` (in `apps/web`) | passed (`/change-requests` in route table) |
| Alembic current | `.\.venv\Scripts\python.exe -m alembic current` | `20260811_0026 (head)` |

## Behaviors verified in tests

- Draft CR blocked from baseline update / development gate
- Impact → submit → approve → baseline version + ticket link
- Rejected CR preserves rationale and evidence
