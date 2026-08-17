# MOD-220 — Conversations, Messages, Attachments, and Communication History

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Open a conversation, draft a message, and send it. |
| QA | Verify sensitive approval, immutable sent history, filters, and paging. |
| Developer | Trace the desk to message, recipient, revision, and send APIs. |
| Owner | Confirm sensitive drafts cannot be sent before approval. |

## 2. What this module is

This module keeps entity-linked communication history. Messages begin as drafts, recipients are attached, sensitive drafts require approval, and sent bodies become immutable.

In this company it means: open a thread for a client query, draft an email to `ops@example.test`, require review when it is confidential, then preserve exactly what was sent.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/comms` conversation list, create, search, status, paging | Implemented | Current UI supersedes stale README. |
| Draft message plus one `to` recipient | Implemented | Recipient is added in the same UI submission sequence. |
| Sensitive approval and send | Implemented | Approval button depends on UI role; API enforces message gate. |
| Thread history and select-for-actions | Implemented | Shows drafts and sent messages. |
| Real provider delivery | Stubbed | Send records state/outbox; no live email provider here. |
| Attachments and revisions | Implemented API only | No desk controls to attach or edit a draft. |
| Multiple recipient roles | Implemented API only | UI adds one `to` recipient. |
| Header identity | Stubbed | Not login. |
| Human M1 acceptance | Blocked | AC-901 not recorded. |

## 4. Requirements and dependencies

- MOD-210 query selection is preferred. `masms.workspace.queryId` links a new conversation.
- `masms.workspace.projectId` is included when present.
- `masms.workspace.conversationId` preserves selection.
- Without a selected query, the desk creates an opportunity-type thread using a generated id.
- Use only synthetic recipient addresses.

## 5. How to start

1. Start API/web from the shared conventions.
2. Optionally select a query in `/queries`.
3. Open `/comms`.
4. Use Contributor to create/draft; use Baseline Approver or Admin for a sensitive approval.
5. Inspect localStorage if a prior conversation is selected unexpectedly.

## 6. Screens, buttons, and files

Screen: `/comms`  
Desk: [`comms-desk-page.tsx`](../../../apps/web/src/components/comms-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| New conversation | Toggles Open conversation form for create-capable roles. | Implemented | `comms-desk-page.tsx` |
| Subject | Required conversation subject. | Implemented | `comms-desk-page.tsx` |
| Sensitivity | Internal, Confidential, Restricted. | Implemented | `comms-desk-page.tsx` |
| Cancel | Closes conversation form. | Implemented | `comms-desk-page.tsx` |
| Open conversation | Links active query or fallback opportunity id. | Implemented | `comms-desk-page.tsx` |
| Search subject | Server-backed `q` filter. | Implemented | `comms-desk-page.tsx` |
| Status | Any, Open, Closed, Archived. | Implemented | `comms-desk-page.tsx` |
| Conversation row | Selects thread and stores workspace conversation id. | Implemented | `comms-desk-page.tsx` |
| Pagination | Changes list offset/page size. | Implemented | `list-pagination.tsx` |
| Message | Required draft body. | Implemented | `comms-desk-page.tsx` |
| Recipient | Required email input; added with role `to`. | Implemented | `comms-desk-page.tsx` |
| Message sensitivity | Internal, Confidential, Restricted. | Implemented | `comms-desk-page.tsx` |
| Draft message | Creates message then adds recipient. | Implemented | `comms-desk-page.tsx` |
| Approve draft | Appears for selected sensitive message and approve-capable role. | Implemented | `comms-desk-page.tsx` |
| Send | Sends selected active message; API may block. | Implemented | `comms-desk-page.tsx` |
| Select for actions | Makes a thread message active for approve/send. | Implemented | `comms-desk-page.tsx` |
| Thread | Displays status, classification, body, timestamps. | Implemented | `comms-desk-page.tsx` |

No close/archive, attachment, draft-edit, delivery-receipt, CC, or BCC control exists on this desk.

## 7. API, data, and automated tests

Prefix: `/api/v1/comms`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/comms/router.py)  
Migration: `20260811_0011`

| Method | Path |
|---|---|
| POST / GET | `/conversations` |
| POST | `/messages` |
| PATCH | `/messages/{message_id}` |
| POST | `/messages/{message_id}/approve` |
| POST | `/messages/{message_id}/send` |
| GET | `/messages/{message_id}/revisions` |
| GET | `/conversations/{conversation_id}/messages` |
| POST | `/recipients` |
| POST | `/attachments` |
| POST | `/delivery-receipts` |

Tests: [`tests/unit/comms`](../../../tests/unit/comms), [`tests/integration/comms/test_comms_api.py`](../../../tests/integration/comms/test_comms_api.py)

```bash
uv run pytest tests/unit/comms tests/integration/comms -q --tb=short
```

## 8. Test flows

Capture conversation/message ids, classifications, approval actor, sent timestamp, API error, and audit/outbox evidence.

### F-SETUP

1. Select a synthetic query in `/queries`, then open `/comms`.
2. Role = Contributor.
3. Expected: conversation inventory loads; workspace conversation may preselect.
4. Evidence: query and conversation localStorage ids.

### F-HAPPY

1. Click **New conversation**.
2. Subject `E2E Discovery Follow-up 220`; Sensitivity **Internal**.
3. Click **Open conversation**; expect success and selected thread.
4. Enter Message `Synthetic follow-up`, Recipient `ops@example.test`, sensitivity Internal.
5. Click **Draft message**; expect “Draft saved with recipient.”
6. Click **Send**; expect “Message sent,” status `sent`, sent timestamp.
7. Reload; sent message remains in Thread.
8. Search `Discovery`; row remains. Filter **Open**; row remains.

### F-HAPPY — sensitive message

1. Draft another message with **Restricted** sensitivity.
2. Expected: status `pending_approval`, “Needs approval.”
3. Attempt **Send** before approval; expect API denial and unchanged state.
4. Switch to Baseline Approver/Admin, select message, click **Approve draft**.
5. Expected: approval actor recorded.
6. Click **Send**; expect `sent`.

### F-VALIDATE

1. Empty Subject must block conversation submit.
2. Empty Message or invalid Recipient email must block draft submit.
3. Direct send with no recipient must be rejected by API.
4. Evidence: browser validation and problem JSON.

### F-AUTHZ

1. Viewer sees no create/draft form and warning where applicable.
2. Contributor should not see **Approve draft** under current role matrix.
3. Agent actor must not be used to finalize sensitive human review where policy requires human.
4. Backend response, not hidden UI alone, is authorization evidence.

### F-TENANT

1. Request conversation list under a second organization.
2. Expected: no first-organization subjects.
3. Request first organization’s message list using another organization.
4. Expected: not found/forbidden; no body leak.

### F-CONCUR

N/A in the desk — no `expected_version` control. Concurrent draft edits can be exercised through PATCH API and revision history.

### F-TRANS

1. Send a sensitive `pending_approval` message directly.
2. Expected: `403`; no sent timestamp.
3. Approve then send; expected valid order.
4. Attempt to approve/send an already sent message; expect rejection or no unsafe mutation.

### F-GATE

1. Restricted/confidential message approval must precede send.
2. Capture `approved_by_actor_id` and exact message id.
3. Approval applies to that draft; do not edit after approval without re-evaluating the gate.

### F-TERM

1. PATCH the body of a sent message through API.
2. Add a recipient after send.
3. Expected: both return `403`; existing body/recipient remain.
4. Sent history is terminal and immutable.

### F-RECOVER

1. Simulate API failure while drafting; expect “Could not draft message.”
2. Because message creation and recipient creation are separate calls, inspect whether a message exists if recipient creation fails.
3. Do not blindly resubmit until checking the thread to avoid duplicate drafts.
4. Provider delivery is Stubbed; a local `sent` state is not proof of real email delivery.

### F-CLEAN

Leave synthetic thread and sent evidence intact. Clear filters. Do not delete revisions, audit, delivery receipts, or outbox records.

## 9. Security, privacy, and approvals

- Message bodies and recipients can be sensitive PII; use `.test` addresses.
- Classification and organization scope must apply to lists and mutations.
- Sensitive approval is a real gate; role dropdown alone is not identity proof.
- Sent content, recipients, and attachments are immutable.
- “Sent” here does not prove external provider delivery.

## 10. Planned versus implemented

| Target design | Current behavior |
|---|---|
| Real provider delivery | Local state/outbox only |
| Rich composer with CC/BCC/attachments | One `to` recipient and body |
| Draft editing UI | PATCH/revisions API only |
| Conversation lifecycle controls | List filter only |
| Authenticated approver | Header identity stub |

## 11. Related journeys

- Previous: [MOD-210](../MOD-210/E2E_GUIDE.md)
- Documents/attachments: [MOD-250](../MOD-250/E2E_GUIDE.md)
- Shared: [Cross-module journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

## 12. Pass / fail checklist

| Check | Result (pass / fail / skip / blocked) |
|---|---|
| Conversation opens against expected workspace entity | |
| Search, status filter, and pagination work | |
| Draft creates message and recipient | |
| Internal draft sends and persists | |
| Sensitive send is blocked before approval | |
| Authorized human approval enables send | |
| Sent body and recipients reject mutation | |
| Thread survives reload | |
| Cross-organization bodies do not leak | |
| Provider delivery recorded as Stubbed | |
| Automated tests command and result recorded | |
