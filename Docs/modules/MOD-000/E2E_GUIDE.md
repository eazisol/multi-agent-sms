# MOD-000 — Project Governance, Source Baseline, and Change Control

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | What to do here |
|---|---|
| First-time user | Learn what a “source baseline” is, then create a draft and open it. |
| QA | Run F-HAPPY through F-GATE. Check role hiding and human-only approve. |
| Developer | Confirm API, migration, immutability, and tests. |
| Owner | Confirm agents cannot approve. Approved records stay immutable. |

## 2. What this module is

MASMS must not guess what “the approved SRS” or “the approved architecture” is. This module is the **register of official documents**: each row points at an exact artifact path and version.

In daily language:

1. Someone **drafts** a baseline (“this file is our SRS candidate”).
2. They **submit** it and a reviewer **starts review**.
3. A **human** approves or rejects that exact version.
4. After approval, the row is **locked**. A later change is a new version or a change request — not a silent edit.

This module also stores architecture decision records (ADRs), governance change requests, requirement-to-module maps, and exact-version approval rows. The **Change Requests** sidebar item (`/change-requests`) is the later **MOD-420** product desk, not the MOD-000 governance CR API.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| Baseline list, create, detail, transitions | Implemented | Strongest role-aware UI in the app |
| ADR list, create, accept | Implemented | Accept requires human actor on the API |
| Governance CR + approval APIs | Implemented | No dedicated MOD-000 CR desk |
| Requirement mapping API | Implemented | No dedicated desk |
| Header identity | Stubbed | Not Auth0 |
| Temporal / notifications | Planned | Not in this module |
| Full RBAC middleware | Planned | UI role matrix is client-side for baselines |
| README “AC-901 pending” vs checklist Done | Contradiction | Treat M1 as accepted in the progress checklist; README is stale |

## 4. Requirements and dependencies

- Requirements: MVP-NFR-010, SRS Change Control
- Dependencies: none
- Downstream: almost every later module assumes an organization and, for release, approved baselines

## 5. How to start

1. Complete [MOD-010](../MOD-010/E2E_GUIDE.md) so API and web are running.
2. Open **Governance → Source Baselines**.
3. Set **Role** to **Contributor** for create/submit, **Baseline Approver** or **Admin** for approve/reject.
4. Keep the default organization/actor unless you are doing a tenant test.

## 6. Screens, buttons, and files

### Shared chrome

See [TESTING_CONVENTIONS.md](../../testing/TESTING_CONVENTIONS.md). **Create**, **Notifications**, and **AI** in the header do nothing. Use the desks below.

### Source Baselines list — `/governance/baselines`

Files: [`apps/web/src/app/governance/baselines/page.tsx`](../../../apps/web/src/app/governance/baselines/page.tsx), [`baseline-list-page.tsx`](../../../apps/web/src/components/baseline-list-page.tsx)

| Control | What happens | Status |
|---|---|---|
| New baseline | Goes to `/governance/baselines/new` if role `can create` | Implemented |
| Search (key or title) + Apply | Reloads list with `q` | Implemented |
| Status filter | draft / submitted / under_review / approved / rejected | Implemented |
| Table columns | Key, Title, Status, Version, Updated | Implemented |
| Key link | Opens detail | Implemented |
| Pagination | Limit/offset | Implemented |
| Empty state Create baseline | Same as New baseline | Implemented |
| Forbidden banner | Viewer still can view list; hidden create | Implemented (view_list is allowed for all current variants) |
| Loading | Skeleton rows | Implemented |

### Create baseline — `/governance/baselines/new`

File: [`baseline-create-page.tsx`](../../../apps/web/src/components/baseline-create-page.tsx)

| Field / button | Meaning |
|---|---|
| Back to source baselines | Returns to list |
| Baseline key | Unique business key, e.g. `BL-SRS-001` |
| Title | Human title |
| Artifact path | Repo or document path |
| Document version | Exact artifact version string |
| Classification | Default `internal` |
| Submit (create) | POST baseline as **draft**, then navigate to detail |
| Forbidden banner | Role cannot create (Viewer) |

### Baseline detail — `/governance/baselines/[id]`

File: [`baseline-detail-page.tsx`](../../../apps/web/src/components/baseline-detail-page.tsx)

| Control | When it shows | What happens |
|---|---|---|
| Summary / History tabs | Always | History lists audit-like events |
| Title + Save title | Draft only | PATCH; approved rows show immutability message |
| Submit | draft | Transition → `submitted` |
| Start review | submitted | Transition → `under_review` |
| Approve | under_review + approver role | Human-only API transition → `approved` |
| Approve (unavailable) | under_review without permission | Disabled / hidden per role matrix |
| Reject | under_review + approver role | Requires reason → `rejected` |
| 403 / 404 banners | Missing or other-org id | Strongest inline error UI in the product |

Role matrix: [`apps/web/src/lib/roles.ts`](../../../apps/web/src/lib/roles.ts)

| Role in header | Create/edit/submit | Approve/reject |
|---|---|---|
| Viewer | Hidden | Hidden |
| Contributor | Allowed | Hidden |
| Baseline Approver / Admin | Allowed | Allowed |
| Agent (draft only) | Allowed | Hidden (API also rejects agent approve) |

### Architecture Decisions — `/architecture-decisions`

File: [`architecture-decisions-desk-page.tsx`](../../../apps/web/src/components/architecture-decisions-desk-page.tsx)

| Control | What happens | Status |
|---|---|---|
| New ADR | Toggles Propose ADR form | Implemented |
| ADR key, Title, Context, Decision, Consequences | Required fields | Implemented |
| Create | POST as `proposed` | Implemented |
| Status filter | proposed / accepted / deprecated / superseded | Implemented |
| Accept | Human transition to `accepted` | Implemented |
| Pagination | Yes | Implemented |
| Detail workspace | — | Planned |

