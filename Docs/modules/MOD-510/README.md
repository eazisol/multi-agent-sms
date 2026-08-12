# MOD-510 — Gmail Client Communication Integration

**Status:** Implementation draft (M1); AC-901 NOT obtained  
**Human Done (AC-901):** Not obtained

## Purpose

Connect Gmail mailboxes with opaque `credential_ref` only, sync inbound email into query/thread mappings, import attachments (local-stub), human draft review, and approved send via simulated `local-gmail-sim` delivery.

## Honesty (M1 limits)

- **No live Gmail API or OAuth token exchange** — connections store `credential_ref` only; inbound/outbound are simulated.
- **Attachment import uses `local-stub/...` storage refs** — no S3 or file pipeline.
- **Push idempotency** tracked via `gm_history_cursors` with `push:{external_event_id}` keys.
- **Query/thread linkage** stores UUID refs on `gm_thread_mappings`; does not mutate MOD-210 query records directly in M1.
- **Pub/Sub, Gmail history sync workers, and Temporal send workflows** are deferred.
- AC-901 human owner approval has **not** been obtained.

## M1 delivered

API: `/api/v1/gmail`  
Migration: `20260811_0032`  
FE: `/gmail`

### Checklist main points (DB-001..007)

| ID | Entity |
|---|---|
| MP-001 / DB-001 | `gm_connections` |
| MP-002 / DB-002 | `gm_history_cursors` |
| MP-003 / DB-003 | `gm_thread_mappings` |
| MP-004 / DB-004 | `gm_message_mappings` |
| MP-005 / DB-005 | `gm_attachment_imports` |
| MP-006 / DB-006 | `gm_draft_reviews` |
| MP-007 / DB-007 | `gm_approved_sends` |

## Acceptance behavior (M1)

- **AC-001:** Valid inbound email creates one thread mapping and one message mapping; re-processing same `gmail_message_id` returns existing (409) without duplicates.
- **AC-002:** Draft → submit → approve → send creates `gm_approved_sends` with `local-gmail-sim-{uuid}` and outbound message mapping.
- **AC-003:** Duplicate push `external_event_id` does not duplicate thread/message records.
