# MOD-020 — Shared Architecture, Domain Kernel, and API Standards

**Status:** Done (kernel library)  
**Human Done (AC-901):** Approved 2026-08-11 by workspace owner

## Purpose

Common typed identifiers, actor and tenant context, domain errors, transactions, API contracts, redaction, audit action codes, and event boundaries for all modules.

## Delivered

| ID | Deliverable | Location |
|---|---|---|
| MOD-020-MP-001 | Typed UUID brands | `kernel/ids.py` |
| MOD-020-MP-002 | ActorKind + ActorContext | `kernel/actor.py` |
| MOD-020-MP-003 | TenantContext | `kernel/tenant.py` |
| MOD-020-MP-004 | AppError hierarchy | `kernel/errors.py` |
| MOD-020-MP-005 | SqlAlchemyUnitOfWork | `kernel/uow.py` |
| MOD-020-MP-006 | Outbox table + enqueue | `kernel/outbox.py`, migration `20260810_0002` |
| MOD-020-MP-007 | `application/problem+json` | `kernel/problem.py` (+ compat `message`) |
| MOD-020-MP-008 | Shared PageMeta | `kernel/pagination.py` |
| MOD-020-MP-009 | `assert_expected_version` | `kernel/concurrency.py` |
| MOD-020-SEC-001 | Org/project scope asserts | `kernel/authz.py` (RBAC store = MOD-120) |
| MOD-020-SEC-003 | Payload redaction | `kernel/redact.py` (outbox enqueue applies) |
| MOD-020-SEC-004 | Audit action catalog | `kernel/audit_actions.py` (writers = MOD-040) |

## Explicit N/A (kernel is not a business module)

- **API-001 / FE-\*** — no entity CRUD UI or module-owned CRUD routes
- **WF-001** — business workflow rules live in domain modules + `Docs/governance/WORKFLOW.md`
- **WF-002** — Temporal waits = MOD-350; LangGraph = MOD-360
- **WF-004** — notifications = MOD-440
- **QA-004** — Temporal/agent/file/perf suites owned by those modules; kernel covers outbox + authz/redact tests

## Remaining (platform, not MOD-020 blockers)

- Real SNS/SQS outbox bridge — MOD-500; M1 local relay is `/api/v1/observability/outbox/relay`
- Platform-wide enforcement that agents cannot open DB sessions

## Verification

See `VERIFICATION.md`.
