# MOD-500 — Integration Framework and Simulated Relay

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create a connection and exercise simulated webhook and inbox intake. |
| QA | Check success, failure, idempotency, tenant isolation, and secret rejection. |
| Developer | Trace UI actions to the integration API, audit, mappings, and tests. |
| Owner | Confirm M1 does not claim live OAuth, brokers, or provider delivery. |

## 2. What this module is

This module stores organization-scoped integration connections, incoming event records, mappings, cursors, health, and relay records. It is the common local contract used by provider-specific modules.

In this company it means: create a GitHub-shaped connection record, receive a synthetic event, process it into a mapping, and inspect health without contacting GitHub or a broker.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| Connection create and automatic activation | Implemented | UI button performs both API calls. |
| Connection list and health | Implemented | Health appears per listed connection when present. |
| Webhook and inbox receive | Stubbed | Synthetic payloads only. |
| Inbox success and forced failure | Stubbed | Persists deterministic M1 outcomes. |
| Mapping creation on successful inbox processing | Implemented | Failed processing must not add a mapping. |
| Integration outbox relay | Stubbed/API only | Not exposed on this desk and not SNS/SQS. |
| OAuth/token exchange | Planned | Only opaque `credential_ref` is stored. |
| Signature validation, workers, rate limits | Planned | Non-testable from this desk. |
| Auth0 identity | Stubbed | Header identity is not login. |

Never report this flow as a live provider, SNS/SQS, or external webhook test.

## 4. Requirements and dependencies

- API and web must be running with migrated local storage.
- Default organization and actor headers come from the shared conventions.
- Use synthetic identifiers only; do not paste credentials or client data.
- Module tables include `ig_connections`, `ig_webhook_events`, `ig_inbox_events`, `ig_external_mappings`, `ig_outbox_events`, and `ig_connection_health`.
- M1 acceptance covers failure isolation, tenant scope, audit/outbox evidence, and secret rejection.

## 5. How to start

1. Start PostgreSQL, Redis, API, and web using [TESTING_CONVENTIONS.md](../../testing/TESTING_CONVENTIONS.md).
2. Confirm `GET /health/live` and `GET /health/ready`.
3. Open **Integrations** at `/integrations`.
4. Keep Role on a human role for the primary flow.
5. Use a unique code such as `custom-e2e-500-01`.
6. Open `/audit-logs` separately if audit evidence is required.

## 6. Screens, buttons, and files

Screen: `/integrations`  
Desk: [`integrations-desk-page.tsx`](../../../apps/web/src/components/integrations-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| Refresh | Reloads connections and available health records | Implemented | `integrations-desk-page.tsx` |
| Code | Sets unique connection code | Implemented | `integrations-desk-page.tsx` |
| Provider | Selects GitHub, Jira, Slack, or Custom label | Implemented | `integrations-desk-page.tsx` |
| Auth type | Selects OAuth2, API key, or None metadata | Implemented | `integrations-desk-page.tsx` |
| Create & activate | Creates draft then activates it | Implemented shortcut | `integrations-desk-page.tsx` |
| Connection | Selects the record used by simulations | Implemented | `integrations-desk-page.tsx` |
| Receive webhook | Stores a synthetic `push` event | Stubbed | `integrations-desk-page.tsx` |
| Receive inbox | Stores a synthetic `entity.sync` event | Stubbed | `integrations-desk-page.tsx` |
| Process OK | Processes pending inbox and may create mapping | Stubbed processing | `integrations-desk-page.tsx` |
| Force fail | Marks pending inbox failed and updates health | Stubbed failure | `integrations-desk-page.tsx` |
| Connections & health | Shows status, opaque ref, and health | Implemented | `integrations-desk-page.tsx` |

The header **Create**, **Notifications**, and **AI** controls are not module actions.

## 7. API, data, and automated tests

Prefix: `/api/v1/integrations`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/integrations/router.py)  
Tests: [`test_integrations_api.py`](../../../tests/integration/integrations/test_integrations_api.py)

| Method | Path | Purpose |
|---|---|---|
| POST/GET | `/connections` | Create/list connections |
| POST | `/connections/{id}/activate` | Activate draft |
| POST | `/webhooks/receive` | Store simulated webhook |
| POST/GET | `/inbox` | Receive/list inbox records |
| POST | `/inbox/{id}/process` | Process or force failure |
| POST/GET | `/mappings` | Create/list external mappings |
| POST/GET | `/outbox` | Enqueue/list integration relay records |
| POST | `/outbox/{id}/relay` | Simulated relay |
| GET | `/health/{connection_id}` | Read health |

