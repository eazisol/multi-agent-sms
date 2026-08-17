# MOD-350 — Workflow Orchestrator Registry

> **Implementation update (2026-08-17):** Local Compose now provides Temporal and its UI,
> `LiveTemporalAdapter` handles start/signal/cancel, and `apps/temporal-worker` runs
> `masms.query_intake`. The adapter remains stubbed when `MASMS_TEMPORAL_ADDRESS` is unset;
> the other 11 catalog workflows are not yet live.

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Start and locate a workflow instance. |
| QA | Test catalog, filtering, idempotent signals, failure, and intervention APIs. |
| Developer | Verify PostgreSQL authority and stub adapter boundaries. |
| Owner | Confirm no claim of live Temporal durability is made. |

## 2. What this module is

This module stores approved workflow definitions, active versions, instances, signals, failures, and interventions. PostgreSQL holds authoritative state.

In this company it means a long-running business process has a traceable registry row, but the current M1 adapter only simulates Temporal run identifiers; no live worker executes the process.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/workflows` instance desk | **Implemented** | Start, status tabs, pagination |
| Orchestrator API | **Implemented** | Definitions, versions, instances, signals, failures, interventions |
| `TemporalAdapter` | **Stubbed** | `stub-{uuid}`; signal/cancel no-op |
| Live Temporal cluster/workers | **Planned** | Not exercised |
| Worker restart durability | **Blocked** | Cannot prove with stub |
| Instance detail/actions UI | **Planned** | List only |
| Header identity | **Stubbed** | Not authentication |
| Human Done approval | **Implemented record** | README says owner approved 2026-08-11 |

## 4. Requirements and dependencies

- Only 12 approved workflow catalog codes may start.
- Selected code needs an active version; service may seed/bootstrap per current behavior.
- Instance state lives in `orf_*` PostgreSQL tables.
- Signal idempotency uses instance plus idempotency key.
- Failures are append-only; interventions apply to non-terminal instances.

## 5. How to start

1. Start API/web and migrate PostgreSQL.
2. Open `/workflows`.
3. Optionally select a workspace project first.
4. Open `/docs` for version, signal, failure, and intervention actions absent from UI.
5. Treat every displayed Temporal run ID as stub evidence.

## 6. Screens, buttons, and files

Desk: [`workflows-desk-page.tsx`](../../../apps/web/src/components/workflows-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| Start instance | Opens form | Implemented | `workflows-desk-page.tsx` |
| Workflow code | Selects one approved catalog code | Implemented | `workflows-desk-page.tsx` |
| Related entity type/id | Binds instance; blank id generates UUID | Implemented | `workflows-desk-page.tsx` |
| Project id | Optional workspace scope | Implemented | `workflows-desk-page.tsx` |
| Start | Creates instance through stub adapter | Implemented + Stubbed runtime | `workflows-desk-page.tsx` |
| All/Running/Waiting/Failed/Completed/Cancelled | Filters instances | Implemented | `workflows-desk-page.tsx` |
| Pagination | Changes limit/offset | Implemented | `workflows-desk-page.tsx` |
| Instance row | Displays code/status/entity/stub run id | Implemented read-only | `workflows-desk-page.tsx` |
| Signal/cancel/intervene controls | No controls | Implemented API only | `router.py` |

## 7. API, data, and automated tests

Router: [`router.py`](../../../apps/api/src/masms_api/modules/orchestrator/router.py)  
Prefix: `/api/v1/orchestrator`

| Method | Path | Purpose |
|---|---|---|
| GET | `/definitions` | Approved catalog |
| POST/GET | `/definitions/{code}/versions`, `/versions` | Version registry |
| POST | `/versions/{id}/activate` | Activate version |
| POST/GET | `/instances` | Start/list |
| GET | `/instances/{id}` | Read |
| POST/GET | `/instances/{id}/signals` | Signal/list |
| POST/GET | `/instances/{id}/failures` | Fail/list |
| POST/GET | `/instances/{id}/interventions` | Create/list |
| POST | `/interventions/{id}/resolve` | Resolve |

Approved codes: `query_intake`, `requirement_clarification`, `project_handover`, `assignment_ack`, `blocker_resolution`, `qa_rejection_loop`, `client_status_report`, `change_request_flow`, `deployment_approval`, `project_closure`, `approval_gate_wait`, `followup_escalation`.

Test: `tests/integration/orchestrator/test_orchestrator_api.py`

```bash
uv run pytest tests/integration/orchestrator -q --tb=short
```

## 8. Test flows

Capture definition/version, instance/status, `stub-` run ID, signal/failure/intervention rows, audit, and outbox.

### F-SETUP

1. GET definitions; expect exactly the approved catalog codes.
2. Ensure selected code has an active version using OpenAPI if needed.
3. Open `/workflows`; choose **Start instance**.
4. **Expected:** form explicitly says stub Temporal run IDs.

### F-HAPPY

1. Select `query_intake`; enter related type/id and optional project.
2. Click **Start**.
3. Expect “Workflow instance started”, Running tab, and persisted row.
4. Confirm `temporal_run_id` starts `stub-`.
5. Filter All/Running and paginate.
6. This proves registry behavior only, not live Temporal execution.

### F-VALIDATE

1. Through API, start unknown `workflow_code`.
2. Expect 422/problem response and no instance.
3. Submit blank required related type in UI; browser blocks.

### F-AUTHZ

1. Attempt version activation/start/intervention as unauthorized actor.
2. Expect forbidden and no mutation.
3. UI currently does not role-hide **Start instance**; backend behavior is authoritative.

### F-TENANT

1. Read/list instance under another organization.
2. Expect not-found/forbidden.
3. Signals, failures, and intervention records must not leak.

### F-CONCUR

1. POST the same signal twice using one idempotency key.
2. Expect first applied; second response status `duplicate`.
3. Confirm only one signal row.

### F-TRANS

1. Attempt an unsupported status/intervention sequence on a terminal instance.
2. Expect invalid state.
3. Valid modeled states include pending/running/waiting/completed/failed/cancelled.

### F-GATE

1. Start `deployment_approval` or `project_closure` only as a registry test.
2. Do not treat starting as human approval or production authorization.
3. Required MOD-330 approval remains external and human-only.

### F-TERM

1. Use API to complete/cancel through supported intervention behavior.
2. Attempt new intervention on terminal instance.
3. Expect blocked; history/failures remain append-only.

### F-RECOVER

1. POST a failure; expect instance Failed and failure row.
2. Create/resolve an intervention using OpenAPI.
3. Expect configured resulting status.
4. This is database recovery logic, not a live worker restart test.

### F-CLEAN

Leave instances terminal or clearly labeled. Preserve signals, failures, interventions, audit, and outbox rows.

## 9. Security, privacy, and approvals

- Organization/project scope applies to instances and child records.
- Related IDs and payloads must not contain secrets.
- Starting high-risk workflow codes does not grant approval.
- Production deployment/rollback remains an authorized human action.
- Live Temporal availability and restart survival are unverified.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Live Temporal workers/cluster | Planned |
| Survive real worker restart | Blocked by stub runtime |
| Instance detail/actions UI | Planned |
| Search/code/project UI filters | API supports more than desk |
| Full Temporal operations UI | Planned |

## 11. Related journeys

- [J-AGENT](../../testing/CROSS_MODULE_JOURNEYS.md#j-agent-stub-agent-runtime-and-knowledge)
- Catalog also includes approval waits, follow-up escalations, QA loops, and deployment — all stub Temporal ids.

## 12. Pass / fail checklist

- [ ] Catalog contains only approved codes
- [ ] Start creates PostgreSQL instance
- [ ] Run ID is clearly `stub-`
- [ ] Status tabs and pagination work
- [ ] Unknown code is rejected
- [ ] Duplicate signal is idempotent
- [ ] Failure/intervention history persists
- [ ] Cross-tenant access is denied
- [ ] High-risk start does not imply approval
- [ ] No live Temporal claim made
- [ ] Automated result recorded
