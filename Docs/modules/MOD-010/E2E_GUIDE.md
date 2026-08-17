# MOD-010 — Repository, Toolchain, and Local Development Environment

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | What to do here |
|---|---|
| First-time user | Clone/open the repo and start API + web. |
| QA | Confirm health endpoints and that desks load. |
| Developer | Run the same quality commands CI uses. |
| Owner | Confirm no real secrets are in the tree. |

## 2. What this module is

This is not a business desk. It is the **workshop**: Python, Node, Docker, env files, and CI so everyone runs the same stack.

If this module fails, no later E2E guide can be executed honestly.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| Docker Compose Postgres + Redis | Implemented | Dev password `masms_dev_only` is local-only |
| uv Python env + Alembic | Implemented | |
| FastAPI + Next.js local run | Implemented | Web may use port 3001 if 3000 is busy |
| GitHub Actions CI | Implemented | Requires a git remote to run in the cloud |
| pnpm as package manager | Stubbed / waived | Root `package.json` names pnpm; web install uses **npm** |
| Temporal / agent / integration workers | Placeholder folders | Not live workers |
| Production secrets | Blocked | Must not be placed in `.env` committed files |

## 4. Requirements and dependencies

- Requirements: Cursor Rules 010, 600–720
- Depends on: MOD-000 (governance docs exist; toolchain proceeded under a documented waiver)
- Downstream: every module

## 5. How to start

From the repository root:

```bash
docker compose up -d postgres redis
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn masms_api.main:app --app-dir apps/api/src --reload --port 8000
```

Second terminal:

```bash
cp apps/web/.env.example apps/web/.env.local
npm --prefix apps/web install
npm --prefix apps/web run dev
```

Optional helper: `powershell -File scripts/dev-check.ps1`

Open `http://127.0.0.1:8000/health/ready` then `http://localhost:3000`.

## 6. Screens, buttons, and files

No module-owned UI. After start, you should see the shared shell ([`app-shell.tsx`](../../../apps/web/src/components/app-shell.tsx)) and Dashboard.

| File | Why it matters |
|---|---|
| [`.env.example`](../../../.env.example) | API env template |
| [`apps/web/.env.example`](../../../apps/web/.env.example) | Web org/actor defaults and API origin |
| [`package.json`](../../../package.json) | `web:dev`, `web:lint`, `web:build` |
| [`pyproject.toml`](../../../pyproject.toml) | uv / pytest / ruff / mypy |
| [`.python-version`](../../../.python-version) | Python 3.12 |
| [`.nvmrc`](../../../.nvmrc) | Node 22 |
| [`docker-compose.yml`](../../../docker-compose.yml) | Postgres + Redis |
| [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml) | CI quality gate |
| [`scripts/dev-check.ps1`](../../../scripts/dev-check.ps1) | Local quality helper |

## 7. API, data, and automated tests

No business CRUD. Prove the platform:

| Check | How |
|---|---|
| Live | `GET http://127.0.0.1:8000/health/live` |
| Ready | `GET http://127.0.0.1:8000/health/ready` (needs DB) |
| OpenAPI | `http://127.0.0.1:8000/docs` |
| Web proxy | Browser `/api/...` rewrites to FastAPI |

```bash
uv run ruff check apps/api/src tests
uv run mypy apps/api/src/masms_api
uv run pytest -q
npm --prefix apps/web run lint
```

Do not record these as passed unless you ran them.

## 8. Test flows

### F-SETUP

Install Docker, Python 3.12, Node 22, uv. Copy env examples. **Do not** paste production secrets.

### F-HAPPY

1. `docker compose up -d postgres redis` — containers healthy.
2. `uv run alembic upgrade head` — no error.
3. Start uvicorn — `/health/ready` returns ready.
4. Start Next.js — Dashboard loads (empty data is OK).
5. Sidebar shows the sections from [`navigation.ts`](../../../apps/web/src/lib/navigation.ts).

### F-VALIDATE

1. Start API without Postgres. **Expected:** ready check fails; live may still pass.
2. Missing `.env` database URL. **Expected:** API cannot talk to Postgres.

### F-AUTHZ

N/A for toolchain. Secret files must stay uncommitted.

### F-TENANT

N/A.

### F-CONCUR

N/A.

### F-TRANS

N/A.

### F-GATE

Production deploy is **not** this module. See [MOD-030](../MOD-030/E2E_GUIDE.md) and [MOD-630](../MOD-630/E2E_GUIDE.md).

### F-TERM

Stop with Ctrl+C; `docker compose stop` if you are done. Data in local Postgres remains.

### F-RECOVER

If Next cache is corrupt, follow `apps/web/scripts` clean-cache helpers if present. Re-run `uv sync` after lockfile changes.

### F-CLEAN

Leave Compose running for the rest of the E2E day.

## 9. Security, privacy, and approvals

- Only `.env.example` belongs in git.
- Compose password is documented as **dev-only**.
- CI must not print secrets.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| pnpm workspace | npm for `apps/web` |
| Live Temporal/agent workers | Placeholder directories |
| Cloud CI on every machine | Needs GitHub remote |

## 11. Related journeys

- [J-LEARN](../../testing/CROSS_MODULE_JOURNEYS.md#j-learn-first-hour)

## 12. Pass / fail checklist

| Step | Result |
|---|---|
| Postgres + Redis up | |
| Migrations at head | |
| `/health/ready` OK | |
| Web dashboard loads | |
| No production secrets in repo | |
| Quality commands run (record output) | |
