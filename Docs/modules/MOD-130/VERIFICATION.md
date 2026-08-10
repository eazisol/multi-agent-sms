# MOD-130 Verification Evidence

**Date:** 2026-08-10  
**Human Done (AC-901):** NOT obtained

## Commands executed

| Check | Result |
|---|---|
| `uv run ruff check apps/api/src tests` | **passed** |
| `uv run mypy apps/api/src/masms_api` | **passed** |
| `uv run pytest -q` | **52 passed** |
| `uv run alembic upgrade head` | **not run** (migration `20260810_0007` present) |

## Verified behaviors

- Skill / actor-skill / availability / allocation / calendar / holiday / leave / on-call create APIs  
- Assignment evaluation uses skill, capacity remaining, leave, calendar deadline  
- SLA business-day helper skips weekends and holidays and returns calendar timezone  
