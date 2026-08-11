# MOD-310 Verification

**Date:** 2026-08-11  
**Human Done (AC-901):** NOT obtained

## Commands

| Check | Command | Result |
|---|---|---|
| Lint | `python -m ruff check apps/api/src/masms_api/modules/assignments tests/unit/assignments tests/integration/assignments` | passed |
| Types | `python -m mypy apps/api/src/masms_api/modules/assignments` | passed |
| Tests | `python -m pytest tests/unit/assignments tests/integration/assignments -q` | 6 passed |
| Full suite | `python -m pytest -q` | 95 passed |
| Alembic | `alembic upgrade head` | Not run against Postgres (SQLite tests) |

## Behaviors verified in tests

- Assignment to non-member rejected (AC-001)
- Leave/unavailability blocks unless override + reason (AC-001/002)
- Acknowledge by assignee; reassignment records immutable history (AC-003)
- Recommendations ranked for project members
