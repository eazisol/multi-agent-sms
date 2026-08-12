# MOD-440 Verification

**Date:** 2026-08-11  
**Human Done (AC-901):** Obtained 2026-08-12 (human owner sign-off)

## Commands

| Check | Command | Result |
|---|---|---|
| Alembic | `.\.venv\Scripts\python.exe -m alembic upgrade head` | passed (`20260811_0027 → 20260811_0028`) |
| Tests | `.\.venv\Scripts\python.exe -m pytest tests/integration/notifications -q --tb=short` | 1 passed |
| Integration suite | `.\.venv\Scripts\python.exe -m pytest tests/integration -q --tb=line` | 40 passed |
| OpenAPI | path count via `create_app().openapi()` | **292** (was 281; +11) |
| Meta | `GET /api/v1/meta` modules | includes `MOD-440` |
| Web build | `npm.cmd run build` (in `apps/web`) | prebuild blocked (port 3000 / `assert-dev-not-running`); `npx next build` **passed** (`/notifications` in route table) |
| Alembic current | `.\.venv\Scripts\python.exe -m alembic current` | `20260811_0028 (head)` |

## Behaviors verified in tests

- Idempotent create (409 on duplicate key)
- Preference mute of `system_alert` rejected (422)
- Fail ×3 → DLQ → replay → pending
