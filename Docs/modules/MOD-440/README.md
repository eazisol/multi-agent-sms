# MOD-440 — Notifications, Preferences, Digests, Delivery, and Failure Handling

**Status:** M1 Done (human AC-901 approved 2026-08-12)
**Human Done (AC-901):** Obtained 2026-08-12

## Purpose

Persist org-scoped notifications, preferences, templates, deliveries, retries, dead letters, and digests. Simulate delivery, retry exhaustion, DLQ listing, and replay — without a live email/SMTP/SES provider.

## Honesty (M1 limits)

- No live email provider; delivery uses `provider_ref=local-sim` only.
- FE is a desk list + create / mark-read / simulate deliver / preference mute note — not a full notification studio.
- Temporal digest scheduling deferred; digest create/process is a FastAPI stub.
- AC-901 obtained 2026-08-12 (human owner sign-off).

## M1 delivered

API: `/api/v1/notifications`  
Migration: `20260811_0028`  
FE: `/notifications`

| ID | Entity |
|---|---|
| MP-001 | `ntf_notifications` |
| MP-002 | `ntf_preferences` |
| MP-003 | `ntf_templates` |
| MP-004 | `ntf_deliveries` |
| MP-005 | `ntf_retries` |
| MP-006 | `ntf_dead_letters` |
| MP-007 | `ntf_digests` |

## Acceptance behavior (M1)

- **AC-001:** Create is org-scoped, audited, outbox-emitted; optional `idempotency_key` unique per org (duplicate → 409)
- **AC-002:** Preferences cannot disable `system_alert`; critical priority is never suppressed by prefs
- **AC-003:** Simulated deliver can fail → retries → after max 3 attempts → dead letter; list DLQ + replay recovers to pending with audit
