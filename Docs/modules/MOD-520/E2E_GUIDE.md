# MOD-520 — Jira Work Management Integration

> **Implementation update (2026-08-17):** `MASMS_JIRA_MODE=live` now selects a Jira Cloud
> sandbox client for approved issue creation and comment sync. Credentials are resolved from
> an opaque secret reference, inbound status webhooks require HMAC validation, and Jira still
> cannot mutate MASMS workflow state. `sim` remains the default; live evidence needs a
> human-provisioned Jira sandbox.

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create a simulated Jira issue, conflict, and retry record. |
| QA | Verify approved-only push, protected status, and retry behavior. |
| Developer | Trace the desk to router and integration test assertions. |
| Owner | Confirm Jira Cloud is not contacted. |

## 2. What this module is

This module stores Jira-shaped issue pushes, inbound status conflicts, and comment-sync attempts.

In this company it means: an approved internal-ticket-shaped payload receives a `SIM-*` key, an external status cannot directly close internal work, and a failed comment sync can be retried locally.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| Approved issue push record | Stubbed | Local `SIM-*` key only. |
| Approval-status validation | Implemented | Non-approved payload is rejected. |
| Status conflict record | Implemented | Always returns conflict; no internal mutation. |
| Failed comment sync and retry | Stubbed | Deterministic local failure/recovery. |
| Issue/comment lists | Implemented | Persisted local records. |
| Jira Cloud API, OAuth, webhooks | Planned | Never run by this desk. |
| Link to authoritative ticket record | Stubbed | UI generates a UUID. |

## 4. Requirements and dependencies

- Shared local environment is running.
- Use unique summary and simulated key values.
- The UI sends `approval_status: approved`; negative approval testing uses OpenAPI/tests.
- Internal ticket workflow remains authoritative.
- Header identity is not Auth0.

## 5. How to start

1. Open **Jira** at `/jira`.
2. Confirm the page describes M1 as simulated.
3. Use key `SIM-520-E2E-01`.
4. Do not use real Jira tenant data or credentials.

## 6. Screens, buttons, and files

Desk: [`jira-desk-page.tsx`](../../../apps/web/src/components/jira-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| Refresh | Reloads pushes and comment attempts | Implemented | `jira-desk-page.tsx` |
| Push approved issue | Stores an approved simulated issue push | Stubbed | `jira-desk-page.tsx` |
| Create conflict | Records external/internal status conflict for first issue | Stubbed inbound | `jira-desk-page.tsx` |
| Fail sync then retry | Creates failed comment sync then retries it | Stubbed shortcut | `jira-desk-page.tsx` |
| Pushed issues | Lists simulated key, status, summary | Implemented | `jira-desk-page.tsx` |
| Comment sync attempts | Lists status and retry count | Implemented | `jira-desk-page.tsx` |

## 7. API, data, and automated tests

Prefix: `/api/v1/jira`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/jira/router.py)  
Tests: [`test_jira_api.py`](../../../tests/integration/jira/test_jira_api.py)

| Method | Path | Purpose |
|---|---|---|
| POST | `/issues/push` | Approved-only simulated push |
| GET | `/issues/pushes` | List pushes |
| POST | `/webhooks/status` | Persist conflict and return `409` |
| POST/GET | `/comments/sync` | Create/list attempts |
| POST | `/comments/sync/{id}/retry` | Retry failed attempt |

```bash
uv run pytest tests/integration/jira -q --tb=short
```

The test does not need a Jira account and does not prove Jira Cloud connectivity.

## 8. Test flows

### F-SETUP

1. Open `/jira`.
2. **Expected UI:** three action cards and two lists.
3. **Expected data/audit:** no push created on page load.
4. **Evidence:** initial screenshot.

### F-HAPPY — approved simulated push

1. Enter a unique Summary and `SIM-*` key.
2. Click **Push approved issue**.
3. **Expected UI:** toast “Approved issue pushed to Jira”; pushed row appears.
4. **Expected data/audit:** `approval_status=approved`, `push_status=pushed`, simulated key retained.
5. **Evidence:** row and API response.
6. Record clearly that Jira Cloud was not called.

### F-HAPPY — protected status conflict

1. Ensure at least one pushed issue exists.
2. Enter external status `Done`.
3. Click **Create conflict**.
4. **Expected UI:** conflict registered or API-error toast because endpoint intentionally returns `409`; list reloads.
5. **Expected data/audit:** conflict stored; issue remains `pushed`; internal status is not changed.
6. **Evidence:** `409` response and unchanged issue row.

### F-VALIDATE

1. Clear Summary or key and submit.
2. **Expected:** browser required validation.
3. POST `approval_status: pending` through OpenAPI.
4. **Expected:** `422` and no push record.

### F-AUTHZ

The UI has no module-specific role controls. Use approved API test identities for backend authorization checks. The hard approval invariant is approved-only input, not proof of a production approver.

### F-TENANT

Create in organization A and list using organization B.

**Expected:** organization A pushes and sync attempts are absent.

### F-CONCUR

N/A — current Jira actions do not expose an `expected_version` contract.

### F-TRANS

1. Try to push a pending internal-ticket-shaped payload.
2. **Expected:** rejected before simulated push.
3. Trigger status webhook.
4. **Expected:** conflict instead of internal transition.

### F-GATE

Only `approval_status=approved` may create a push. The desk hard-codes this for its synthetic payload; it does not establish or finalize the underlying ticket approval.

### F-TERM

Pushed issues have no desk edit/reopen action. Status webhook must not turn them into closed internal tickets.

### F-RECOVER

1. Click **Fail sync then retry**.
2. **Expected UI:** “Comment sync retried successfully”.
3. **Expected data:** initial failed attempt increments retry count to 1; retry changes status to `synced`, count to 2, and clears failure reason.
4. **Evidence:** final list row plus API test/API response if intermediate failure must be shown.

### F-CLEAN

Leave synthetic `SIM-*` records for traceability. Do not delete audit evidence or infer an external Jira issue exists.

## 9. Security, privacy, and approvals

- Never enter Jira URLs, tokens, credentials, or real issue content.
- External status is non-authoritative and cannot bypass MASMS workflow.
- Approval must be resolved in the authoritative internal domain.
- Keep all reads and writes organization-scoped.
- Treat inbound webhook fields as untrusted data.

## 10. Planned versus implemented

| Target design | M1 behavior |
|---|---|
| Jira Cloud issue creation | Local issue-push record |
| Signed Jira webhook | Direct synthetic API call |
| Bidirectional status sync | Conflict record; no internal mutation |
| Worker-based comment retry | Combined local fail/retry action |
| Ticket linkage | Generated synthetic internal UUID |
| Browser automation | Manual flow plus API tests |

## 11. Related journeys

- MOD-400 owns internal ticket state.
- MOD-430 owns approval gates.
- MOD-500 supplies common integration controls.
- MOD-610 stores resilience evidence.

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Jira desk loads | |
| Approved push creates `SIM-*` row | |
| Pending push is rejected | |
| Status webhook returns conflict | |
| Internal/push status remains unchanged | |
| Failed sync is visible | |
| Retry reaches synced with count 2 | |
| Cross-org data is hidden | |
| No real Jira data or secret used | |
| No Jira Cloud call claimed | |
| Automated test result recorded | |
