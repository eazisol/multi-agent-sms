# MOD-020 — Shared Architecture, Domain Kernel, and API Standards

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

Developers and QA proving that every API speaks the same language (ids, errors, pages, concurrency). There is **no desk**.

## 2. What this module is

The kernel is the shared toolbox: typed ids, who is acting, which organization, how errors look, how a transaction and outbox work, how pages are sliced, and how stale versions are rejected.

If later modules return random JSON errors or forget `organization_id`, this module’s rules were skipped.

## 3. Status honesty

| Item | Status |
|---|---|
| Kernel library under `apps/api/src/masms_api/kernel` | Implemented |
| Outbox table + enqueue | Implemented |
| Problem+json errors | Implemented |
| Pagination `PageMeta` | Implemented |
| Optimistic concurrency helper | Implemented |
| Redaction helper | Implemented |
| Org/project asserts | Implemented (full RBAC is MOD-120) |
| SNS/SQS outbox consumer | Planned (MOD-500); local relay is MOD-040 |
| Agent cannot open DB sessions platform-wide | Planned / not fully enforced |

## 4. Requirements and dependencies

- MVP-NFR-004, MVP-NFR-010
- Depends on: MOD-010
- Downstream: all FastAPI modules

## 5. How to start

Complete [MOD-010](../MOD-010/E2E_GUIDE.md). Open `http://127.0.0.1:8000/docs` and trigger any validation error (empty POST). You should see `application/problem+json`.

## 6. Screens, buttons, and files

No UI. Kernel files:

| File | Role |
|---|---|
| [`kernel/ids.py`](../../../apps/api/src/masms_api/kernel/ids.py) | Typed UUID brands |
| [`kernel/actor.py`](../../../apps/api/src/masms_api/kernel/actor.py) | ActorKind + ActorContext |
| [`kernel/tenant.py`](../../../apps/api/src/masms_api/kernel/tenant.py) | TenantContext |
| [`kernel/errors.py`](../../../apps/api/src/masms_api/kernel/errors.py) | AppError hierarchy |
| [`kernel/uow.py`](../../../apps/api/src/masms_api/kernel/uow.py) | Unit of work |
| [`kernel/outbox.py`](../../../apps/api/src/masms_api/kernel/outbox.py) | Outbox enqueue |
| [`kernel/problem.py`](../../../apps/api/src/masms_api/kernel/problem.py) | Problem details |
| [`kernel/pagination.py`](../../../apps/api/src/masms_api/kernel/pagination.py) | PageMeta |
| [`kernel/concurrency.py`](../../../apps/api/src/masms_api/kernel/concurrency.py) | expected_version |
| [`kernel/authz.py`](../../../apps/api/src/masms_api/kernel/authz.py) | Scope asserts |
| [`kernel/redact.py`](../../../apps/api/src/masms_api/kernel/redact.py) | Secret/PII redaction |
| [`kernel/audit_actions.py`](../../../apps/api/src/masms_api/kernel/audit_actions.py) | Audit action catalog |

Web client types: [`apps/web/src/lib/api.ts`](../../../apps/web/src/lib/api.ts) (`ProblemDetails`, `PageMeta`).

## 7. API, data, and automated tests

Migration: [`migrations/versions/20260810_0002_mod020_outbox.py`](../../../migrations/versions/20260810_0002_mod020_outbox.py)

Tests: `tests/unit/kernel/`

```bash
uv run pytest tests/unit/kernel -q --tb=short
```

Outbox relay for manual check: `POST /api/v1/observability/outbox/relay` ([MOD-040](../MOD-040/E2E_GUIDE.md)) — **stub**, not SNS.

## 8. Test flows

### F-SETUP

API running.

### F-HAPPY

1. `GET /api/v1/governance/baselines?limit=10&offset=0`.
2. **Expected:** `items` + `page` with `limit`, `offset`, `total`, `has_more`.

### F-VALIDATE

1. POST a known resource with a missing required field.
2. **Expected:** 4xx problem+json with `code` and `message`, not a stack trace HTML page.

### F-AUTHZ

1. Call a mutating API with `X-Actor-Kind: agent` on a human-only action (baseline approve).
2. **Expected:** forbidden.

### F-TENANT

1. Use a different `X-Organization-Id` than the row’s org.
2. **Expected:** not found or forbidden.

### F-CONCUR

1. Update with wrong `expected_version`.
2. **Expected:** conflict.

### F-TRANS

N/A — the kernel provides shared primitives but owns no business status lifecycle.

### F-GATE

N/A — human approval gates are enforced by consuming business modules; the kernel only identifies actor kind and shared errors.

### F-TERM

N/A — the kernel owns no terminal business record or reopen process.

### F-RECOVER

Enqueue happens in the same transaction as the business write. If the API reports success, the outbox row should exist. Relay is a later stub.

### F-CLEAN

N/A.

## 9. Security, privacy, and approvals

- Never log raw secrets. Redaction applies on outbox enqueue.
- Kernel asserts scope; it does not replace MOD-120 permission rows.

## 10. Planned versus implemented

Live broker consumers, universal agent DB-session block, and OpenTelemetry exporters are later modules.

## 11. Related journeys

Every journey depends on this contract. Start with [J-LEARN](../../testing/CROSS_MODULE_JOURNEYS.md#j-learn-first-hour).

## 12. Pass / fail checklist

| Step | Result |
|---|---|
| List endpoints return PageMeta | |
| Validation returns problem+json | |
| Stale version conflicts | |
| Cross-org access denied | |
| Kernel unit tests run | |
