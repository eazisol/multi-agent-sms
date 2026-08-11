# MOD-220 Verification Evidence

**Date:** 2026-08-11  
**Human Done (AC-901):** NOT obtained

## Commands executed

| Check | Result |
|---|---|
| `uv run ruff check apps/api/src tests` | **passed** (after E501 fixes) |
| `uv run mypy apps/api/src/masms_api` | **passed** |
| `uv run pytest -q` | **64 passed** |
| `uv run alembic upgrade head` | **not run** (migration `20260811_0011` present) |

## Verified behaviors

- Conversation links to `related_entity_type` + `related_entity_id`
- Sensitive classification requires approval before send
- Draft body edits create revisions; sent bodies reject mutation
- Recipients and attachment links blocked after send
- Delivery receipts recorded for sent messages
