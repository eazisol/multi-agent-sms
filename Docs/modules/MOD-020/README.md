# MOD-020 — Shared Architecture, Domain Kernel, and API Standards

**Status:** Implementation draft (M1 partial: typed IDs, actor/tenant context, domain errors)  
**Human Done (AC-901):** NOT obtained

## Purpose

Common typed identifiers, actor and tenant context, domain errors, transactions, API contracts, and event boundaries for all modules.

## M1 delivered in this slice

| ID | Deliverable | Location |
|---|---|---|
| MOD-020-MP-001 | Typed UUID brands | `apps/api/src/masms_api/kernel/ids.py` |
| MOD-020-MP-002 | ActorKind + ActorContext | `kernel/actor.py` |
| MOD-020-MP-003 | TenantContext (org / optional client+project) | `kernel/tenant.py` |
| MOD-020-MP-004 | Shared AppError hierarchy | `kernel/errors.py` |

FastAPI header adapter: `masms_api.deps.get_request_context` builds `RequestContext` from:

- `X-Organization-Id`, `X-Client-Id` (optional), `X-Project-Id` (optional)
- `X-Actor-Id`, `X-Actor-Kind`, `X-Actor-Name`
- `X-Correlation-Id`

Compatibility: `masms_api.errors` and `masms_api.deps` re-export kernel types so governance keeps working.

## Not in this slice (remaining M1)

- Unit of work (`MOD-020-MP-005`)
- Outbox table + publisher (`MOD-020-MP-006`)
- RFC-style problem-details media type polish (`MOD-020-MP-007`)
- Shared pagination helpers (`MOD-020-MP-008`) — still governance-local `PageMeta`
- Shared optimistic concurrency helper (`MOD-020-MP-009`) — still service-local checks

## Template task guidance

- DB rows for typed IDs / actor / tenant / domain errors: **not physical tables**; record conventions in data dictionary.
- FE list/detail CRUD for the kernel itself: **N/A** (library, not a user entity module).
- Full SEC/Auth0: deferred to MOD-110; this module provides the context *shape*.

## Verification

See `VERIFICATION.md`.
