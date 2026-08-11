# Deep Audit — MOD-000 through MOD-340

**Date:** 2026-08-11  
**Question:** Are all modules fully working (backend, APIs, database, frontend)?  
**Answer:** **No — not end-to-end.** Backend M1 packages + migrations + tests are largely present; frontend “ready” desks are only partially wired to list APIs; Postgres/RLS and Auth0 are not verified in CI; every module AC-901 remains blocked.

## Verification commands run

| Check | Result |
|---|---|
| `pytest -q` | **119 passed** (after P0 list APIs) |
| OpenAPI paths | **195** |
| `npm run build` (apps/web) | **passed** |
| Live Postgres `alembic upgrade` + RLS | **not run** |
| Auth0 / bearer production auth | **not wired** (header stub) |

## Checklist hygiene vs reality

Checklist through MOD-340 shows **0 partials** after hygiene pass, but modules still roll up **Blocked** because **AC-901** (human Done) is blocked everywhere.

Treat checklist `done` as **M1 implementation claimed**, not “production-complete” or “human signed-off.”

---

## Layer verdict

### Backend (FastAPI domain services)

| Verdict | Detail |
|---|---|
| **Mostly working** | Packages exist for governance, identity, auth, access, capacity, configadmin, clients, queries, comms, requirements, projects, documents, roadmap, tickets, assignments, statusengine, approvalgates, followups + observability/kernel |
| Wired in `main.py` | MOD-000,020,030,040,100–140,200–260,300–340 |
| Meta omission | MOD-010 (toolchain) not listed |
| Platform | MOD-030 has no HTTP/DB package (secrets/env helpers only) |

### APIs

| Verdict | Detail |
|---|---|
| **Create/action APIs strong** | CRUD-lite + transitions dominate; OpenAPI builds (193 paths) |
| **Collection GETs uneven** | Strong: clients, queries, baselines, approvals, follow-ups, nested project reqs/phases/tickets |
| **Missing primary list GETs** | **projects**, **documents**, **comms conversations** (messages nested only) |

### Database

| Prefix | Present in models/migrations |
|---|---|
| `gov_`, `sys_`, `ops_`, `org_`, `auth_`, `cfg_` | yes |
| `crm_`, `com_`, `req_`, `prj_`, `doc_`, `pm_` | yes |
| `tkt_`, `asg_`, `wfe_`, `apr_`, `flu_` | yes |

| Risk | Detail |
|---|---|
| Tests use **SQLite memory + create_all** | Alembic path + **Postgres RLS not exercised** |
| Local data visibility | Web uses hardcoded org `…0001` / actor `…0101` — data in other orgs won’t show |

### Frontend

| Ready desk | Loads org collection from API? | Notes |
|---|---|---|
| `/` Dashboard | **No** | Mock KPIs |
| `/clients` | **Yes** | Search is client-side on first 50 |
| `/queries` | **Yes** | Fixed list+filters (`eb95c1a`) |
| `/comms` | **Yes** | Inbox list + thread |
| `/requirements` | **Yes** | Questionnaires + briefs from API; links to crm_query |
| `/projects` | **Yes** | Inventory + search; sets workspace project |
| `/documents` | **Yes** | Library + search; reload keeps selection |

FE `ready: false` while APIs exist: `/approvals`, `/follow-ups`, and many Phase 4+ placeholders.

---

## Module scorecard (honest)

| Module | Backend M1 | DB/migrate | API tests | FE desk | E2E “works fine”? |
|---|---|---|---|---|---|
| MOD-000 Governance | yes | yes | yes | baselines yes | **partial** (AC-901 blocked) |
| MOD-020 Kernel | yes | outbox yes | unit yes | n/a | **partial** (broker bridge deferred) |
| MOD-030 Platform | helpers only | no tables | unit only | n/a | **partial** |
| MOD-040 Observability | yes | yes | yes | no dedicated ready desk | **partial** |
| MOD-100 Identity | yes | yes | yes | soon | **API-only in UI** |
| MOD-110 Auth | yes | yes | yes | soon | **header stub, not Auth0** |
| MOD-120 Access | yes | yes | yes | soon | **API-only in UI** |
| MOD-130 Capacity | yes | yes | yes | soon | **API-only in UI** |
| MOD-140 Config | yes | yes | yes | soon | **API-only in UI** |
| MOD-200 Clients | yes | yes | yes | ready | **mostly** |
| MOD-210 Queries | yes | yes | yes | ready | **mostly** (post list fix) |
| MOD-220 Comms | yes | yes | yes | ready | **mostly** (inbox list wired) |
| MOD-230 Requirements | yes | yes | yes | ready | **mostly** (questionnaire/brief lists wired) |
| MOD-240 Projects | yes | yes | yes | ready | **mostly** (inventory list wired) |
| MOD-250 Documents | yes | yes | yes | ready | **mostly** (library list wired) |
| MOD-260 Roadmap | yes | yes | yes | ready | **partial** (project UUID gate) |
| MOD-300 Tickets | yes | yes | yes | ready | **partial** (project UUID gate) |
| MOD-310 Assignments | yes | yes | yes | n/a | **API-only** |
| MOD-320 Status engine | yes | yes | yes | n/a | **API-only** |
| MOD-330 Approvals | yes | yes | yes | soon | **API-only** |
| MOD-340 Follow-ups | yes | yes | yes | soon | **API-only** |

---

## Top gaps (severity)

1. **P0** Header-only auth / hardcoded org-actor (spoofable locally)  
2. ~~**P0** Missing `GET /projects`~~ **fixed** — list + get + Projects desk inventory  
3. ~~**P0** Missing `GET /comms/conversations`~~ **fixed** — list + Messages inbox  
4. ~~**P0** Missing `GET /documents`~~ **fixed** — list + get + Documents library  
5. **P0** Dashboard ready with mock data  
6. **P1** Clients search not server-backed  
7. ~~**P1** Requirements desk localStorage entity/version loss~~ **fixed** — questionnaire inventory, published version, answers, briefs reload from API; discovery links to `crm_query` / project  
8. **P1** Approvals & Follow-ups APIs unused by FE  
9. **P2** Milestone list not reloadable  
10. **P2** Postgres RLS / Alembic never proven in CI  

**P0 list follow-up (2026-08-11):** `list_projects`, `list_conversations`, `list_documents` (+ `get_project` / `get_document`) wired; desks load org collections with search; integration tests extended.
---

## Conclusion

**Backend + migrations + automated tests for MOD-000…340 M1 are largely in place and currently green (119 pytest).**  
**They are not all “working fine” as a product**—especially frontend readiness claims for Projects/Comms/Documents/Dashboard, auth stub, and unproven Postgres RLS.

Human **AC-901** remains blocked on every module.
