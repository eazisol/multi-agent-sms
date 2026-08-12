# MOD-500 — Integration Framework, OAuth Connections, Webhooks, Outbox, Inbox, and Sync State

**Status:** M1 Done (human AC-901 approved 2026-08-12)
**Human Done (AC-901):** Obtained 2026-08-12

## Purpose

Provide org-scoped integration connections with opaque `credential_ref` (never raw secrets), idempotent webhook/inbox intake, external entity mappings, sync cursors, integration relay outbox (`ig_outbox_events`), connection health tracking, and simulated process/relay flows for M1.

## Honesty (M1 limits)

- **No live OAuth or provider API calls** — connections store `credential_ref` only; tokens live in secret manager (not implemented here).
- **`ig_outbox_events` is distinct from kernel `sys_outbox_messages`** — module outbox is for outbound integration relay; kernel outbox still receives domain events via `enqueue_outbox`.
- **Relay and inbox process are simulated** — `force_fail` flags exercise failure paths without external side effects.
- **Webhook signature validation, rate limits, Temporal workers, and SNS/SQS bridges** are deferred.
- AC-901 obtained 2026-08-12 (human owner sign-off).

## M1 delivered

API: `/api/v1/integrations`  
Migration: `20260811_0031`  
FE: `/integrations`

### Checklist main points (DB-001..007)

| ID | Entity |
|---|---|
| MP-001 / DB-001 | `ig_connections` |
| MP-002 / DB-002 | `ig_webhook_events` |
| MP-003 / DB-003 | `ig_sync_cursors` |
| MP-004 / DB-004 | `ig_external_mappings` |
| MP-005 / DB-005 | `ig_outbox_events` (integration relay) |
| MP-006 / DB-006 | `ig_inbox_events` |
| MP-007 / DB-007 | `ig_connection_health` |

## Acceptance behavior (M1)

- **AC-001:** Inbox process with `force_fail=true` marks inbox failed, updates health, and does **not** create mappings; successful process may create mapping from payload ids.
- **AC-002:** Mappings, connections, and events are org-scoped (cross-org 404/empty); mutations write audit + kernel outbox.
- **AC-003:** Raw `client_secret` / `access_token` rejected at API; responses and audit payloads never contain raw secret strings; only opaque `credential_ref`.