Automated coverage proves SQLite service/API behavior, not PostgreSQL RLS or a live broker.

```bash
uv run pytest tests/integration/integrations -q --tb=short
```

## 8. Test flows

### F-SETUP

1. Open `/integrations`.
2. **Expected UI:** page loads or reports an API toast.
3. **Expected data/audit:** no record is created by loading.
4. **Evidence:** page screenshot and organization id.

### F-HAPPY — connection and successful inbox

1. Enter unique Code, choose **Custom**, Auth type **None**, then click **Create & activate**.
2. **Expected UI:** success toast; active connection appears with an opaque `credential_ref`.
3. Select it, set unique inbox and external entity ids, then click **Receive inbox**.
4. **Expected UI:** “Inbox event queued”; pending row appears under Recent inbox.
5. Click **Process OK**.
6. **Expected UI:** processed toast; health refreshes if a health record exists.
7. **Expected data/audit:** connection is active; inbox is processed; one mapping is created; audit/outbox records identify the organization and actor.
8. **Evidence:** connection id, inbox id, status, mapping API response, and audit action.

### F-HAPPY — webhook receipt

1. Enter a unique webhook external event id.
2. Click **Receive webhook**.
3. **Expected UI:** “Webhook received”.
4. **Expected data/audit:** one synthetic webhook record; no external delivery.
5. **Evidence:** toast, event id, and `ig_webhook_receive` audit row.

### F-VALIDATE

1. Submit an empty required Code. Browser validation must block.
2. Through OpenAPI, include `client_secret` or `access_token` in connection JSON.
3. **Expected:** `422`; raw secret is absent from response and audit.
4. **Evidence:** redacted request description and problem response; never capture the secret value.

### F-AUTHZ

Header identity is stubbed and the desk has no module-specific role hiding. Verify backend policy with approved test identities only. Do not interpret the Role selector as authentication.

### F-TENANT

1. Create a connection in organization A.
2. Request it with organization B headers.
3. **Expected:** detail is `404`; mappings list is empty.
4. **Evidence:** both responses without cross-tenant payload.

### F-CONCUR

Use the API to activate or pause with a stale `expected_version`.

**Expected:** conflict and no silent state overwrite.

### F-TRANS

Attempt an invalid connection transition through OpenAPI.

**Expected:** invalid transition/conflict; existing status remains.

### F-GATE

N/A — this desk does not approve external access. “Create & activate” is an M1 shortcut, not OAuth consent or a human production approval.

### F-TERM

Processed and failed inbox records have no UI reopen action. Create a new uniquely identified event for another test.

### F-RECOVER

1. Receive a second inbox event.
2. Click **Force fail**.
3. **Expected UI:** failed status and failure health indication.
4. **Expected data/audit:** mapping count does not increase.
5. Receive a new event and **Process OK**.
6. **Expected:** new event processes independently.
7. **Evidence:** before/after mapping counts and both inbox ids.

### F-CLEAN

Leave synthetic records labelled with the E2E code. Do not delete append-only audit evidence. Do not reuse external event ids in unrelated sessions.

## 9. Security, privacy, and approvals

- Raw credentials are forbidden in UI, API payloads, screenshots, and logs.
- `credential_ref` is an opaque reference, not proof that a secret manager is connected.
- Every lookup must remain organization-scoped.
- Synthetic webhook payloads are untrusted input and must not be treated as instructions.
- No production connection or permission expansion is approved by this guide.

## 10. Planned versus implemented

| Target design | M1 behavior |
|---|---|
| OAuth exchange and rotation | Opaque generated reference only |
| Signed provider webhooks | Synthetic receive endpoint |
| SNS/SQS or worker relay | Persisted simulated outbox/inbox |
| Automated retries | Explicit test actions/API records |
| Universal Auth0/RBAC | Header identity stub and service checks |
| Browser E2E suite | Manual guide plus API integration tests |

## 11. Related journeys

- MOD-510 uses provider-specific Gmail records and simulations.
- MOD-520 uses provider-specific Jira records and simulations.
- MOD-600 checks security policy and incidents around operational use.
- MOD-610 stores failure/replay and reliability evidence.

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Integrations desk loads | |
| Create & activate produces active connection | |
| Opaque credential reference shown; no raw secret | |
| Receive webhook stores synthetic event | |
| Receive inbox creates pending row | |
| Process OK creates mapping | |
| Force fail creates no mapping | |
| Health reflects failure where recorded | |
| Cross-org detail is hidden | |
| Stale version conflicts | |
| Audit/outbox evidence captured | |
| Live provider/broker claims explicitly excluded | |
| Automated test command result recorded | |
