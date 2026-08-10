# MOD-010 Verification Evidence

**Date:** 2026-08-10  
**Human Done (AC-901):** NOT obtained

## Commands executed

| Check | Result |
|---|---|
| `docker info` | **passed** — Engine 29.6.1 |
| `docker compose up -d postgres redis` | **passed** — images pulled; both containers Up |
| `docker compose ps` | **passed** — postgres **healthy**, redis **healthy** |
| `uv run alembic upgrade head` | **passed** — `20260810_0001` (MOD-000 governance) |
| `uv run alembic current` | **passed** — `20260810_0001 (head)` |
| `uv sync` | passed (prior session) |
| `uv run ruff check apps/api/src tests` | passed (prior session) |
| `uv run mypy apps/api/src/masms_api` | passed (prior session) |
| `uv run pytest -q` | **10 passed** (prior session; SQLite smoke) |
| `npm --prefix apps/web run lint` | passed (prior session) |
| `npm --prefix apps/web run build` | passed (prior session) |
| `scripts/dev-check.ps1` | passed quality section (prior session) |

## Limitations

- GitHub Actions workflow exists but was not cloud-executed here (needs git remotes).  
- pnpm still blocked on this host; web uses npm.  
- Live Postgres RLS / CMP suites beyond alembic apply are not claimed as full QA Done.  
- MOD-010 AC-901 and MOD-000 AC-901 still require human owners.

## Artifacts

- `.github/workflows/ci.yml`  
- `.python-version`, `.nvmrc`  
- `docs/modules/MOD-010/README.md`  
- `docs/modules/MOD-010/TEMPLATE_TASK_RATIONALE.md`  
