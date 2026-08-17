# MOD-440 — Notifications, Preferences, Simulated Delivery, and Recovery

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create, deliver, read, fail, and retry notifications. |
| QA | Verify preference limits, DLQ behavior, and actor/tenant scoping. |
| Developer | Inspect the Phase 4 notification API and integration test. |
| Owner | Understand that email and scheduled digests are not live. |

## 2. What this module is

MOD-440 persists organization-scoped notifications, actor preferences, templates, delivery attempts, retries, dead letters, and digest records.

In this company it means a user can see an in-app notification and testers can simulate successful or failed delivery. It does not send a real email: delivery uses the local simulator.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/notifications` list/create/pagination | Implemented | Phase 4 desk |
| **Mute reminder email** | Implemented preference record | No real email provider |
| **Deliver OK** / **Deliver fail** | Stubbed delivery | `provider_ref=local-sim` |
| **Retry** | Implemented state action | Local persistence only |
| **Mark read** | Implemented | Shows after delivered/sent |
| Dead-letter list/replay | Implemented API | No desk controls |
| `/my-work` notification column | Implemented read-only aggregation | Current actor, first 20 |
| Real email/SMTP/SES | Planned | Non-testable |
| Temporal digest scheduling | Planned | FastAPI digest processing is stubbed |

## 4. Requirements and dependencies

- Phase: **Phase 4**.
- Duplicate organization-scoped idempotency key returns conflict.
- `system_alert` cannot be disabled; critical priority is not suppressed.
- Three simulated failures dead-letter; replay restores pending and retry count zero.
- Dependencies: API/web, organization and actor header identity.

## 5. How to start

1. Start local services using [TESTING_CONVENTIONS.md](../../testing/TESTING_CONVENTIONS.md).
2. Open `/notifications`.
3. Record the current actor UUID; `/my-work` filters notifications to it.
4. Use synthetic title/body text.
5. Open `/my-work` in another tab for aggregation checks.

## 6. Screens, buttons, and files

Notification desk: [`notifications-desk-page.tsx`](../../../apps/web/src/components/notifications-desk-page.tsx)  
My Work: [`my-work-desk-page.tsx`](../../../apps/web/src/components/my-work-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| **Mute reminder email** | Writes disabled reminder/email preference | Implemented record | notifications desk |
| **Unmute reminder email** | Re-enables same preference | Implemented record | same |
| **New notification** | Toggles form | Implemented | same |
| **Cancel** / **Create** | Closes form / creates pending row | Implemented | same |
| **Deliver OK** | Simulates successful delivery | Stubbed runtime | same |
| **Deliver fail** | Simulates failed delivery | Stubbed runtime | same |
| **Retry** | Schedules local retry from failed | Implemented | same |
| **Mark read** | Marks delivered/sent notification read | Implemented | same |
| Pagination | Changes list page | Implemented | same |
| My Work Notifications heading | Links to `/notifications` | Implemented | my-work desk |

Fields: Title, Recipient actor ID, Body, Channel, Type, and Priority. These are free-text inputs.

## 7. API, data, and automated tests

Prefix: `/api/v1/notifications`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/notifications/router.py)  
Integration test: [`test_notifications_api.py`](../../../tests/integration/notifications/test_notifications_api.py)  
Migration: `20260811_0028`

API routes also cover templates, preferences, dead letters/replay, and digests/process.

```bash
uv run pytest tests/integration/notifications -q --tb=short
```

The verification log records one historical pass and a direct Next build after the normal prebuild was blocked by a running dev port. Do not reuse that as current evidence.

## 8. Test flows

Capture action, UI/toast, persisted status/retry/audit, and screenshot or API response at every step.

### F-SETUP

1. Load `/notifications` and `/my-work`.
2. Record organization and current actor.
3. Confirm the Inbox says local-sim delivery only.

### F-HAPPY

1. Click **New notification**.
2. Enter title `E2E assignment`, current actor recipient, synthetic body, channel `in_app`, type `assignment`, priority `normal`.
3. Click **Create**; expect `Notification created`, status `pending`.
4. Click **Deliver OK**; expect `Delivered (simulated)` and status `delivered`.
5. Click **Mark read**; expect `Marked read` and read state.
6. Reload `/my-work`; expect the notification in its Notifications card if within the first 20.

### F-HAPPY — preference

1. Click **Mute reminder email**.
2. Expect toast `Reminder email muted (critical/system_alert cannot mute)`.
3. Click **Unmute reminder email**; expect unmuted toast.
4. Record that no real email subscription changed.

### F-VALIDATE

1. Leave required Title, Recipient, or Body empty; browser validation blocks.
2. API-create duplicate `idempotency_key` within one organization; expect `409`.
3. Attempt to disable `system_alert`; expect `422`.

### F-AUTHZ

1. Try changing another actor’s preference with an unauthorized identity.
2. Backend must enforce permitted actor scope.
3. UI role selection alone is not authorization evidence.

### F-TENANT

1. Create under organization A.
2. List/get under organization B.
3. Expect no title/body, delivery, preference, or dead-letter leakage.

### F-CONCUR

1. Load one delivered notification in two clients.
2. Mark read in client A.
3. Mark read with stale version in client B.
4. Expect conflict or idempotent safe result; no state regression.

### F-TRANS

1. Mark a `pending` notification read directly by API.
2. Expect invalid transition if reading requires sent/delivered.
3. Confirm desk only shows **Mark read** for `delivered` or `sent`.

### F-GATE

1. Attempt to mute reminder/email; expect allowed.
2. Attempt to mute `system_alert`; expect rejected.
3. Verify critical priority remains unsuppressed.

### F-TERM

1. Deliver successfully and mark read.
2. Confirm failure/retry controls no longer appear.
3. Dead-letter is terminal until explicit replay.

### F-RECOVER

1. Create a pending notification.
2. Click **Deliver fail**, then **Retry**; expect failed then pending/queued per response.
3. For full DLQ proof, use API to fail three times, list `/dead-letters`, and replay.
4. Expect replay status `replayed`; notification returns `pending`, retry count `0`.

### F-CLEAN

1. Restore reminder-email preference to its original state.
2. Retain delivery/dead-letter/audit evidence.
3. Record notification and dead-letter IDs.

## 9. Security, privacy, and approvals

- Notification bodies may contain PII; use synthetic data.
- Organization and recipient actor scope must be enforced server-side.
- Critical/system alerts cannot be muted.
- Delivery simulation must never be reported as real email delivery.
- Header identity is a stub, not authentication.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Real email provider | Planned |
| Provider delivery confirmation | `local-sim` only |
| Scheduled Temporal digests | Planned |
| DLQ/replay desk | API only |
| Search/status/channel filters | API only |
| Full My Work pagination | First 20 aggregation |

## 11. Related journeys

- `/my-work` aggregates follow-ups, approvals, and notifications.
- [MOD-220 follow-ups](../MOD-220/E2E_GUIDE.md)
- [MOD-310 approval gates](../MOD-310/E2E_GUIDE.md)
- [MOD-450 dashboard](../MOD-450/E2E_GUIDE.md)

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Notification creates pending | |
| Successful delivery labeled simulated | |
| Mark read works after delivery | |
| My Work shows current actor item | |
| Reminder email preference toggles | |
| System alert mute rejected | |
| Critical notification unsuppressed | |
| Three failures dead-letter | |
| Replay restores pending/retry zero | |
| Cross-tenant content hidden | |
| Real email recorded Planned | |
| Integration test output recorded | |
