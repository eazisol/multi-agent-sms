# MOD-020 — Shared Architecture, Domain Kernel, and API Standards

**Status:** Implementation draft (M1 complete; BE/API/AC partial)  
**Human Done (AC-901):** NOT obtained

## Purpose

Common typed identifiers, actor and tenant context, domain errors, transactions, API contracts, and event boundaries for all modules.

## M1 delivered

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

Governance uses UoW, shared paging/concurrency, and enqueues `governance.baseline.created` on baseline create.

## Remaining (beyond M1)

- Outbox **publisher/consumer** runtime (Temporal/SNS-SQS — MOD-500ish)
- Full OpenAPI examples for every error path
- Platform-wide enforcement that agents cannot open DB sessions
- Human AC-901

## Template guidance

- FE CRUD for the kernel itself: **N/A**
- Auth0: deferred to MOD-110; this module defines context *shape*

## Verification

See `VERIFICATION.md`.
