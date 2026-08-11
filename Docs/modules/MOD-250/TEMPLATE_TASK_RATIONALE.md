# MOD-250 Template Task Rationale

| Plan IDs | Status | Why |
|---|---|---|
| FE-001…004 | N/A | Document desk UI deferred (Phase 2 FE batch later) |
| WF-001…004 | partial | Outbox on scan record; Temporal scan workers deferred |
| API-002 | partial | Core actions; list/pagination deferred |
| QA-004 | partial | Scan gate tested via API stub; no real AV engine |

Storage bytes remain outside DB; `storage_key` is the authoritative object reference for M1.
