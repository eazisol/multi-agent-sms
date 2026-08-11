# Deep Audit (refresh) — MOD-000 through MOD-340

**Date:** 2026-08-11 (post desk/list hardening)  
**Question:** Are MOD-000…340 all working fine (backend, APIs, DB, frontend)?  
**Answer:** **Backend M1 is largely green; product is not “all working fine” end-to-end.** Ready UI desks now sync collections from APIs. Auth is still a header stub; Postgres/RLS/`alembic upgrade` are not proven in CI; every module **AC-901** remains **blocked** (human Done).

## Verification commands run (this refresh)

| Check | Result |
|---|---|
| `pytest -q` | **119 passed** |
| OpenAPI paths | **200** |
| `npm run build` (apps/web) | **passed** |
| Live Postgres `alembic upgrade head` + RLS | **not run** |
| Auth0 / bearer production auth | **not wired** (header stub) |

## Progress since first audit

Closed previously P0/P1 desk gaps:

| Gap | Status |
|---|---|
| Queries list + filters | fixed earlier |
| `GET /projects` + Projects desk inventory | fixed |
| `GET /comms/conversations` + Messages inbox | fixed |
| `GET /documents` + Documents library | fixed |
| Requirements questionnaires/answers/briefs reload | fixed |
| Approvals + Follow-ups FE desks | fixed (nav `ready: true`) |
| Dashboard live KPIs | fixed |
| Roadmap milestones reload | fixed (`GET …/milestones`) |
| Clients server-side `q` search | fixed |

## Layer verdict

### Backend (FastAPI)

| Verdict | Detail |
|---|---|
| **Mostly working (M1)** | Modules wired in `main.py`: MOD-000,020,030,040,100–140,200–260,300–340 |
| Meta omission | MOD-010 toolchain not listed |
| Platform | MOD-030 helpers only (no business tables/HTTP desk) |
| Kernel | Outbox enqueue + relay stub; SNS/SQS bridge deferred (MOD-500) |

### APIs

| Verdict | Detail |
|---|---|
| **Strong create/action + collection GETs for ready desks** | OpenAPI builds (**200** paths) |
| Collection lists in play | clients (`q`/`status`), queries, projects, documents, conversations, questionnaires, briefs, approvals, follow-ups (open), phases, milestones, tickets-by-project, baselines |
| API-first / no ready desk | Identity, Auth, Access, Capacity, Config, Assignments, Status engine (and later-phase modules) |

### Database

| Fact | Detail |
|---|---|
| Alembic chain | `20260810_0001` … `20260811_0020` (20 revisions covering MOD-000…340 table sets) |
| Test strategy | **SQLite memory + `create_all`** in integration fixtures — not Alembic-against-Postgres |
| Risk | **RLS and Postgres-specific behavior unproven in CI** |
| Web visibility | Hardcoded default org/actor headers — data in other orgs will not appear |

### Frontend (ready desks)

| Ready desk | Org collection from API? | Notes |
|---|---|---|
| `/` Dashboard | **Yes** | Live counts from projects/approvals/follow-ups/queries |
| `/clients` | **Yes** | Server `q` search + paging meta |
| `/queries` | **Yes** | Status / SLA filters |
| `/comms` | **Yes** | Conversation inbox |
| `/projects` | **Yes** | Inventory + workspace selection |
| `/requirements` | **Yes** | Questionnaires + briefs; links to `crm_query`/project |
| `/roadmap` | **Yes** | Phases + milestones; project picker |
| `/tickets` | **Yes** | Scoped by workspace/project |
| `/documents` | **Yes** | Library reload |
| `/follow-ups` | **Yes** | Open list + evidence/close |
| `/approvals` | **Yes** | Queue + decide (needs Approver/Admin role for approve) |
| `/governance/baselines` | **Yes** | List/filter strong |

FE still `ready: false` (placeholders): My Work, Inbox, Opportunities, Quality, AI Ops, Release, most Admin, ADRs, CRs, audit logs UI, etc.

## Module scorecard (honest)

| Module | Backend M1 | Migrate | API tests | FE desk | E2E “works fine”? |
|---|---|---|---|---|---|
| MOD-000 Governance | yes | yes | yes | baselines | **partial** (AC-901 blocked) |
| MOD-020 Kernel | yes | outbox | unit + relay | n/a | **partial** (broker deferred) |
| MOD-030 Platform | helpers | no tables | unit | n/a | **partial** |
| MOD-040 Observability | yes | yes | yes | no dedicated ready desk | **partial** |
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
| MOD-340 Follow-ups | yes | yes | yes | ready | **mostly** (open list; rule_version demo UUID on create) |

## Remaining gaps (priority)

1. **P0** Header-only auth / hardcoded org-actor (spoofable; not Auth0)  
2. **P0** Postgres RLS + `alembic upgrade head` not proven in CI  
3. **P1** AC-901 human Done blocked on every module (intentional)  
4. **P1** No dedicated FE for Identity/Auth/Access/Capacity/Config/Assignments/Status engine  
5. **P1** Follow-ups create uses synthetic `rule_version_id` when no effective config  
6. **P2** Outbox SNS/SQS consumer (MOD-500)  
7. **P2** Temporal / notifications platform items still deferred/n/a by design  
8. **P2** Admin/Quality/AI/Release nav placeholders ahead of their modules  

## Conclusion

**Yes for “M1 backend + SQLite tests + OpenAPI + ready desk wiring are largely sound.”**  
**No for “all MOD-000…340 fully working in production sense.”**

Treat checklist `done` as **M1 implementation claimed**, not production sign-off. Human **AC-901** remains blocked everywhere.
