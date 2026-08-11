# MOD-350 Template Task Rationale

| Plan IDs | Status | Why |
|---|---|---|
| FE-001 | partial | Ops list + start form only; no Temporal UI / saved views |
| FE-002…004 | N/A / partial | Detail tabs, a11y pass deferred beyond desk basics |
| WF-001 | partial | Catalog + status rules; full durable Temporal waits deferred |
| WF-002 | partial | Stub adapter only; real Temporal client/worker not wired |
| WF-003 | partial | Outbox events written; consumers not wired |
| WF-004 | N/A | Notifications deferred (MOD-440) |
| QA-004 | N/A | No live Temporal worker suite in M1 |
| BE-003 | partial | Outbox written; publisher runtime separate |
| AC-001 | blocked | Requires real Temporal durability |
| AC-901 | done | Human owner approved 2026-08-11 |

Catalog enforcement and Postgres-as-SoT live in `orchestrator.domain` / `OrchestratorService`.
