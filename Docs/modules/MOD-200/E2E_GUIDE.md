# MOD-200 — Client and Contact Management

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Add a client and find it in the inventory. |
| QA | Verify create, search, status filtering, paging, and isolation. |
| Developer | Trace the desk to the clients API and tests. |
| Owner | Understand which contact and merge capabilities are API-only. |

## 2. What this module is

This module is the organization’s client register. It stores client companies and, through API-only capabilities, their contacts, communication preferences, project roles, duplicate suggestions, and merge history.

In this company it means: create “Acme Corporation” once, use that client as the anchor for later queries and projects, and preserve evidence if a duplicate client is merged.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/clients` inventory and create form | Implemented | Current source supersedes README’s stale “FE deferred” note. |
| Search, status filter, total, table, pagination | Implemented | Server-backed list. |
| Contacts, preferences, project contacts, duplicate and merge APIs | Implemented | No controls on the current desk. |
| **Import with AI** | Planned | Visible only in the empty state; it has no click handler. |
| Client detail route | Planned | Rows are not links; no detail page exists. |
| Automatic duplicate detection | Planned | Manual suggestion API only. |
| Header identity | Stubbed | Header actor fields are not login. |
| Human M1 acceptance | Blocked | AC-901 is not recorded in VERIFICATION.md. |

## 4. Requirements and dependencies

- Acceptance focus: multiple contacts with authority, merge snapshot history, organization/client isolation, and create/merge audit.
- Runtime dependency: MOD-010 local API/web setup.
- Downstream: MOD-210 queries and MOD-240 projects.
- Optional API setup: a second client is needed to exercise duplicate and merge endpoints.
- Browser workspace does not store a client id.

## 5. How to start

1. Start the shared environment using [TESTING_CONVENTIONS.md](../../testing/TESTING_CONVENTIONS.md).
2. Open `http://localhost:3000/clients`.
3. Use **Contributor** or **Admin** to expose **New client**.
4. Keep browser developer tools open for the API response and record id.
5. Use synthetic client names only.

## 6. Screens, buttons, and files

Screen: `/clients`  
Desk: [`clients-desk-page.tsx`](../../../apps/web/src/components/clients-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| New client | Toggles the create card for roles that can create. | Implemented | `clients-desk-page.tsx` |
| Client name | Required legal/trading name; also proposes a short code. | Implemented | `clients-desk-page.tsx` |
| Industry | Optional free text. | Implemented | `clients-desk-page.tsx` |
| Short code | Required; accepts lowercase letters, digits, `_`, `-`. | Implemented | `clients-desk-page.tsx` |
| Cancel | Closes the create card without saving. | Implemented | `clients-desk-page.tsx` |
| Create client | POSTs the client, closes the form, and reloads the list. | Implemented | `clients-desk-page.tsx` |
| Search name, code, or industry | Sends `q`; resets to the first page. | Implemented | `clients-desk-page.tsx` |
| Status | Filters Any, Active, Inactive, Prospect, or Archived. | Implemented | `clients-desk-page.tsx` |
| Match count | Shows server-reported total. | Implemented | `clients-desk-page.tsx` |
| Client table | Shows Client/code, Industry, Status, Created. | Implemented | `clients-desk-page.tsx` |
| Client row | Displays data only; it does not navigate. | Implemented | `clients-desk-page.tsx` |
| Pagination | Changes offset and page size. | Implemented | `list-pagination.tsx` |
| Add client | Empty-state shortcut to the create card. | Implemented | `clients-desk-page.tsx` |
| Import with AI | No handler and no provider call. | Planned | `clients-desk-page.tsx` |

Shared header **Create**, notification bell, and **AI** are not module actions; see the conventions.

## 7. API, data, and automated tests

Prefix: `/api/v1/clients`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/clients/router.py)  
Migration: `20260811_0009`

| Method | Path | Current surface |
|---|---|---|
| POST / GET | `/api/v1/clients` | UI + API |
| POST | `/api/v1/clients/contacts` | API only |
| GET | `/api/v1/clients/{client_id}/contacts` | API only |
| POST | `/api/v1/clients/project-contacts` | API only |
| POST | `/api/v1/clients/preferences` | API only |
| POST | `/api/v1/clients/duplicates` | API only |
| POST | `/api/v1/clients/merge` | API only |

Tests:

