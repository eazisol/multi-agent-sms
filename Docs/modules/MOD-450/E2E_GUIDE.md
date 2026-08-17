# MOD-450 — Dashboard, Insights, Search, Filters, and Export Previews

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Read KPI cards, refresh insights, search, save a filter, and export. |
| QA | Reconcile counts, freshness, tenancy, and UI gaps. |
| Developer | Inspect Phase 4 insights APIs and integration tests. |
| Owner | Distinguish live-source counts from snapshots and previews. |

## 2. What this module is

MOD-450 provides an organization dashboard, on-demand reconciled snapshots, project-health records, indexed search, activity, saved filters, report definitions, and export previews.

In this company it means managers can see current counts and testers can create a JSON preview of metrics. It is not a streaming data warehouse, full-text engine, BI platform, or downloadable S3 export.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/` KPI cards and links | Implemented | Live module list counts |
| Dashboard **Refresh** | Implemented | Reloads all dashboard sources and refreshes insights |
| **Open Queries**, **Insights**, **View Projects** | Implemented navigation | Real links |
| `/insights` metric cards | Implemented | On-demand snapshot |
| **Refresh snapshot** | Implemented | Recomputes snapshot |
| Global **Search** | Implemented | Indexed documents only |
| **Save filter** | Implemented | Persists filter JSON |
| **Create export** | Implemented preview | In-DB JSON, not a file |
| Pagination on insights lists | Planned | API supports offsets; desk loads first 20 only |
| Scheduled/streaming refresh | Planned | On demand |

## 4. Requirements and dependencies

- Phase: **Phase 4**.
- Refresh reconciles organization-scoped source counts and reports `reconciled: true`.
- Snapshot is fresh under 60 seconds.
- Search and export are organization-scoped.
- Dependencies: API/web and seed records from Projects, Queries, Tickets, Bugs, Follow-ups, and Approvals.

## 5. How to start

1. Start services from [TESTING_CONVENTIONS.md](../../testing/TESTING_CONVENTIONS.md).
2. Seed known counts in the current organization.
3. Open `http://localhost:3000/`.
4. Open `/insights` in another tab.
5. Index at least one search document through the API because the desk has no indexing form.

## 6. Screens, buttons, and files

Dashboard: [`dashboard-page.tsx`](../../../apps/web/src/components/dashboard-page.tsx)  
Insights: [`insights-desk-page.tsx`](../../../apps/web/src/components/insights-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| KPI cards Projects/Approvals/Follow-ups/Queries | Navigate to desks | Implemented | dashboard |
| **Refresh** | Reloads source counts and refreshes insights | Implemented | dashboard |
| **Insights** | Navigates `/insights` | Implemented | dashboard |
| **Open Queries** | Navigates `/queries` | Implemented | dashboard |
| **View Projects** | Navigates `/projects` | Implemented | dashboard |
| Quick-start buttons | Navigate to Clients/Queries/Follow-ups/Approvals | Implemented | dashboard |
| **Refresh snapshot** | Recomputes snapshot | Implemented | insights |
| **Create export** | Creates ready JSON payload preview in DB | Implemented preview | insights |
| **Search** | Searches indexed titles/body | Implemented | insights |
| **Save filter** | Saves `insights` filter JSON | Implemented | insights |
| List pagination | Not rendered on activity/filter/export/search lists | Planned | insights |

The dashboard also shows Needs attention and Recent movement from loaded sets; those are not exhaustive historical reports.

## 7. API, data, and automated tests

Prefix: `/api/v1/insights`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/insights/router.py)  
Integration tests: [`test_insights_api.py`](../../../tests/integration/insights/test_insights_api.py)  
Migration: `20260811_0029`

Routes cover dashboard get/refresh, project health, saved filters, search index/query, activity, reports, and exports.

```bash
uv run pytest tests/integration/insights -q --tb=short
```

The verification log records two prior passes; this guide does not claim the current checkout passes until rerun.

## 8. Test flows

Capture action, expected UI, persisted snapshot/filter/export/audit, and screenshots or API responses.

