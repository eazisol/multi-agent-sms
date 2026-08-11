# MOD-220 Template Task Rationale

| Plan IDs | Status | Why |
|---|---|---|
| FE-001…004 | N/A | Communication desk UI deferred |
| WF-001…004 | partial | Outbox on send; Temporal/provider delivery deferred |
| API-002 | partial | CRUD-lite actions; full list filters/pagination deferred |
| QA-004 | N/A | No Temporal/provider suite in M1 |

Sent immutability (AC-003) is enforced in domain before any post-send mutation.
