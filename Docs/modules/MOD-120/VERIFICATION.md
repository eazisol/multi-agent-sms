# MOD-120 Verification Evidence

**Date:** 2026-08-10  
**Human Done (AC-901):** NOT obtained

## Commands executed

| Check | Result |
|---|---|
| `uv run ruff check apps/api/src tests` | **passed** |
| `uv run mypy apps/api/src/masms_api` | **passed** |
| `uv run pytest -q` | **49 passed** |
| `uv run alembic upgrade head` | **not run** (SQLite-only verify; migration `20260810_0006` present) |

## Verified behaviors

- Deny-by-default permission checks until role grant exists  
- Project-scoped check fails without membership  
- Module / document / approval authority / access review APIs create successfully  

## Limits

- Postgres RLS not exercised in SQLite tests  
- Full actor permission loadout (without explicit role_id) deferred  
