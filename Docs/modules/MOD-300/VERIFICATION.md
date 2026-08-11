# MOD-300 Verification

**Date:** 2026-08-11  
**Human Done (AC-901):** NOT obtained

## Commands

| Check | Command | Result |
|---|---|---|
| Lint | `python -m ruff check apps/api/src/masms_api/modules/tickets tests/unit/tickets tests/integration/tickets` | passed |
| Types | `python -m mypy apps/api/src/masms_api/modules/tickets` | passed |
| Tests | `python -m pytest tests/unit/tickets tests/integration/tickets -q` | 8 passed |
| Full suite | `python -m pytest -q` | 89 passed |
| Alembic | `alembic upgrade head` | Not run against Postgres in this change (SQLite tests) |

## Behaviors verified in tests

- Ready transition rejected until description, requirement link, AC, estimate, DoD, phase, owner/queue, and readiness checks are complete (AC-001)
- Ticket links to project, phase, owner, and requirement before Ready (AC-002)
- Done requires Passed QA + satisfied done checks
- Done reopen requires human actor, reason, and evidence (AC-003)
- Self-dependency rejected
- Subtasks and ticket dependencies can be created
