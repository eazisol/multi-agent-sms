# Deep Audit (refresh) — MOD-000 through MOD-340

**Date:** 2026-08-11 (post toast / CORS proxy / pagination / multilevel scroll / LAN UUID)  
**Commit context:** through `7189880` on `main`  
**Question:** Are MOD-000…340 all working fine (backend, APIs, DB, frontend)?  
**Answer:** **Backend M1 remains largely green; ready desks are stronger than the prior refresh; product is still not production “fully working.”** Auth is a header stub; RLS not proven in CI; every module **AC-901** remains **blocked** (human Done). Agents must not claim AC-901 complete.

## Verification commands run (this refresh)

| Check | Result |
|---|---|
| `pytest -q` | **119 passed**, 1 Starlette/`httpx` deprecation warning |
| OpenAPI paths | **200** |
| `npm run build` (apps/web) | **passed** |
| `alembic heads` | `20260811_0020` |
| `alembic current` (connected Postgres) | **`20260811_0020 (head)`** — live DB matches head in this environment |
| Postgres RLS policies / cross-tenant tests | **not run in CI** |
| Auth0 / bearer production auth | **not wired** (header stub) |

## Progress since prior audit (`ff01fdc`)

| Area | Status |
|---|---|
| Browser → API CORS on localhost | mitigated via Next rewrite proxy + widened CORS; LAN still may use direct IP |
| Global Sonner toasts | shipped; replace inline success/error on desks |
| Collection list `{ items, page: PageMeta }` | queries, projects, documents, comms, requirements, approvals, follow-ups, tickets (+ clients/baselines already) |
| Desk pagination + filters | ready desks use `ListPagination` + server filters |
| Multilevel scroll shell | `AppShell` `h-dvh` + sidebar/main scroll; ready split desks use `fill` + `ScrollRegion` |
| Full-width tables | Clients, baselines, projects requirements, requirements briefs |
| LAN non-secure HTTP | `crypto.randomUUID` fallback (`newId`) |
| Queries desk UI polish | stronger inbox/detail hierarchy |
| Local Wi‑Fi hosting docs/scripts | updated separately (`a9a840e`) |

## Layer verdict

### Backend (FastAPI)

| Verdict | Detail |
|---|---|
| **Mostly working (M1)** | Routers in `main.py`: governance, observability, identity, auth, access, capacity, config, clients, queries, comms, requirements, projects, documents, roadmap, tickets, assignments, status-engine, approvals, follow-ups |
| Meta list | MOD-000,020,030,040,100–140,200–260,300–340 |
| Meta omission | MOD-010 toolchain not listed as a business module (expected) |
| Platform | MOD-030 helpers only |
| Kernel | Outbox enqueue + relay stub; SNS/SQS consumer deferred (MOD-500) |

### APIs

| Verdict | Detail |
|---|---|
| **Strong create/action + paged collection GETs** | OpenAPI **200** paths |
| List contract | Kernel shape `{ items, page: { limit, offset, total, has_more } }` on ready-desk collections (default limit 20, max 100) |
| Follow-ups | `GET /follow-ups` defaults `status=open`; `status=all` skips status filter |
| Tickets | Paged list under `GET /tickets/projects/{project_id}` with `q`/`status` |
| Approvals | Paged `GET /approvals` with `status`/`action_code`/`q` |
| API-first / no ready desk | Identity, Auth, Access, Capacity, Config, Assignments, Status engine |

### Database

| Fact | Detail |
|---|---|
| Alembic chain | `20260810_0001` … `20260811_0020` |
| This environment | `alembic current` = **head** on Postgres |
| CI / shared gate | Integration tests still primarily **SQLite memory + `create_all`** — not Alembic-against-Postgres in pytest |
| Risk | **RLS and cross-tenant isolation unproven in automated suite** |
| Web visibility | Default org/actor headers — other orgs’ data will not appear |

### Frontend

