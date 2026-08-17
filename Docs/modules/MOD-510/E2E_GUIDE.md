# MOD-510 — Gmail Client Communication Integration

> **Implementation update (2026-08-17):** `MASMS_GMAIL_MODE=live` now selects a sandbox
> Gmail HTTP client. It resolves OAuth JSON through `credential_ref`, refreshes tokens when
> configured, polls inbound history/messages through the new connection sync endpoint, and
> sends only approved drafts. `sim` remains the default; no sandbox pass is claimed without
> a human-provisioned mailbox and credential reference.

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create a simulated mailbox and inspect message mappings. |
| QA | Verify inbound/push idempotency and the draft state sequence. |
| Developer | Trace the Gmail desk, API contracts, and integration tests. |
| Owner | Confirm no Google API, OAuth, Pub/Sub, or real email ran. |

## 2. What this module is

This module stores Gmail-shaped mailbox, thread, message, attachment, draft-review, and approved-send records.

In this company it means: a tester can simulate a client email, map it to local records, and exercise draft → submit → approve → send while all delivery remains inside MASMS.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| Connection create and activation | Implemented | **Add connection** performs both operations. |
| Inbound processing | Stubbed | Synthetic IDs and sender only. |
| Push notification receipt | Stubbed | No Google Pub/Sub. |
| Thread/message mappings | Implemented | Persisted and listed. |
| Draft review/send sequence | Stubbed shortcut | Combined button runs all four calls. |
| Approved send id | Stubbed | `local-gmail-sim-*`, not Google. |
| Attachment storage | Stubbed/API only | `local-stub/...`, no S3 pipeline. |
| Gmail API and OAuth | Planned | Not executed. |
| Human separation in combined button | Planned | Current UI combines approval with creation/send. |

Never use the toast wording as evidence that an email reached a recipient.

## 4. Requirements and dependencies

- API/web and local database are running.
- Use `example.com` addresses and synthetic message identifiers.
- MOD-500 concepts apply, but this module has its own `gm_*` records.
- Header identity is a stub, not Auth0.
- A real human approval process remains required for production client communication.

## 5. How to start

1. Start the shared environment.
2. Open **Gmail** at `/gmail`.
3. Use a unique code such as `gmail-e2e-510-01`.
4. Keep all addresses synthetic.
5. Select the created connection before using other cards.

## 6. Screens, buttons, and files

Desk: [`gmail-desk-page.tsx`](../../../apps/web/src/components/gmail-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| Refresh | Reloads connections and mappings | Implemented | `gmail-desk-page.tsx` |
| Add connection | Creates then activates a mailbox record | Implemented shortcut | `gmail-desk-page.tsx` |
| Connection row | Selects mailbox for later actions | Implemented | `gmail-desk-page.tsx` |
| Process inbound | Creates synthetic inbound thread/message mappings | Stubbed | `gmail-desk-page.tsx` |
| Receive push | Stores/processes a synthetic push event | Stubbed | `gmail-desk-page.tsx` |
| Create → submit → approve → send | Runs full draft flow | Stubbed shortcut | `gmail-desk-page.tsx` |
| Thread mappings | Lists Gmail-shaped thread ids and query refs | Implemented | `gmail-desk-page.tsx` |
| Message mappings | Lists inbound/outbound records | Implemented | `gmail-desk-page.tsx` |

There is no separate draft list or human-review pause on this M1 desk.

## 7. API, data, and automated tests

Prefix: `/api/v1/gmail`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/gmail/router.py)  
Tests: [`test_gmail_api.py`](../../../tests/integration/gmail/test_gmail_api.py)

| Method | Path | Purpose |
|---|---|---|
| POST/GET | `/connections` | Mailbox records |
| POST | `/connections/{id}/activate` | Activate |
| POST | `/inbound/process` | Synthetic inbound |
| POST | `/push/receive` | Synthetic push |
| GET | `/threads` | Thread mappings |
| GET | `/messages` | Message mappings |
| POST | `/drafts` | Create draft |
| POST | `/drafts/{id}/submit` | Pending review |
| POST | `/drafts/{id}/approve` | Approve record |
| POST | `/drafts/{id}/send` | Simulated send |

