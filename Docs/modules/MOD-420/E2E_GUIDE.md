# MOD-420 — Risks, Change Requests, Impact, and Development Gate

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create and submit a scope change with impact. |
| QA | Test approval/rejection, stale versions, and the development gate. |
| Developer | Inspect the Phase 4 change-control API and integration test. |
| Owner | Ensure scope and commercial decisions remain human-only. |

## 2. What this module is

MOD-420 governs product risks and out-of-scope work through impact analysis, exact change-request decisions, development gating, and baseline-update records.

In this company it means a new client request is documented, its impact is assessed, and development stays blocked until an authorized human decides that exact change request.

This is distinct from the MOD-000 governance change-request API. The `/change-requests` desk uses MOD-420 `/api/v1/change-control`.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/change-requests` list/pagination | Implemented | Phase 4 product CR desk |
| **Create & submit** | Implemented shortcut | Creates scope CR, adds impact, submits |
| **Gate** | Implemented | Reads development gate |
| **Approve** / **Reject** | Implemented UI | Fixed rationale/evidence values |
| Human authorization in UI | Stubbed | Role selector is not login |
| Risk register/review | Implemented API | No desk controls |
| Baseline updates | Implemented API record | Does not mutate MOD-000/MOD-240 artifacts |
| Full CAB studio | Planned | No detailed review workspace |

## 4. Requirements and dependencies

- Phase: **Phase 4**, even if another checklist heading says Phase 3.
- Development gate and baseline updates require status `approved`.
- Rejected/deferred decisions retain rationale and evidence.
- Dependencies: API/web, organization identity, optional project, and authorized human decision-maker.
- Scope, quotation, discount, timeline, and commercial terms cannot be finalized by an agent.
- Outbox includes `changecontrol.cr.created`, `.cr.submitted`, `.cr.approved`, `.cr.rejected`, and `.baseline.updated`.

## 5. How to start

1. Start local services from [TESTING_CONVENTIONS.md](../../testing/TESTING_CONVENTIONS.md).
2. Open `http://localhost:3000/change-requests`.
3. Obtain a valid project UUID if testing project scope.
4. Use unique codes such as `CR-E2E-420-A` and `CR-E2E-420-R`.
5. Arrange a named authorized human for approval/rejection evidence.

## 6. Screens, buttons, and files

Desk: [`change-requests-desk-page.tsx`](../../../apps/web/src/components/change-requests-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| **New CR** | Toggles create form | Implemented | `change-requests-desk-page.tsx` |
| **Cancel** | Closes form | Implemented | same |
| **Create & submit** | Creates `scope` CR, adds impact, submits | Implemented shortcut | same |
| **Gate** | Displays status, allowed/blocked, and reason | Implemented | same |
| **Approve** | Records `approved`, `Desk approval`, `Owner sign-off` | Implemented; human-only decision | same |
| **Reject** | Records `rejected`, `Desk rejection`, `Out of capacity` | Implemented; human-only decision | same |
| Pagination | Changes list page | Implemented | same |
| Search/status/project filters | API only | Planned UI | router |

Fields are Code, Title, optional Project ID, and Impact summary. The desk hard-codes `change_type: scope` and affected area `scope`.

## 7. API, data, and automated tests

Prefix: `/api/v1/change-control`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/changecontrol/router.py)  
Integration test: [`test_changecontrol_api.py`](../../../tests/integration/changecontrol/test_changecontrol_api.py)  
Migration: `20260811_0026`

Important routes:

- `POST/GET /change-requests`
- `GET /change-requests/{id}`
- `POST/GET /change-requests/{id}/impacts`
- `POST /change-requests/{id}/submit`
- `POST/GET /change-requests/{id}/approvals`
- `GET /change-requests/{id}/development-gate`
- `POST/GET /change-requests/{id}/baseline-updates`
- `POST/GET /risks` and risk reviews

```bash
uv run pytest tests/integration/changecontrol -q --tb=short
```

The verification log’s one-test pass is historical; record the current run separately.

## 8. Test flows

For each step capture action, expected UI, expected persisted/audit state, and screenshot/API evidence.