| Ready desk (`ready: true`) | Collection from API | UX notes (this refresh) |
|---|---|---|
| `/` Dashboard | Yes — KPIs via `page.total` | Toasts on partial failures |
| `/clients` | Yes | Server `q`/`status`, pagination, full-width table |
| `/queries` | Yes | Filters + pagination + fill split scroll + polished inbox |
| `/comms` | Yes | Fill split scroll |
| `/projects` | Yes | Fill split + requirements table scroll |
| `/requirements` | Yes | Fill split + briefs table |
| `/roadmap` | Yes | Fill 2-column scroll |
| `/tickets` | Yes | Fill split; project-scoped |
| `/documents` | Yes | Fill split |
| `/follow-ups` | Yes | Fill split; status open/closed/all |
| `/approvals` | Yes | Fill split; role gates for approve |
| `/governance/baselines` | Yes | Filters + pagination + full-width table |

FE still `ready: false` (placeholders): My Work, Inbox, Opportunities, Test Cases, Bugs, Agents, Agent Runs, Knowledge, Releases, Deployments, ADRs, CRs, Audit Logs UI, Users, Roles, Capacity, Workflows, Integrations, Notifications, Security.

## Module scorecard (honest)

| Module | Backend M1 | Migrate | API tests | FE desk | E2E “works fine”? |
|---|---|---|---|---|---|
| MOD-000 Governance | yes | yes | yes | baselines | **partial** (AC-901 blocked) |
| MOD-020 Kernel | yes | outbox | unit + relay | n/a | **partial** (broker deferred) |
| MOD-030 Platform | helpers | no tables | unit | n/a | **partial** |
| MOD-040 Observability | yes | yes | yes | no ready desk | **partial** |
| MOD-100 Identity | yes | yes | yes | soon | **API-only in UI** |
| MOD-110 Auth | yes | yes | yes | soon | **header stub, not Auth0** |
| MOD-120 Access | yes | yes | yes | soon | **API-only in UI** |
| MOD-130 Capacity | yes | yes | yes | soon | **API-only in UI** |
| MOD-140 Config | yes | yes | yes | soon | **API-only in UI** |
| MOD-200 Clients | yes | yes | yes | ready | **mostly** |
| MOD-210 Queries | yes | yes | yes | ready | **mostly** |
| MOD-220 Comms | yes | yes | yes | ready | **mostly** |
| MOD-230 Requirements | yes | yes | yes | ready | **mostly** |
| MOD-240 Projects | yes | yes | yes | ready | **mostly** |
| MOD-250 Documents | yes | yes | yes | ready | **mostly** |
| MOD-260 Roadmap | yes | yes | yes | ready | **mostly** |
| MOD-300 Tickets | yes | yes | yes | ready | **mostly** (project-scoped) |
| MOD-310 Assignments | yes | yes | yes | n/a | **API-only** |
| MOD-320 Status engine | yes | yes | yes | n/a | **API-only** |
| MOD-330 Approvals | yes | yes | yes | ready | **mostly** |
| MOD-340 Follow-ups | yes | yes | yes | ready | **mostly** (create may use demo `rule_version_id`) |

## Remaining gaps (priority)

1. **P0** Header-only auth / spoofable org-actor (not Auth0)  
2. **P0** RLS + cross-tenant automation not in CI (live `alembic current` is not a substitute)  
3. **P1** AC-901 human Done blocked on every module (intentional)  
4. **P1** No ready FE for Identity/Auth/Access/Capacity/Config/Assignments/Status engine  
5. **P1** Follow-ups create synthetic rule version when no effective config  
6. **P1** Dev DX: `.next` chunk misses (`627.js`) when build/dev collide — operational hazard  
7. **P2** Outbox SNS/SQS consumer (MOD-500)  
8. **P2** Temporal / notifications platform items deferred by design  
9. **P2** Placeholder nav modules ahead of their MOD waves  

## Conclusion

**Yes for “M1 backend + SQLite API tests + OpenAPI + ready-desk wiring + paging/toast/scroll UX are largely sound in this repo state.”**  
**No for “all MOD-000…340 fully working in a production / multi-tenant / Auth0 sense.”**

Treat checklist `done` as **M1 implementation claimed**, not production sign-off. **AC-901** remains blocked everywhere.