```bash
uv run pytest tests/integration/gmail -q --tb=short
```

Tests prove local API behavior, not Google connectivity or delivery.

## 8. Test flows

### F-SETUP

1. Open `/gmail`.
2. **Expected UI:** connection card, simulation cards, and mapping lists.
3. **Expected data/audit:** page load does not create a mailbox.
4. **Evidence:** screenshot and organization id.

### F-HAPPY — inbound mapping

1. Enter unique Code and `inbox-e2e@example.com`.
2. Click **Add connection**.
3. **Expected UI:** success toast and active selected connection.
4. Enter unique Gmail message/thread ids and `client-e2e@example.com`.
5. Click **Process inbound**.
6. **Expected UI:** “Inbound email processed”.
7. **Expected data/audit:** one inbound message and one thread mapping.
8. **Evidence:** connection id, synthetic ids, mapping rows.

### F-HAPPY — simulated draft send

1. Enter synthetic To, Subject, and Body preview.
2. Click **Create → submit → approve → send**.
3. **Expected UI:** toast includes `local-gmail-sim-*`.
4. **Expected data/audit:** draft transitions through pending review and approved; approved-send and outbound mapping are persisted.
5. **Evidence:** outbound mapping and local simulated send id.
6. Record explicitly: no message was sent through Gmail.

### F-VALIDATE

1. Clear required Code or Email and submit.
2. **Expected:** browser validation blocks.
3. Repeat inbound with the same `gmail_message_id` through OpenAPI.
4. **Expected:** `409`, `idempotent=true`, and no duplicate mappings.

### F-AUTHZ

The combined desk action does not demonstrate independent human approval. Use API tests with approved identities to verify policy. Do not tell an agent to approve real client mail.

### F-TENANT

List connections, threads, and messages using another organization.

**Expected:** no organization A data is returned.

### F-CONCUR

Submit or approve a draft with stale `expected_version` through OpenAPI.

**Expected:** conflict; no skipped or overwritten state.

### F-TRANS

Try `/send` before approval.

**Expected:** invalid transition/approval error and no outbound mapping.

### F-GATE

1. The valid API sequence is draft → submit → approve → send.
2. Current UI combines it as an M1 shortcut.
3. **Evidence:** API state records, not a claim of independent production approval.

### F-TERM

Sent records are not editable from the desk. Use a new draft for another scenario.

### F-RECOVER

1. Submit the same push external event id twice through OpenAPI.
2. **Expected:** first `201`; duplicate `200` with `idempotent=true`.
3. **Expected data:** only one thread and one message mapping.
4. **Evidence:** both responses and final counts.

### F-CLEAN

Leave clearly named synthetic records. Do not delete audit history and do not send to real addresses.

## 9. Security, privacy, and approvals

- Never enter Gmail passwords, OAuth tokens, real mailbox addresses, or client content.
- `credential_ref` is opaque and does not prove a secret exists.
- Agent actors must not provide final client-communication approval.
- A production send needs separate authorized human review of the exact content.
- Organization scope applies to mailbox and mapping data.

## 10. Planned versus implemented

| Target design | M1 behavior |
|---|---|
| Google OAuth/API | Local mailbox record |
| Gmail Pub/Sub/history worker | Synthetic push endpoint |
| S3 attachment pipeline | Local stub reference |
| Independent human draft review | Combined UI shortcut; API states exist |
| Real delivery receipt | `local-gmail-sim-*` record |
| Browser automation | Manual guide and API integration tests |

## 11. Related journeys

- MOD-500 supplies common integration concepts.
- MOD-210 owns authoritative query intake.
- MOD-300 owns internal communication records.
- MOD-600 governs privacy and training policy.

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Gmail desk loads | |
| Add connection creates active record | |
| Inbound creates one thread mapping | |
| Inbound creates one message mapping | |
| Duplicate message is idempotent | |
| Push duplicate is idempotent | |
| Draft sequence reaches local simulated sent | |
| Outbound mapping appears | |
| Send before approval is rejected | |
| Cross-org records are hidden | |
| No real address or secret used | |
| No Google delivery claimed | |
| Automated test result recorded | |
