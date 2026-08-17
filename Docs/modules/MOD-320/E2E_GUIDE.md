# MOD-320 — Configurable Status and Transition Engine

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Learn why records move only through configured states. |
| QA | Test initialize, available actions, transition, hold, and reopen through OpenAPI. |
| Developer | Confirm effective configuration, audit, and string status behavior. |
| Owner | Confirm approval-gated transitions remain human controlled. |

## 2. What this module is

The status engine resolves an effective workflow configuration for an entity and evaluates allowed transitions. Status codes are configurable strings, not database enums.

In this company it means a ticket can show delivery actions, while the backend decides which move is legal and records who moved it, why, and under which rule.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/api/v1/status-engine` | **Implemented** | Bindings, states, actions, transitions, holds, reopen |
| Status/history/audit persistence | **Implemented** | Initialize and mutations write history |
| Dedicated status-engine desk | **Planned** | None found |
| Ticket delivery buttons | **Implemented** | `/tickets`; fixed ticket API flow, not a MOD-320 desk |
| Approval-id presence rule | **Implemented** | Approval record validity is not integrated with MOD-330 |
| Exact approval validation | **Planned** | Current engine checks presence where configured |
| Temporal wait orchestration | **Planned** | MOD-350 |
| Header identity | **Stubbed** | Not authentication |
| Human Done approval | **Blocked** | AC-901 not obtained |

## 4. Requirements and dependencies

- MOD-140 supplies effective status and transition configuration.
- A workflow binding connects entity type/project scope to that configuration.
- Approval-required transitions need a human and `approval_id`.
- Holds block transitions until released.
- Reopen requires a terminal state, human actor, and reason.

## 5. How to start

1. Start API/database and open `/docs`.
2. Prepare effective MOD-140 status/transition configuration.
3. Prepare an entity UUID and optional project UUID.
4. Use OpenAPI’s `status-engine` group.
5. Optionally observe `/tickets` for a business-facing transition UI.

## 6. Screens, buttons, and files

| Control | What it does | Status | Source file |
|---|---|---|---|
| Dedicated status-engine navigation | No route exists | Planned | — |
| Tickets → Prepare & mark Ready | Runs ticket readiness/transition API | Implemented adjacent UI | `tickets-desk-page.tsx` |
| Tickets → assigned … done | Requests ticket-local delivery transitions | Implemented adjacent UI | `tickets-desk-page.tsx` |
| OpenAPI **Try it out** | Enables API request entry | Implemented tooling | FastAPI OpenAPI |
| OpenAPI **Execute** | Sends request and displays response | Implemented tooling | FastAPI OpenAPI |

Do not describe ticket buttons as dynamic MOD-320 available actions: the current component renders a fixed sequence.

## 7. API, data, and automated tests

Router: [`router.py`](../../../apps/api/src/masms_api/modules/statusengine/router.py)  
Prefix: `/api/v1/status-engine`

| Method | Path | Purpose |
|---|---|---|
| POST/GET | `/bindings` | Create/list workflow bindings |
| GET | `/resolve` | Resolve workflow for entity type/project |
| POST | `/states` | Initialize state |
| GET | `/states/{type}/{id}` | Read current state |
| GET | `/states/{type}/{id}/history` | Read append-only history |
| GET | `/states/{type}/{id}/actions` | Evaluate available actions |
| POST | `/transitions` | Apply transition |
| POST | `/holds` | Place hold |
| POST | `/holds/{type}/{id}/release` | Release hold |
| POST | `/reopen` | Reopen terminal entity |

OpenAPI is authoritative for request fields.

Automated evidence:

- `tests/unit/statusengine/test_statusengine_domain.py`
- `tests/integration/statusengine/test_statusengine_api.py`
- `uv run pytest tests/unit/statusengine tests/integration/statusengine -q --tb=short`

## 8. Test flows

Capture configuration/binding IDs, state versions, actions, history, problem JSON, and audit/outbox references.

### F-SETUP

1. Create effective configured states and transition rules in MOD-140.
2. POST a binding for the test entity type.
3. GET `/resolve`; expect the intended workflow/rule version.
4. POST `/states`; expect initial configured string status and history.

### F-HAPPY

1. GET current state and `/actions`.
2. Choose an allowed non-gated action.
3. POST `/transitions` with entity, target action/status, reason fields required by schema, and current version.
4. Expect new status/version.
5. GET history; expect previous/next status, actor, rule, reason, timestamp.
6. Capture matching audit/outbox evidence.

### F-VALIDATE

1. Initialize with an unknown entity type or invalid initial status.
2. Apply a transition missing a required reason.
3. Expect validation/configuration problem JSON and no state mutation.

### F-AUTHZ

1. Use an agent actor on an approval-gated transition, even with `approval_id`.
2. Expect rejection.
3. Repeat with an unauthorized human.
4. Expect forbidden and unchanged history.

### F-TENANT

1. Read a known state with another organization header.
2. Resolve using another tenant’s project UUID.
3. Expect not-found/forbidden; do not expose configuration or history.

### F-CONCUR

1. Read the same state/version in two clients.
2. Transition client A.
3. Submit client B using stale version if exposed by the schema.
4. Expect conflict and one committed transition.

### F-TRANS

1. Request an action absent from `/actions`.
2. Attempt to skip an intermediate configured state.
3. Expect invalid transition and unchanged state/history.

### F-GATE

1. As a human, request an approval-gated transition without `approval_id`.
2. Expect `approval_required`.
3. Repeat with an ID; current implementation checks presence, not MOD-330 validity.
4. Mark end-to-end exact-version approval proof **Planned**, not passed.

### F-TERM

1. Move to a configured terminal state.
2. Normal transition must be blocked.
3. POST `/reopen` as human with reason; expect configured reopened state and history.
4. Agent or missing reason must be rejected.

### F-RECOVER

1. Place a hold with reason/responsible party/review data required by schema.
2. Attempt transition; expect blocked.
3. Release hold, then retry; expect normal evaluation.
4. No Temporal worker recovery is claimed.

### F-CLEAN

Leave the entity in an understandable state. Preserve bindings, holds, reopen rows, state history, and audit evidence.

## 9. Security, privacy, and approvals

- Tenant/project scope applies to state, config resolution, history, and actions.
- Deterministic backend rules—not UI—authorize transitions.
- Agents cannot perform approval-gated transitions.
- An arbitrary `approval_id` is not proof of MOD-330 exact-version approval today.
- Production workflow configuration changes require authorized governance.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Dedicated configuration/runtime desk | Planned |
| Dynamic ticket buttons from `/actions` | Planned |
| MOD-330 approval-record validation | Planned |
| Durable waits/timers | Planned |
| Browser E2E | Planned |

## 11. Related journeys

- MOD-140 defines effective configuration.
- MOD-300 presents ticket lifecycle actions.
- MOD-330 owns exact-version human approval.
- MOD-350 will coordinate durable waits.

## 12. Pass / fail checklist

- [ ] Binding resolves effective workflow
- [ ] Initial status is a configured string
- [ ] Available actions reflect current state
- [ ] Valid transition records full history
- [ ] Invalid transition does not mutate
- [ ] Hold blocks until release
- [ ] Agent cannot use approval-gated transition
- [ ] Missing approval id blocks human
- [ ] Terminal reopen requires human reason
- [ ] Cross-tenant state/history is hidden
- [ ] Exact approval integration marked Planned
- [ ] Automated result recorded
