# MOD-250 Verification Evidence

**Date:** 2026-08-11  
**Human Done (AC-901):** NOT obtained

## Commands executed

| Check | Result |
|---|---|
| `uv run ruff check apps/api/src tests` | **passed** |
| `uv run mypy apps/api/src/masms_api` | **passed** |
| `uv run pytest -q` | **77 passed** |
| `uv run alembic upgrade head` | **not run** (migration `20260811_0014` present) |

## Verified behaviors

- Available version requires owner, effective date, and clean scan
- Infected scan quarantines and blocks availability/indexing
- Access-check enforces download/preview/extract/embeddings separately
