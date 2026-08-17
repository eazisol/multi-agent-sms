# MOD-240 — Projects, Requirements, Versions, and SRS Management

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create a project and one must-have requirement. |
| QA | Verify project filters, requirement gates, SRS approval, and immutability. |
| Developer | Trace UI shortcuts to separate requirement and SRS APIs. |
| Owner | Confirm the final SRS remains a human-only exact-version gate. |

## 2. What this module is

This module creates delivery projects, gives requirements stable codes, stores versioned statements and acceptance criteria, and produces authoritative SRS baselines only after approval.

In this company it means: create project `E2E-PORTAL`, draft `REQ-001`, approve its complete version, then have a named human approve the SRS containing that exact version.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/projects` create, search, status, selection, pagination | Implemented | Current UI exists despite stale README. |
| Embedded requirement table and draft form | Implemented | Creates requirement, v1 must-have statement, and fixed AC-1. |
| Approve last version | Implemented | Available only for the most recently created version in this session. |
| Create & approve SRS | Implemented shortcut | Two API calls; target requires separate human approval. |
| Business rules, assumptions, constraints | Implemented API only | No desk fields. |
| Multi-tab project workspace | Planned | Current page is inventory + embedded requirement area. |
| Requirement/SRS detail history | Planned in UI | No detail workspace. |
| Header identity | Stubbed | Not login. |
| Human M1 acceptance | Blocked | AC-901 not obtained. |

## 4. Requirements and dependencies

- MOD-010 supplies runtime.
- A client/brief is conceptually upstream, but current create form asks only code/title.
- Selected project persists as `masms.workspace.projectId`.
- MOD-230, MOD-250, and MOD-260 consume that workspace project.
- Requirement approval requires a unique project code and acceptance criterion.
- SRS approval is human-only and must reference approved requirement versions.

## 5. How to start

1. Start shared API/web.
2. Open `/projects`.
3. Use Contributor to create/draft.
4. Use Baseline Approver/Admin as the named human for approve actions.
5. Clear `masms.workspace.projectId` if stale selection is confusing.

## 6. Screens, buttons, and files

Screen: `/projects`  
Desk: [`projects-desk-page.tsx`](../../../apps/web/src/components/projects-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| New project | Toggles create form. | Implemented | `projects-desk-page.tsx` |
| Project code | Required; transformed to uppercase before POST. | Implemented | `projects-desk-page.tsx` |
| Title | Required project title. | Implemented | `projects-desk-page.tsx` |
| Cancel | Closes project form. | Implemented | `projects-desk-page.tsx` |
| Create project | Creates and selects workspace project. | Implemented | `projects-desk-page.tsx` |
| Search code or title | Server `q` filter. | Implemented | `projects-desk-page.tsx` |
| Status | Any, Active, Draft, On hold, At risk, Blocked, Completed, Cancelled. | Implemented | `projects-desk-page.tsx` |
| Project row | Selects project and stores workspace id. | Implemented | `projects-desk-page.tsx` |
| Pagination | Changes project offset/page size. | Implemented | `list-pagination.tsx` |
| Draft requirement | Toggles embedded form. | Implemented | `projects-desk-page.tsx` |
| Requirement code | Required, default `REQ-001`. | Implemented | `projects-desk-page.tsx` |
| Requirement Title | Required. | Implemented | `projects-desk-page.tsx` |
| Statement | Required multiline “system shall” text. | Implemented | `projects-desk-page.tsx` |
| Create draft | Creates requirement, v1 must-have version, and fixed AC-1. | Implemented | `projects-desk-page.tsx` |
| Approve last version | Approves only `lastVersion` held in UI state. | Implemented | `projects-desk-page.tsx` |
| Create & approve SRS | Creates “Project SRS” from last approved version, then approves. | Implemented shortcut | `projects-desk-page.tsx` |
| Requirements table | Code, Title, Status for selected project. | Implemented | `projects-desk-page.tsx` |

The page is not a multi-tab workspace and exposes no project status-transition controls.

## 7. API, data, and automated tests

Prefix: `/api/v1/projects`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/projects/router.py)  
Migration: `20260811_0013`

| Method | Path |
|---|---|
| POST / GET | `/api/v1/projects` |
| GET | `/api/v1/projects/{project_id}` |
| POST | `/api/v1/projects/requirements` |
| GET | `/api/v1/projects/{project_id}/requirements` |
| POST | `/api/v1/projects/requirement-versions` |
| POST | `/api/v1/projects/requirement-versions/{id}/approve` |
| POST | `/api/v1/projects/business-rules` |
| POST | `/api/v1/projects/acceptance-criteria` |
| POST | `/api/v1/projects/assumptions` |
| POST | `/api/v1/projects/constraints` |
| POST | `/api/v1/projects/srs-baselines` |
| POST | `/api/v1/projects/srs-baselines/{id}/approve` |

Tests: [`tests/unit/projects`](../../../tests/unit/projects), [`tests/integration/projects/test_projects_api.py`](../../../tests/integration/projects/test_projects_api.py)

```bash
uv run pytest tests/unit/projects tests/integration/projects -q --tb=short
```

## 8. Test flows

Capture project/requirement/version/SRS ids, workspace key, statuses, approval actors, errors, and audit evidence.

### F-SETUP

1. Open `/projects`; Role = Contributor.
2. Clear search/status.
3. Expected: project inventory loads as a paged list.
4. Evidence: initial total and workspace project id.

### F-HAPPY

1. Click **New project**.
2. Project code `e2e-portal-240`; Title `E2E Portal Project 240`.
3. Click **Create project**.
4. Expected: code `E2E-PORTAL-240`, selected row, workspace id saved.
5. Click **Draft requirement**.
6. Enter `REQ-E2E-240`, title `Synthetic login`, statement `The system shall support synthetic login testing.`
7. Click **Create draft**; expect draft-ready toast and table row.
8. Switch to authorized human role; click **Approve last version**.
9. Expected: requirement version approved.
10. Click **Create & approve SRS**.
11. Expected: SRS version 1 approved toast; API row has human approver.
12. Search and status-filter the project; verify pagination.

### F-VALIDATE

1. Empty project code/title must be browser-blocked.
2. Empty requirement code/title/statement must be blocked.
3. Duplicate requirement code in the same project must conflict.
4. Directly approve a requirement version without acceptance criteria; expect `422`.
5. Note: the UI shortcut automatically creates fixed `AC-1`.

### F-AUTHZ

1. Viewer should not see create or draft controls.
2. Contributor sees approval controls disabled under current role matrix.
3. Send SRS approve with `X-Actor-Kind: agent`; expect denial.
4. A header Role visual change is not identity proof.

### F-TENANT

1. GET project and requirements under another organization.
2. Expected: not found/forbidden and no titles/statements leak.
3. Attempt to attach another tenant’s requirement version to SRS; expect rejection.

### F-CONCUR

N/A in current UI — no `expected_version`. Approved requirement versions are immutable; create v2 for change.

### F-TRANS

1. Click/create SRS before the last requirement version is approved.
2. UI should show “Approve a requirement version…” and not POST SRS.
3. Direct API SRS with unapproved version must fail.
4. New requirement version after v1 without `change_reason` must fail.

### F-GATE

1. Requirement version approval requires acceptance criterion.
2. SRS draft creation and SRS approval are distinct API calls.
3. A named human approves the exact SRS id/version.
4. Record `approved_by_actor_id`; agent approval must fail.
5. Treat the combined UI action as a known shortcut, not target governance.

### F-TERM

1. After requirement approval, add another acceptance criterion through API.
2. Expected: `403`; approved version unchanged.
3. Material changes create v2 with `change_reason`.
4. Approved SRS is authoritative and must not be silently edited.
5. Completed/cancelled project terminal behavior is not controlled by this desk.

### F-RECOVER

1. Fail acceptance-criterion creation during **Create draft**.
2. Inspect API: requirement/version may exist because the shortcut is sequential.
3. Fail SRS approval after SRS creation.
4. Inspect for a draft SRS before retry to avoid duplicate baselines.

### F-CLEAN

Keep synthetic project, approved requirement, and SRS evidence. Preserve workspace project for MOD-250/MOD-260. Do not delete audit/approval history.

## 9. Security, privacy, and approvals

- Project requirements can contain confidential scope; use synthetic text.
- Backend organization/project scope is mandatory.
- Approved requirement versions and SRS baselines are immutable.
- Final SRS approval is human-only, exact-version, and cannot be delegated to an agent here.
- This guide does not approve project scope or client commitments.

## 10. Planned versus implemented

| Target design | Current behavior |
|---|---|
| Multi-tab project workspace | Single inventory/detail split |
| Separate SRS submit/review/approve | Combined create-and-approve shortcut |
| Full requirement editor | Fixed must-have v1 + fixed AC-1 |
| Rules/assumptions/constraints UI | API only |
| Change-request-linked versioning | `change_reason` API only |

## 11. Related journeys

- Inputs: [MOD-230](../MOD-230/E2E_GUIDE.md)
- Documents: [MOD-250](../MOD-250/E2E_GUIDE.md)
- Roadmap: [MOD-260](../MOD-260/E2E_GUIDE.md)
- Shared: [Cross-module journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

## 12. Pass / fail checklist

| Check | Result (pass / fail / skip / blocked) |
|---|---|
| Project creates and becomes workspace project | |
| Search/status/pagination work | |
| All actual project/requirement fields tested | |
| Draft creates requirement, v1, and AC-1 | |
| Approval without AC is rejected by API | |
| Human approves exact requirement version | |
| SRS cannot use unapproved version | |
| Agent cannot approve final SRS | |
| Approved version rejects mutation | |
| Multi-tab workspace recorded Planned | |
| Cross-tenant project content does not leak | |
| Automated tests command and result recorded | |