Governance change-request **API** has no matching sidebar desk. Product CRs are [MOD-420](../MOD-420/E2E_GUIDE.md).

## 7. API, data, and automated tests

Prefix: `/api/v1/governance`  
Router: [`apps/api/src/masms_api/modules/governance/router.py`](../../../apps/api/src/masms_api/modules/governance/router.py)  
Client: [`apps/web/src/lib/api.ts`](../../../apps/web/src/lib/api.ts) (`listBaselines`, `createBaseline`, `updateBaseline`, `transitionBaseline`, ADR helpers)  
Migration: [`migrations/versions/20260810_0001_mod000_governance.py`](../../../migrations/versions/20260810_0001_mod000_governance.py)

| Method | Path |
|---|---|
| POST/GET | `/baselines` |
| GET/PATCH | `/baselines/{id}` |
| POST | `/baselines/{id}/transitions` |
| GET | `/baselines/{id}/history` (client: `listBaselineHistory`) |
| POST/GET | `/requirement-mappings` |
| POST/GET | `/architecture-decisions` |
| POST | `/architecture-decisions/{id}/transitions` |
| POST/GET | `/change-requests` |
| POST | `/change-requests/{id}/transitions` |
| POST/GET | `/approvals` |

Tests:

- `tests/unit/governance/`
- `tests/integration/governance/test_governance_api.py`

```bash
uv run pytest tests/unit/governance tests/integration/governance -q --tb=short
```

## 8. Test flows

### F-SETUP

1. API and web running ([MOD-010](../MOD-010/E2E_GUIDE.md)).
2. Role = Contributor.
3. **Expected:** Source Baselines page loads; toast only if API is down.

### F-HAPPY — baseline lifecycle

1. Click **New baseline**.
2. Fill key `BL-E2E-001`, title `E2E baseline`, path `Docs/testing/README.md`, document version `0.1.0`.
3. Submit. **Expected:** detail page, status `draft`, version `1`.
4. **Save title** with a small edit. **Expected:** version increments; toast or silent refresh.
5. Click **Submit**. **Expected:** `submitted`.
6. Click **Start review**. **Expected:** `under_review`.
7. Switch Role to **Baseline Approver**.
8. Click **Approve**. **Expected:** `approved`; title editor gone; immutability message.
9. Open History tab. **Expected:** transition events with actor and timestamps.
10. Open **Audit Logs**. **Expected:** matching governance/audit rows (if writers are wired for this action).

Evidence: baseline id, statuses, version numbers, screenshot of approved lock.

### F-HAPPY — ADR

1. Open Architecture Decisions → **New ADR**.
2. Create with key `ADR-E2E-001` and short context/decision/consequences.
3. **Expected:** toast “ADR created as proposed”.
4. Switch to a human role (not Agent) and click **Accept**.
5. **Expected:** status `accepted`. Repeat as Agent: API must reject.

### F-VALIDATE

1. Create baseline with empty title (browser `required` should block).
2. API POST with duplicate `baseline_key`. **Expected:** conflict problem+json.

### F-AUTHZ

1. Role = Viewer. **Expected:** no **New baseline**; opening `/governance/baselines/new` shows forbidden banner.
2. Role = Agent (draft only), baseline `under_review`, click Approve if visible. **Expected:** UI hidden or API forbidden. Agents must not approve.

### F-TENANT

1. GET `/api/v1/governance/baselines/{id}` with a different `X-Organization-Id`. **Expected:** not found or forbidden, never the other tenant’s row.

### F-CONCUR

1. Load detail (note `version`).
2. Save title in another tab.
3. Submit from the first tab with stale version. **Expected:** conflict; no silent overwrite.

### F-TRANS

1. From `draft`, try to Approve (button should be absent). Direct API transition to `approved` skipping review. **Expected:** invalid transition.

### F-GATE

1. Approve is human-only and binds this row version.
2. After approve, PATCH title. **Expected:** rejected; message that approved baselines are immutable.

### F-TERM

1. `approved` and `rejected` are terminal for this version.
2. Reopening an approved baseline without a change-control process is **Planned / not in this desk**.

### F-RECOVER

N/A — no retry worker in MOD-000.

### F-CLEAN

Leave the E2E baseline and ADR in place as sample data. Do not delete audit history.

## 9. Security, privacy, and approvals

- Organization scope on every query.
- Approve/reject: human actor kind required on the server.
- Classification is stored; full classification-based authorization is later (MOD-120 / MOD-600).
- Do not put secrets in `artifact_path` or titles.
- Named production approvers remain a pending governance decision.

## 10. Planned versus implemented

| Target (design) | Today |
|---|---|
| Dedicated ADR/CR detail workspaces | ADR is a list desk; CR desk is MOD-420 |
| Auth0 login | Header stub |
| Requirement mapping UI | API only |
| Saved views / column picker | Planned |
| Browser E2E automation | None |

## 11. Related journeys

- [J-GOV](../../testing/CROSS_MODULE_JOURNEYS.md#j-gov-governance-register) — first official baseline
- [J-LEARN](../../testing/CROSS_MODULE_JOURNEYS.md#j-learn-first-hour) — first hour in the product

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| List loads with search, filter, pagination | |
| Viewer cannot create | |
| Contributor can create draft and submit | |
| Human approver can approve under_review | |
| Agent cannot approve | |
| Approved row is immutable | |
| Stale version conflicts | |
| Cross-org id does not leak | |
| ADR propose + human accept | |
| Unit/integration tests run (record command output) | |