- [`tests/unit/clients/test_clients_domain.py`](../../../tests/unit/clients/test_clients_domain.py)
- [`tests/integration/clients/test_clients_api.py`](../../../tests/integration/clients/test_clients_api.py)

```bash
uv run pytest tests/unit/clients tests/integration/clients -q --tb=short
```

## 8. Test flows

Each implemented step records the screen/toast, client id/status, relevant API JSON, and audit evidence if present.

### F-SETUP

1. Start API and web; open `/clients`.
2. Set Role to Contributor.
3. Expected UI: inventory loads without an error toast.
4. Expected data: `GET /api/v1/clients` returns a paged envelope.
5. Evidence: URL, role, response status, initial total.

### F-HAPPY

1. Click **New client**.
2. Enter Client name `E2E Acme 200`, Industry `Technology`, Short code `e2e-acme-200`.
3. Click **Create client**.
4. Expected UI: success toast, form closes, row appears.
5. Expected data: new client has organization ownership, `active` status, id, and timestamps.
6. Search `e2e-acme-200`; expected one matching row.
7. Select **Active**; expected the row remains.
8. Change page size if available; expected pagination metadata changes.
9. Evidence: toast, row, id, list query parameters.

### F-VALIDATE

1. Leave Client name empty; browser required validation must block submit.
2. Enter invalid Short code `Bad Code!`; pattern validation must block submit.
3. POST a duplicate code directly; expect a conflict/validation problem, not a second record.
4. Evidence: browser message and problem JSON.

### F-AUTHZ

1. Set Role to Viewer; **New client** and empty-state **Add client** should be hidden.
2. UI role hiding is not backend authentication.
3. Attempt unauthorized API mutation with an unapproved actor context; expect denial if policy applies.
4. Evidence: hidden control and API response.

### F-TENANT

1. Create contacts for two synthetic clients by API.
2. Send `X-Client-Id` for client A while listing client B contacts.
3. Expected data: `403`; no client B contact payload.
4. Repeat list with another organization id; no cross-organization rows may appear.
5. Evidence: headers, status code, redacted response.

### F-CONCUR

N/A — the current client create/list UI has no update action or `expected_version` contract.

### F-TRANS

N/A — status transitions are not exposed on this desk.

### F-GATE

N/A — creating a client is not a human-only approval. A real merge should still be treated as controlled because it changes identity history.

### F-TERM

1. Use the merge API with two synthetic clients and a reason.
2. Expected data: merged client disappears from active list; snapshot remains in merge history.
3. No delete or reopen control exists on `/clients`.
4. Evidence: pre/post lists and merge response.

### F-RECOVER

1. Stop the API or use an invalid API URL.
2. Reload `/clients`.
3. Expected UI: “Unable to load clients” toast and empty list state.
4. Restore API and reload; data returns without recreating records.

### F-CLEAN

Leave synthetic records labeled `E2E`; do not delete audit or merge history. Clear search/status and record ids for later module journeys.

## 9. Security, privacy, and approvals

- Use synthetic contacts; names, emails, and commercial context can be personal/confidential data.
- Organization and optional client scope must be enforced server-side.
- Merge history preserves a snapshot and should not be edited.
- Do not treat the Role dropdown as proof of identity.
- No approval is finalized by this guide; AC-901 remains a human decision.

## 10. Planned versus implemented

| Target design | Current behavior |
|---|---|
| Rich client workspace | Flat paginated table only |
| Client detail and contact editor | API only; no detail route |
| AI import and duplicate detection | Nonfunctional button/manual API |
| Authenticated RBAC | Header identity stub |
| Browser E2E automation | Not present |

## 11. Related journeys

- [Testing journeys](../../testing/CROSS_MODULE_JOURNEYS.md)
- Continue to [MOD-210](../MOD-210/E2E_GUIDE.md) to capture and qualify an inquiry.
- Continue to [MOD-240](../MOD-240/E2E_GUIDE.md) to create a delivery project.

## 12. Pass / fail checklist

| Check | Result (pass / fail / skip / blocked) |
|---|---|
| `/clients` loads a paginated table | |
| New client form exposes all three real fields | |
| Required and short-code validation blocks invalid submit | |
| Created row persists after reload | |
| Search and status filter affect server results | |
| Viewer create controls are hidden | |
| No client row falsely navigates to a detail route | |
| Import with AI recorded as Planned/non-testable | |
| Cross-client and cross-organization access does not leak | |
| Merge snapshot API behavior checked if in scope | |
| Automated tests command and actual result recorded | |
