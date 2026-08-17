# MOD-210 — Client Queries, Qualification, and Opportunities

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Capture an inquiry, qualify it, and convert it. |
| QA | Test statuses, SLA display, search, filters, conversion, and inbox aggregation. |
| Developer | Trace three desks to the queries API and integration test. |
| Owner | Distinguish actual qualification controls from planned AI support. |

## 2. What this module is

This module records inbound client inquiries, moves them through qualification, and converts qualified work into an opportunity without losing the original trail.

In this company it means: save “Need a field-service portal,” classify it, qualify it, then create one commercial opportunity linked to the original query.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/queries` create, search, status/SLA tabs, paging, selection | Implemented | Current UI exists despite stale README. |
| `received → classified → qualifying → qualified` controls | Implemented | Classification is automatically `new_build` in the first action. |
| `/opportunities` qualified-query conversion, status filter, paging | Implemented | Estimated value and notes are optional. |
| `/inbox` query/notification/Gmail aggregation | Implemented | Read-only lists and links to source desks. |
| Generate clarifying questions | Planned | Button has no handler. |
| Qualification-answer editor and first-response control | Planned in UI | APIs exist; no desk controls. |
| Gmail provider | Stubbed/Blocked | Inbox tolerates unavailable Gmail; live connection is separate. |
| Header identity | Stubbed | Not login. |
| Human M1 acceptance | Blocked | AC-901 not obtained. |

## 4. Requirements and dependencies

- Start with MOD-010 runtime; a MOD-200 client is useful but the current query form does not select one.
- Query ids persist as `masms.workspace.queryId` in [`workspace.ts`](../../../apps/web/src/lib/workspace.ts).
- MOD-220 uses the selected query when opening a conversation.
- MOD-230 prefers the selected query for requirement gathering.
- Conversion requires a query in `qualified`.

## 5. How to start

1. Start API and web using the shared conventions.
2. Open `/queries` with Contributor or Admin.
3. Clear `masms.workspace.queryId` if an unexpected inquiry remains selected.
4. Also open `/opportunities` and `/inbox` in separate tabs.
5. Use synthetic inquiry text without client secrets.

## 6. Screens, buttons, and files

### Queries — `/queries`

File: [`queries-desk-page.tsx`](../../../apps/web/src/components/queries-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| New inquiry | Toggles Capture inquiry form. | Implemented | `queries-desk-page.tsx` |
| Subject | Required inquiry subject. | Implemented | `queries-desk-page.tsx` |
| Summary | Required multiline summary. | Implemented | `queries-desk-page.tsx` |
| Cancel | Closes form. | Implemented | `queries-desk-page.tsx` |
| Save inquiry | Creates a web source if needed, then a `received` query. | Implemented | `queries-desk-page.tsx` |
| All / New / Classified / Qualifying / Qualified | Status tabs; reset offset. | Implemented | `queries-desk-page.tsx` |
| Overdue | Filters `sla_status=breached`. | Implemented | `queries-desk-page.tsx` |
| Search subject or summary | Server `q` filter. | Implemented | `queries-desk-page.tsx` |
| Inquiry row | Selects detail and stores workspace query id. | Implemented | `queries-desk-page.tsx` |
| Pagination | Offset and page-size controls. | Implemented | `list-pagination.tsx` |
| Mark classified | `received → classified`, classification `new_build`. | Implemented | `queries-desk-page.tsx` |
| Start qualifying | `classified → qualifying`. | Implemented | `queries-desk-page.tsx` |
| Mark qualified | `qualifying → qualified`. | Implemented | `queries-desk-page.tsx` |
| Generate clarifying questions | No click handler. | Planned | `queries-desk-page.tsx` |

### Opportunities — `/opportunities`

File: [`opportunities-desk-page.tsx`](../../../apps/web/src/components/opportunities-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| Convert query | Toggles conversion form. | Implemented | `opportunities-desk-page.tsx` |
| Qualified query | Required select populated from qualified queries. | Implemented | `opportunities-desk-page.tsx` |
| Opportunity title | Required. | Implemented | `opportunities-desk-page.tsx` |
| Estimated value | Optional text sent to API decimal field. | Implemented | `opportunities-desk-page.tsx` |
| Conversion notes | Optional text. | Implemented | `opportunities-desk-page.tsx` |
| Convert | Creates opportunity and transitions query to converted. | Implemented | `opportunities-desk-page.tsx` |
| All statuses / open | Filters opportunity list. | Implemented | `opportunities-desk-page.tsx` |
| Pagination | Offset and page size. | Implemented | `list-pagination.tsx` |

### Inbox — `/inbox`

File: [`inbox-desk-page.tsx`](../../../apps/web/src/components/inbox-desk-page.tsx)

| Control | What it does | Status |
|---|---|---|
| Queries heading | Links to `/queries`. | Implemented |
| Notifications heading | Links to `/notifications`. | Implemented |
| Gmail heading | Links to `/gmail`. | Implemented |
| Three lists | Show up to 20 recent records each. | Implemented, read-only |

## 7. API, data, and automated tests

Prefix: `/api/v1/queries`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/queries/router.py)  
Migration: `20260811_0010`

| Method | Path |
|---|---|
| POST | `/sources` |
| GET / POST | `/` |
| GET | `/opportunities` |
| GET | `/{query_id}` |
| POST | `/{query_id}/transitions` |
| POST | `/{query_id}/first-response` |
| POST / GET | `/qualification-answers`, `/{query_id}/qualification-answers` |
| POST | `/{query_id}/convert` |
| GET | `/{query_id}/history` |

Tests: [`tests/unit/queries`](../../../tests/unit/queries), [`tests/integration/queries/test_queries_api.py`](../../../tests/integration/queries/test_queries_api.py)

```bash
uv run pytest tests/unit/queries tests/integration/queries -q --tb=short
```

## 8. Test flows

Capture UI/toasts, query and opportunity ids, each status, history JSON, and relevant audit/outbox evidence.

### F-SETUP

1. Start services and open `/queries`.
2. Role = Contributor; clear filters.
3. Expected data: paged query list; workspace key may select a prior row.
4. Evidence: initial response and localStorage query id.

### F-HAPPY

1. Click **New inquiry**.
2. Subject `E2E Field Portal 210`; Summary `Synthetic qualification journey`.
3. Click **Save inquiry**; expect “Inquiry captured,” status `received`.
4. Select the row and click **Mark classified**; expect `classified`.
5. Click **Start qualifying**; expect `qualifying`.
6. Click **Mark qualified**; expect `qualified`.
7. Open `/opportunities`, click **Convert query**.
8. Select the query, enter title `E2E Field Portal Opportunity`, value `50000.00`, notes `Synthetic E2E`.
9. Click **Convert**; expect success and one `open` opportunity.
10. Query history API must contain `received`, intermediate states, and `converted`.
11. Open `/inbox`; expect the query in the read-only Queries card if within the latest 20.

### F-VALIDATE

1. Submit empty Subject or Summary; browser required validation blocks.
2. Conversion with no qualified query keeps **Convert** disabled.
3. Use invalid estimated value by API; expect validation problem.
4. Evidence: field state and problem JSON.

### F-AUTHZ

1. Viewer should not see **New inquiry**.
2. Agent/header identity must not be treated as a human authorization system.
3. Attempt protected transitions with an unauthorized context; expect denial where policy applies.

### F-TENANT

1. Read the query id under another organization header.
2. Expected: not found/forbidden and no subject or summary leak.
3. Repeat opportunity list; only current organization rows appear.

### F-CONCUR

N/A — current transition requests do not expose `expected_version` in the desk.

### F-TRANS

1. Directly attempt `received → qualified`.
2. Expected: invalid transition; status remains `received`.
3. Try converting a non-qualified query.
4. Expected: conversion rejected and no opportunity created.

### F-GATE

N/A — qualification and conversion are not listed human-only approval actions. Commercial terms remain subject to separate governance.

### F-TERM

1. After conversion, the query is `converted`.
2. Current UI exposes no further query action or reopen.
3. Re-conversion must not silently create duplicate opportunities.

### F-RECOVER

1. Make Gmail unavailable and open `/inbox`.
2. Expected: Gmail list becomes empty while query/notification aggregation can still load.
3. Make the queries API unavailable; expect “Unable to load inbox” or “Unable to load inquiries.”
4. Restore and reload without recreating records.

### F-CLEAN

Leave labeled synthetic query/opportunity records and history. Clear filters; retain the query workspace id if continuing to MOD-220 or MOD-230.

## 9. Security, privacy, and approvals

- Inquiry text can contain client data; use minimum synthetic content.
- Every list/detail/transition must remain organization-scoped.
- Original-message preservation and qualification evidence are append-only traceability concerns.
- “Generate clarifying questions” must not be reported as AI-tested.
- Conversion does not approve final quotation, scope, or timeline.

## 10. Planned versus implemented

| Target design | Current behavior |
|---|---|
| Full qualification worksheet | Status buttons only; answers API-only |
| AI clarification generation | Nonfunctional button |
| Durable SLA workflow | Row fields; Temporal wait deferred |
| Rich opportunity workspace | List + conversion form |
| Unified actionable inbox | Read-only aggregation |

## 11. Related journeys

- Previous: [MOD-200](../MOD-200/E2E_GUIDE.md)
- Next: [MOD-220](../MOD-220/E2E_GUIDE.md) for communication.
- Next: [MOD-230](../MOD-230/E2E_GUIDE.md) for discovery questions.
- Shared: [Cross-module journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

## 12. Pass / fail checklist

| Check | Result (pass / fail / skip / blocked) |
|---|---|
| Inquiry saves as `received` | |
| Search, tabs, SLA display, and pagination work | |
| Status path follows received → classified → qualifying → qualified | |
| Invalid transition is rejected | |
| Qualified query converts once to an open opportunity | |
| Query history preserves conversion evidence | |
| Workspace query id follows selection | |
| Inbox is read-only and links to source desks | |
| Clarifying-question button recorded Planned | |
| Cross-organization records do not leak | |
| Automated tests command and result recorded | |
