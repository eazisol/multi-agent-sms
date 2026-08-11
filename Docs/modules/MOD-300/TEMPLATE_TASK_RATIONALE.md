# MOD-300 Template Task Rationale

| Plan IDs | Status | Why |
|---|---|---|
| FE-001…004 | N/A | Tickets desk UI deferred |
| WF-001…004 | partial / N/A | Outbox on ready/done/reopen/transition; Temporal/notifications deferred |
| API-002 | partial | Project list + CRUD-lite; saved views/pagination deferred |
| API-003 | partial | Schemas present; full OpenAPI examples deferred |
| QA-004 | N/A | No Temporal/agent suite in M1 |
| SEC-001/003 | partial | Org/project scope + audit; full classification matrix deferred |

AC-001 Ready gate and AC-003 reopen authority are enforced in `tickets.domain` before mutation.