### F-SETUP

1. Create two projects in organization A and one in B.
2. Index `SecretOrgAWidget` only under A.
3. Load `/` and `/insights` as organization A.
4. Record expected source totals.

### F-HAPPY — dashboard

1. Inspect Projects, Approvals, Follow-ups, and Queries KPI cards.
2. Click **Refresh**; expect cards and insights snapshot to reload without fatal page failure.
3. Compare Projects count with `/projects` total.
4. Click **Open Queries**; expect `/queries`.
5. Return and click **Insights**; expect `/insights`.

### F-HAPPY — insights

1. Click **Refresh snapshot**.
2. Expect Projects/Tickets open/Bugs open/Freshness cards, a current refreshed timestamp, `fresh`, and `reconciled=true`.
3. Search for `SecretOrgAWidget`; expect hit count toast and indexed result.
4. Enter filter name `Open E2E` and JSON `{"status":"open"}`; click **Save filter**.
5. Expect `Saved filter created` and the new private filter.
6. Click **Create export**.
7. Expect `Export ready (in-DB preview)` and a ready JSON export row.

### F-VALIDATE

1. Submit blank Search; expect no request/result mutation.
2. Submit saved filter without Name or Filter JSON; browser validation blocks.
3. Submit malformed filter JSON; expect backend validation if schema validates JSON.

### F-AUTHZ

1. Attempt shared filter/report/export mutations with an unauthorized actor.
2. Backend must enforce permissions where configured.
3. Treat UI role selection as display behavior only.

### F-TENANT

1. Search `SecretOrgAWidget` as organization B; expect zero.
2. Refresh B; expect one project, not A’s two.
3. List B exports; expect no A export ID or A organization payload.

### F-CONCUR

N/A — the desk exposes no versioned edit. Concurrent refreshes should create/return valid scoped snapshots without corrupting counts.

### F-TRANS

N/A — dashboard, search, saved filters, and ready preview exports have no visible status-transition workflow.

### F-GATE

N/A — analytics does not authorize release, scope, or commercial decisions. KPI values are decision support only.

### F-TERM

1. Create a ready export preview.
2. Confirm the desk offers no retry/download mutation.
3. Do not represent `ready` as an uploaded or delivered file.

### F-RECOVER

1. Stop or make one source API unavailable, then load `/`.
2. Dashboard uses settled requests and should preserve available sections while showing error toasts for failures.
3. Restore API and click **Refresh**.

### F-CLEAN

1. Keep snapshots/exports needed for evidence.
2. Delete disposable saved filters via API if authorized.
3. Do not delete audit history; record IDs and expected totals.

## 9. Security, privacy, and approvals

- Search index and export preview must be organization-scoped.
- Classification is displayed; authorization must not rely on display alone.
- Do not index secrets or unnecessary client PII.
- Export preview is sensitive data and must remain scoped.
- Metrics and reports do not grant approval authority.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Streaming/scheduled dashboard | On-demand refresh |
| Full-text enterprise search | Indexed document matching |
| S3/download artifact | In-DB payload preview |
| BI/OLAP warehouse | Transactional snapshot records |
| Pagination controls on insights lists | Missing/Planned |
| Search indexing UI | API only |

## 11. Related journeys

- [MOD-160 projects](../MOD-160/E2E_GUIDE.md)
- [MOD-170 queries](../MOD-170/E2E_GUIDE.md)
- [MOD-410 bugs](../MOD-410/E2E_GUIDE.md)
- [MOD-440 notifications](../MOD-440/E2E_GUIDE.md)

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Dashboard KPI cards reconcile | |
| Refresh updates snapshot | |
| Open Queries navigates correctly | |
| Insights snapshot is fresh/reconciled | |
| Indexed global search finds A record | |
| Organization B search returns none | |
| Saved filter persists | |
| Export preview is ready and org-scoped | |
| Export described as in-DB preview | |
| Insights pagination gap recorded Planned | |
| Partial dashboard failure can recover | |
| Integration test output recorded | |
