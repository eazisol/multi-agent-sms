# MOD-000 — Project Governance, Source Baseline, and Change Control

**Requirement mapping:** MVP-NFR-010, SRS Change Control  
**Status:** Implementation draft — **not Done** (MOD-000-AC-901 human approval pending)  
**Owner:** PENDING

## Delivered in this change

1. Governance documentation under `docs/governance/`  
2. Minimal monorepo skeleton overlapping MOD-010 (`apps/`, `migrations/`, `tests/`, Compose)  
3. FastAPI governance API with ORM models, services, routes, Alembic revision  
4. Unit + SQLite API tests for transitions, human-only approve, immutability, idempotency, org filter  

## API surface (`/api/v1/governance`)

| Method | Path | Notes |
|---|---|---|
| POST/GET | `/baselines` | Source baseline register |
| GET/PATCH | `/baselines/{id}` | Detail / mutable update |
| POST | `/baselines/{id}/transitions` | Status transitions; approve = human only |
| POST/GET | `/requirement-mappings` | Requirement → module map |
| POST/GET | `/architecture-decisions` | ADRs |
| POST | `/architecture-decisions/{id}/transitions` | ADR status |
| POST/GET | `/change-requests` | Governance CRs (+ idempotency key) |
| POST | `/change-requests/{id}/transitions` | CR status |
| POST/GET | `/approvals` | Exact-version approval records |

Provisional auth headers (pre MOD-110): `X-Organization-Id`, `X-Actor-Id`, `X-Actor-Kind`, `X-Correlation-Id`.

## Local verification

```bash
uv sync
uv run pytest
uv run ruff check apps/api/src tests
uv run mypy
```

Postgres (optional for Alembic):

```bash
docker compose up -d postgres
# set MASMS_DATABASE_URL from .env.example
uv run alembic upgrade head
```

## Known limitations / deferred

| Item | Reason |
|---|---|
| Frontend MOD-000-FE-* | Deferred — no pnpm on host; Next.js app is placeholder only |
| Temporal / LangGraph / outbox / notifications | Not required for governance register MVP stub; MOD-350+ |
| Full RBAC + Postgres RLS tests | RLS SQL in migration; runtime session GUC + isolation suite deferred to MOD-120 |
| Auth0 / real sessions | Header stub only until MOD-110 |
| Named human approvers | PENDING (see `docs/governance/PENDING_DECISIONS.md`) |
| Marking module Done | Blocked on MOD-000-AC-901 |
| Git repository | Workspace not initialized as git repo yet |
| pnpm activation | Corepack EPERM on this host |

## Rollback

- Docs: revert `docs/governance/`  
- Schema: `alembic downgrade -1` (destroys governance tables)  
- Code: remove `apps/api` governance module and migration revision  

## Evidence references

- Tests: `tests/unit/governance/`, `tests/integration/governance/`  
- Migration: `migrations/versions/20260810_0001_mod000_governance.py`  
- ADRs: `docs/governance/adrs/`
