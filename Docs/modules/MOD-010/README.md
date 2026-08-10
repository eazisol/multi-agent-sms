# MOD-010 — Repository, Toolchain, and Local Development Environment

**Requirements:** Cursor Rules 010, 600–720  
**Dependencies:** MOD-000 (functional governance in progress; formal AC-901 still PENDING — proceeded under documented waiver for toolchain only)  
**Status:** Implementation draft — human Done (AC-901) PENDING  
**Version:** 0.1.0

## Purpose

Make a new developer able to clone/open the repo, install tools, start local dependencies, run API/web, and pass the same checks CI runs.

## Monorepo layout (MP-001)

```text
apps/
  api/                 FastAPI (uv package masms-api)
  web/                 Next.js (npm package @masms/web)
  temporal-worker/     placeholder (MOD-350)
  agent-worker/        placeholder (MOD-360)
  integration-worker/  placeholder (MOD-500+)
packages/              shared packages placeholder (MOD-020)
migrations/            Alembic
tests/                 unit/integration/...
docs/                  engineering docs (governance, modules)
Docs/                  product specifications (authoritative SRS/specs)
infrastructure/        deploy skeletons (MOD-030)
scripts/               generators + helper scripts
.github/workflows/     CI
```

## Language / package managers (MP-002, MP-003)

| Item | Pin | File |
|---|---|---|
| Python | 3.12 | `.python-version`, `requires-python` |
| Node.js | 22 | `.nvmrc`, `apps/web/package.json` engines |
| Python packages | uv + `uv.lock` | root `pyproject.toml` |
| Web packages | **npm** + `apps/web/package-lock.json` | pnpm preferred later; Corepack EPERM on this host |

## Local stack commands (AC-001)

```bash
# 1) Infra
docker compose up -d postgres redis

# 2) Python env
uv sync
cp .env.example .env

# 3) Migrations (Postgres must be healthy)
uv run alembic upgrade head

# 4) API
uv run uvicorn masms_api.main:app --app-dir apps/api/src --reload --port 8000

# 5) Web (separate terminal)
cp apps/web/.env.example apps/web/.env.local
npm --prefix apps/web install
npm --prefix apps/web run dev
```

Helper: `scripts/dev-check.ps1` / `scripts/dev-check.sh` run format-adjacent quality gates.

## Quality commands (MP-005…007, QA-005)

```bash
uv run ruff check apps/api/src tests
uv run mypy apps/api/src/masms_api
uv run pytest -q
npm --prefix apps/web run lint
npm --prefix apps/web run build
```

## CI (MP-008, AC-002)

GitHub Actions: `.github/workflows/ci.yml`  
Blocks on ruff, mypy, pytest, and Next.js lint/build.

## Secrets (AC-003)

- Only `.env.example` / `apps/web/.env.example` in VCS  
- Compose uses documented **dev-only** password `masms_dev_only` (local)  
- No production secrets in repo  

## Template task N/A rationale

MOD-010 is a **toolchain** module. Plan template rows for business DB/BE/API/FE/WF/SEC CRUD do not apply as product features. See `TEMPLATE_TASK_RATIONALE.md`.

## Acceptance

| ID | Status |
|---|---|
| MOD-010-AC-001 | Draft satisfied when commands above work on a clean machine |
| MOD-010-AC-002 | CI workflow present; requires GitHub + git remote to execute in cloud |
| MOD-010-AC-003 | No real secrets in tree (verified by review of examples) |
| MOD-010-AC-900 | No Critical/High tooling defects logged |
| MOD-010-AC-901 | **Blocked** — human owner approval required |
