# MOD-020 Verification Evidence

**Date:** 2026-08-10  
**Slice:** Full M1 (typed IDs through optimistic concurrency + outbox migration)  
**Human Done (AC-901):** NOT obtained

## Commands executed

| Check | Result |
|---|---|
| `uv run ruff check apps/api/src tests` | passed |
| `uv run mypy apps/api/src/masms_api` | passed |
| `uv run pytest -q` | **23 passed** |
| `uv run alembic upgrade head` | **passed** → `20260810_0002` |
| `docker compose` postgres/redis | **healthy** |

## Scope of this evidence

- `masms_api.kernel` (ids, actor, tenant, errors, uow, outbox, problem, pagination, concurrency)
- Governance wires UoW + shared helpers + outbox enqueue on baseline create
- Problem responses use `application/problem+json` with compat `message` field

## Not verified / remaining

- Outbox publisher relay to broker (rows stay `pending` until later module)
- Temporal/LangGraph enforcement beyond documentation
- Human AC-901  
