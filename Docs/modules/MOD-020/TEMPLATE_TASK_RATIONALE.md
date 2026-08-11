# MOD-020 Template Task Rationale

| Plan IDs | Status | Why |
|---|---|---|
| API-001 | N/A | Kernel library — no business CRUD/history routes |
| FE-001…004 | N/A | Kernel library — no entity UI |
| WF-001 | N/A | Business workflow definitions live in domain modules |
| WF-002 | N/A | Temporal / LangGraph owned by MOD-350 / MOD-360 |
| WF-004 | N/A | Notifications deferred to MOD-440 |
| QA-004 | N/A | No Temporal/agent/file/perf surface in kernel |
| SEC-001 | done | `kernel/authz.py` scope asserts; RBAC tables = MOD-120 |
| SEC-003 | done | `kernel/redact.py` + outbox enqueue redaction |
| SEC-004 | done | `kernel/audit_actions.py` catalog; writers = MOD-040 |
| QA-003 | done | Unit negatives for org/project scope + redact |
| AC-901 | done | Human owner approved 2026-08-11 |
