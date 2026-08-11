# MOD-340 Verification

**Date:** 2026-08-11  
**Human Done (AC-901):** NOT obtained

## Commands

| Check | Command | Result |
|---|---|---|
| Lint | `python -m ruff check apps/api/src/masms_api/modules/followups tests/unit/followups tests/integration/followups` | passed |
| Types | `python -m mypy apps/api/src/masms_api/modules/followups` | passed |
| Tests | `python -m pytest tests/unit/followups tests/integration/followups -q` | 7 passed |
| Full suite | `python -m pytest -q` | 118 passed |
| Alembic | `alembic upgrade head` | Not run against Postgres (SQLite tests) |

## Behaviors verified in tests

- Create rejects missing rule version when no effective config (AC-001)
- Overdue processing creates reminders and escalations (AC-002)
- Parent-child links set return routing; parent cannot close with open mandatory children (AC-003)
- SLA pause/resume and closure evidence required to close
