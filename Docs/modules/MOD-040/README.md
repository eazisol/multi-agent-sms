# MOD-040 — Observability, Audit Foundation, and Operational Health

**Status:** Implementation draft (M1 scaffold complete; real OTEL SDK deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Structured logging/tracing stubs, append-only audit, activity events, status history, agent runs, integration events, correlation IDs, and operational health.

## M1 delivered

| ID | Deliverable |
|---|---|
| MP-001 | `ops_audit_logs` + append-only writer + delete blocked |
| MP-002 | `ops_activity_events` |
| MP-003 | `ops_status_history` |
| MP-004 | `ops_agent_runs` + start/finish API |
| MP-005 | `ops_integration_events` model/writer |
| MP-006 | `TracingStub` (OTEL SDK packaging deferred) |
| MP-007 | `/health/live` + `/health/ready` (DB check) |

Migration: `20260810_0003_mod040_observability.py`

## Limits

- Real OpenTelemetry exporters/Collector not wired (no new heavy deps yet).  
- Redis readiness is config-aware only until a redis client is approved.  
- Governance still uses `gov_audit_events`; shared ops tables are the platform foundation going forward.

## Verification

See `VERIFICATION.md`.
