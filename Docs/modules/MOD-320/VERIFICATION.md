# MOD-320 Verification

**Date:** 2026-08-11  
**Human Done (AC-901):** NOT obtained

## Commands

| Check | Command | Result |
|---|---|---|
| Lint | `python -m ruff check apps/api/src/masms_api/modules/statusengine tests/unit/statusengine tests/integration/statusengine` | passed |
| Types | `python -m mypy apps/api/src/masms_api/modules/statusengine` | passed |
| Tests | `python -m pytest tests/unit/statusengine tests/integration/statusengine -q` | 9 passed |
| Full suite | `python -m pytest -q` | 104 passed |
| Alembic | `alembic upgrade head` | Not run against Postgres (SQLite tests) |

## Behaviors verified in tests

- Status codes are strings from effective config (AC-001)
- Transitions / init / reopen create history; mutations audited (AC-002)
- Agent cannot apply approval-gated transition even with approval_id (AC-003)
- Human without approval_id gets approval_required
- Hold blocks transitions until release; reopen from terminal with human + reason
