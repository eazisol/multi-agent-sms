# MOD-110 Verification Evidence

**Date:** 2026-08-10  
**Human Done (AC-901):** NOT obtained

## Commands executed

| Check | Result |
|---|---|
| `uv run ruff check apps/api/src tests` | **passed** |
| `uv run mypy apps/api/src/masms_api` | **passed** |
| `uv run pytest -q` | **43 passed** |
| `uv run alembic upgrade head` | **not run** (SQLite-only verification per request; migration `20260810_0005` present) |

## Verified behaviors

- Local session create returns opaque `sess_` token (hash stored only)
- Bearer principal resolves to session org/actor/assurance
- MFA verify raises assurance; step-up purpose reaches level 3
- Revoke requires MFA assurance and blocks further bearer use
- Duplicate pending invitation rejected
- Service identity returns secret once; hash persisted
- Auth0 provider remains fail-closed

## Limits

- Auth0 JWKS not enabled
- FE deferred
- Debug MFA codes only in local/test/development
- Postgres alembic apply not verified in this evidence file
