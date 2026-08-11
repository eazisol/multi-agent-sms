# MOD-240 Verification Evidence

**Date:** 2026-08-11  
**Human Done (AC-901):** NOT obtained

## Commands executed

| Check | Result |
|---|---|
| `uv run ruff check apps/api/src tests` | **passed** (after import sort) |
| `uv run mypy apps/api/src/masms_api` | **passed** |
| `uv run pytest -q` | **73 passed** |
| `uv run alembic upgrade head` | **not run** (migration `20260811_0013` present) |

## Verified behaviors

- Approved requirement versions require unique code + acceptance criteria
- Approved versions reject further AC/rule mutation
- New requirement versions after v1 require change_reason
- SRS becomes authoritative only after human approve