### F-SETUP

1. Load `/change-requests`.
2. Record organization, actor kind, project, and authorized human approver.
3. Confirm the test is not using MOD-000 `/api/v1/governance/change-requests`.

### F-HAPPY

1. Click **New CR**.
2. Enter `CR-E2E-420-A`, title `Add approved reporting widget`, project ID, and impact.
3. Click **Create & submit**.
4. Expect `Change request submitted for approval` and `pending_approval`.
5. Click **Gate**; expect blocked with a reason.
6. Have the authorized human click **Approve**.
7. Expect `approved`; click **Gate** and expect allowed.
8. Use API to record a baseline update and ticket link; expect linked `to_version`, not mutation of the referenced source artifact.

### F-HAPPY — rejection

1. Create `CR-E2E-420-R` with a material scope impact.
2. Submit, then have the authorized human click **Reject**.
3. Expect `rejected`; API data retains rationale `Desk rejection` and evidence `Out of capacity`.
4. Click **Gate**; expect blocked.

### F-VALIDATE

1. Leave Code or Title empty; browser-required validation blocks.
2. Use an invalid Project ID; expect problem response/toast.
3. API-submit a draft without impact; expect validation/transition rejection if required by service.

### F-AUTHZ

1. Attempt **Approve** with agent identity or unauthorized human.
2. Backend must deny scope/commercial approval.
3. If accepted, fail and raise a governance defect; UI visibility is insufficient.

### F-TENANT

1. Create a CR under organization A.
2. Get/list/gate it under organization B.
3. Expect not found/forbidden and no leaked impact or decision.

### F-CONCUR

1. Note `pending_approval` version in two clients.
2. Decide in client A.
3. Decide with stale version in client B.
4. Expect conflict; only one decision persists.

### F-TRANS

1. API-create a draft.
2. Attempt a baseline update and inspect its gate.
3. Expect update conflict and gate blocked.
4. Attempt approval before submission; expect invalid transition.

### F-GATE

1. Inspect Gate before approval: blocked.
2. Inspect after authorized approval: allowed.
3. Verify approval references the exact CR/version.
4. Any material edit should create/supersede a version and require new approval.

### F-TERM

1. For rejected CR, attempt another decision or direct development entry.
2. Expect terminal behavior unless an authorized reopening process exists.
3. The current desk has no reopen button.

### F-RECOVER

N/A in the desk — no retry/reopen control. Create a corrected new CR/version through approved change control.

### F-CLEAN

1. Keep approved and rejected examples with evidence.
2. Do not delete append-only approvals/audit.
3. Record CR, impact, approval, baseline-update, artifact, and ticket IDs.

## 9. Security, privacy, and approvals

- Scope-affecting and commercial decisions are human-only.
- Approval must be server-enforced, tenant-scoped, and exact-version bound.
- Do not expose client pricing or sensitive rationale in test fixtures.
- Header identity and UI role are stubs.
- Baseline-update records are links/version bumps, not source-document mutation.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Full impact/CAB workspace | Compact combined form |
| Dynamic decision rationale/evidence | Desk uses fixed strings |
| Risk management UI | API only |
| Baseline artifact mutation workflow | Link/version record only |
| Strong authenticated approver selection | Planned |
| Browser E2E automation | Planned |

## 11. Related journeys

- [MOD-000 governance](../MOD-000/E2E_GUIDE.md) — separate governance CR API
- [MOD-240 requirements](../MOD-240/E2E_GUIDE.md)
- [MOD-430 releases](../MOD-430/E2E_GUIDE.md)
- [MOD-460 traceability](../MOD-460/E2E_GUIDE.md)

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Product CR desk/API distinction confirmed | |
| Create & submit adds impact | |
| Pending CR gate is blocked | |
| Authorized human can approve | |
| Approved gate is allowed | |
| Rejection retains rationale/evidence | |
| Draft baseline update is blocked | |
| Stale decision is rejected | |
| Agent/unauthorized approval is denied | |
| Cross-tenant CR is hidden | |
| Baseline update remains a record/link | |
| Integration test output recorded | |
