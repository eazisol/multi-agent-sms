# MOD-040 Template Task Rationale

| Plan IDs | Status | Why |
|---|---|---|
| FE-001…004 | N/A | Ops foundation APIs first; full ops UI later |
| WF-001…004 | N/A / partial | No Temporal alert WF in this slice |
| DB-006 | N/A | OTEL is telemetry config, not a DB table |
| DB-007 | N/A | Health checks are endpoints, not tables |
| BE-003 | partial | Integration/outbox relay still deferred |

CRUD-style FE for logs is intentionally out of M1; read APIs exist under `/api/v1/observability`.
