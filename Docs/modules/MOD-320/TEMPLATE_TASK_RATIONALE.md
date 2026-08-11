# MOD-320 Template Task Rationale

| Plan IDs | Status | Why |
|---|---|---|
| FE-001…004 | N/A | Status engine desk deferred |
| WF-001…004 | partial / N/A | Outbox on transition/hold/reopen; Temporal/notifications deferred |
| API-002/003 | partial | Core action APIs; full saved views/OpenAPI examples deferred |
| QA-004 | N/A | No Temporal / agent runtime suite in M1 |
| BE-003 | partial | Outbox written; consumers not wired |

AC-001/002/003 are enforced in `statusengine.domain` / `StatusEngineService` before mutation.
