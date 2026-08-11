# MOD-220 — Conversations, Messages, Attachments, and Communication History

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Record material communications linked to business entities, enforce sensitive-message approval, and keep sent-message history immutable.

## M1 delivered

API: `/api/v1/comms`  
Migration: `20260811_0011`

| ID | Entity |
|---|---|
| MP-001 | `com_conversations` (related entity type/id) |
| MP-002 | `com_messages` |
| MP-003 | `com_message_revisions` |
| MP-004 | `com_message_recipients` |
| MP-005 | `com_delivery_receipts` |
| MP-006 | `com_attachment_links` (file refs; bytes in MOD-250) |

## Limits

- FE deferred; real file storage deferred to MOD-250
- Outbox event on send only; provider delivery not integrated
- Attachment links are references, not binary storage
