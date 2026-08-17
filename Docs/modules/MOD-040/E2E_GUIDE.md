# MOD-040 — Observability, Audit Foundation, and Operational Health

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | View append-only audit events and check service health. |
| QA | Test pagination, redaction, tenant scope, deletion denial, and agent-run records. |
| Developer | Inspect observability routes, writers, migration, and relay limitations. |
| Owner | Confirm evidence cannot be deleted and transport/exporters are labeled honestly. |

## 2. What this module is

Observability explains whether MASMS is alive and records who did what. It provides health endpoints, operational audit/activity/status records, agent-run tracking, integration-event foundations, and correlation-aware tracing stubs.

In this company it means a tester can create an agent-run event, see a redacted audit entry for the active organization, and prove that the API refuses to delete that evidence.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/audit-logs` desk | Implemented | Read-only list and pagination |
| Audit/activity/status/agent-run tables and APIs | Implemented | Migration `20260810_0003` |
| Audit delete refusal | Implemented | Always forbidden |
| `/health/live`, `/health/ready` | Implemented | Readiness checks database |
| Secret redaction | Implemented | Nested payload fields |
| Outbox relay endpoint | Stubbed | Marks published; no broker |
| OpenTelemetry tracing/export | Stubbed | No real SDK exporter/Collector |
| Redis readiness | Stubbed | Configuration-aware only |
| MOD-460 traceability use of desk | Implemented reuse | Same `/audit-logs` page |
| Human Done AC-901 | Blocked | Not obtained |

## 4. Requirements and dependencies

- Complete [MOD-010](../MOD-010/E2E_GUIDE.md) and apply migrations.
- Desk: [`apps/web/src/app/audit-logs/page.tsx`](../../../apps/web/src/app/audit-logs/page.tsx), [`audit-logs-desk-page.tsx`](../../../apps/web/src/components/audit-logs-desk-page.tsx).
- API: [`observability/router.py`](../../../apps/api/src/masms_api/observability/router.py).
- Migration: [`20260810_0003_mod040_observability.py`](../../../migrations/versions/20260810_0003_mod040_observability.py).
- Tests: [`tests/unit/observability/`](../../../tests/unit/observability/), [`tests/integration/observability/`](../../../tests/integration/observability/).

## 5. How to start

1. Start the API and web using [MOD-010](../MOD-010/E2E_GUIDE.md).
2. Request `/health/live` and `/health/ready`.
3. Open **Governance → Audit Logs** or `http://localhost:3000/audit-logs`.
4. Use `/docs` for agent-run, activity, status-history, and relay routes not exposed in this desk.

## 6. Screens, buttons, and files

### Audit Logs — `/audit-logs`

| Control / state | What happens | Status | Source |
|---|---|---|---|
| Page heading | Shows “Audit Logs” and append-only description | Implemented | [`audit-logs-desk-page.tsx`](../../../apps/web/src/components/audit-logs-desk-page.tsx) |
| Loading rows | Skeleton while `listAuditLogs` runs | Implemented | same file |
| “No audit events” | Empty state; says org actions appear here | Implemented | same file |
| Event row | Action + entity type; UTC time, actor kind, 8-char entity ID | Implemented | same file |
| Pagination previous/next | Changes offset | Implemented | [`list-pagination.tsx`](../../../apps/web/src/components/list-pagination.tsx) |
| Items-per-page control | Changes limit; default 20 | Implemented | same file |
| Load failure toast | “Unable to load audit logs” | Implemented | desk + [`toast.ts`](../../../apps/web/src/lib/toast.ts) |
| Search/filter/detail/delete buttons | Not present | N/A | Do not invent them |

The shared header **Create**, bell, and **AI** are planned shell controls, not observability actions.

## 7. API, data, and automated tests

Prefix: `/api/v1/observability`

| Method | Path | Purpose |
|---|---|---|
| GET | `/audit-logs?limit=&offset=` | Organization-scoped audit page |
| DELETE | `/audit-logs/{audit_id}` | Always refuses mutation |
| GET | `/activity?limit=&offset=` | Activity page |
| GET | `/status-history?entity_type=&entity_id=&limit=&offset=` | Entity status history |
| POST | `/outbox/relay` | Local relay stub |
| POST | `/agent-runs` | Start run |
| POST | `/agent-runs/{run_id}/finish` | Finish run |
| GET | `/health/live` | Process liveness (outside API prefix) |
| GET | `/health/ready` | Dependency readiness (outside API prefix) |

