# MOD-350 — Temporal Orchestrator and Durable Business Workflows

**Status:** Implementation draft (M1 registry + stub adapter + ops desk)  
**Human Done (AC-901):** NOT obtained

## Purpose

Persist the approved Temporal workflow catalog, versions, instances, signals, failures, and interventions in PostgreSQL. FastAPI owns mutable business state; the Temporal adapter is a stub that does not require a live Temporal server or worker.

## Honesty (M1 limits)

- Live Temporal worker/cluster is **not** required for M1.
- `TemporalAdapter` returns `stub-{uuid}` run ids and no-ops signal/cancel.
- Frontend is an ops instance list + start form — not a full Temporal UI.
- AC-001 (survive worker restarts) is not claimed; AC-901 remains blocked pending human review.
- AC-003 (Postgres is source of truth) is enforced: instance status/history live in `orf_*` tables.

## M1 delivered

API: `/api/v1/orchestrator`  
Migration: `20260811_0021`  
FE: `/workflows` desk

| ID | Entity |
|---|---|
| MP-001 | `orf_workflow_instances` |
| MP-002 | `orf_workflow_signals` |
| MP-003 | `orf_workflow_versions` (+ `orf_workflow_definitions`) |
| MP-004 | `orf_workflow_failures` |
| MP-005 | `orf_interventions` |
| MP-006 | 12 approved workflow codes (seeded per org) |

## Approved workflow codes

`query_intake`, `requirement_clarification`, `project_handover`, `assignment_ack`, `blocker_resolution`, `qa_rejection_loop`, `client_status_report`, `change_request_flow`, `deployment_approval`, `project_closure`, `approval_gate_wait`, `followup_escalation`

## Key rules

- Only catalog codes may start instances.
- Instance transitions: `pending → running → waiting|completed|failed|cancelled`; `waiting → running|…`; `failed → running|cancelled|completed` (intervention).
- Signal idempotency by `(organization_id, instance_id, idempotency_key)`.
- Failures append-only; interventions require a non-terminal instance.
- Outbox events: `orchestrator.workflow.started`, `.signaled`, `.failed`, `.cancelled` / `.completed` / `.running`.