Primary integration test: [`test_observability_api.py`](../../../tests/integration/observability/test_observability_api.py). It checks health, starts/finishes a run, verifies token redaction, and verifies delete returns `403`. [VERIFICATION.md](VERIFICATION.md) records an earlier 34-test full run and migration apply; rerun focused tests:

```bash
uv run pytest tests/unit/observability tests/integration/observability -q --tb=short
```

## 8. Test flows

### F-SETUP

1. Start services and open `/audit-logs`. **Expected UI:** skeleton then rows or “No audit events.” **Data:** organization-scoped query only. **Evidence:** screenshot and active org ID.
2. Keep a synthetic token value ready only for a redaction test.

### F-HAPPY

1. In `/docs`, POST `/agent-runs` with agent name and an `input_summary` containing synthetic `api_token`.
2. **Expected API:** `201`, run ID/status. Finish it with `succeeded`; expect `200`.
3. Refresh `/audit-logs`. **Expected UI:** event row(s), actor kind and shortened entity ID; no raw token.
4. Request audit API. **Expected data:** `payload_redacted.api_token == "[REDACTED]"`. **Evidence:** redacted JSON and screenshot.

### F-VALIDATE

1. Request limit `0`, over `100`, negative offset, or missing status-history query fields. **Expected:** validation problem response; no data mutation.
2. Finish an unknown run ID. **Expected:** not found problem.

### F-AUTHZ

1. Attempt DELETE on an existing audit ID. **Expected API:** `403`, code `forbidden`; UI has no delete control.
2. Test service authorization with an unauthorized context if policy fixtures exist. Do not infer that a hidden button proves backend authorization.

### F-TENANT

1. Create event in organization A, then list with organization B header.
2. **Expected UI/data:** A’s event is absent; direct ID operations do not reveal it. **Evidence:** two redacted responses.

### F-CONCUR

1. Finish the same agent run from two requests. Record actual deterministic result and final row.
2. No `expected_version` appears in these router contracts, so optimistic concurrency is **N/A**; duplicate-finish behavior must not corrupt audit history.

### F-TRANS

1. Finish a run with the allowed terminal status from tests. **Expected:** status changes once and audit/activity attribution is retained.
2. Invalid status values should fail schema/domain validation. Full run state-machine coverage is limited.

### F-GATE

N/A — this module records evidence but does not grant human approval. Audit presence is not approval.

### F-TERM

1. A finished agent run should remain inspectable. Attempt another invalid finish and record behavior.
2. Audit rows are append-only and have no reopen/delete path.

### F-RECOVER

1. Stop the database and call readiness. **Expected:** not ready/database down; liveness may remain live.
2. Restart the database and retry. **Expected:** readiness returns ready.
3. Relay pending outbox twice. **Expected:** first marks pending rows, second returns none. Label broker delivery **Stubbed**.

### F-CLEAN

1. Keep audit evidence; do not delete or directly edit append-only rows.
2. Remove synthetic operational records only through approved test cleanup if available.
3. Redact payloads/correlation details before sharing evidence outside the test team.

## 9. Security, privacy, and approvals

- Every query must be organization-scoped.
- Audit and integration payloads must be minimized and redacted.
- Delete is deliberately refused; database-level append-only controls should be validated on PostgreSQL where applicable.
- Agent-run inputs/outputs may contain client data; use synthetic summaries.
- OTEL and broker delivery are not live and must not be presented as production telemetry.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Read-only audit desk | Implemented |
| Health endpoints and DB readiness | Implemented |
| Activity/status/agent-run APIs | Implemented |
| Append-only refusal | Implemented |
| Real OpenTelemetry exporter | Stubbed |
| Redis active readiness probe | Stubbed |
| SNS/SQS outbox publication | Stubbed local relay |
| Audit search/filter/detail UI | Planned / absent |

## 11. Related journeys

- Audit evidence supports every journey in [CROSS_MODULE_JOURNEYS.md](../../testing/CROSS_MODULE_JOURNEYS.md).
- MOD-460 traceability also uses `/audit-logs`; this guide tests the MOD-040 operational foundation.

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Live and ready endpoints checked | |
| Audit desk loading/empty state observed | |
| Event row fields match the real UI | |
| Pagination limit/offset works | |
| Load failure toast recorded if tested | |
| Agent run starts and finishes | |
| Secret-like field is redacted | |
| Audit delete returns forbidden | |
| Cross-organization list does not leak | |
| Readiness recovers after DB restart | |
| Relay/OTEL limitations labeled Stubbed | |
| Focused automated test result recorded | |
