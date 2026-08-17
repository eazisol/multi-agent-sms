# MOD-330 — Human Approval Gates and Exact-Version Decisions

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Submit a versioned request and find it in the queue. |
| QA | Test approve, reject, withdraw, evidence, roles, and exact-version gates. |
| Developer | Trace the desks to approval APIs and append-only decisions. |
| Owner | Verify only authorized humans decide. |

## 2. What this module is

Approval gates freeze the target entity and version, assign ordered human steps, collect evidence, and keep every decision.

In this company it means “approve the SRS” refers to one exact version. An edit requires a new/superseding request; an agent may recommend but cannot decide.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/approvals` queue and detail | **Implemented** | Create, filter, search, paginate, decide, evidence, steps/history |
| `/my-work` pending approvals | **Implemented** | Read-only summary linking to Approvals |
| Gate check/assert | **Implemented API** | Exact target version |
| Delegation/override/supersede | **Implemented API** | No controls in current desk |
| Request changes decision | **Planned** | No button/API decision value documented in desk |
| Temporal approval wait | **Planned** | No live durable wait |
| Header identity/role selector | **Stubbed** | Role hiding is not authentication |
| Human Done approval | **Blocked** | Module AC-901 not obtained |

## 4. Requirements and dependencies

- Requires a real target entity ID and exact integer target version.
- Request captures action code and ordered step snapshot.
- Only humans decide; recommendation source cannot self-approve.
- Reject and withdraw require reasons.
- Material target edits supersede/invalidate prior approval.

## 5. How to start

1. Start API/web and create/select a query or project.
2. Record the target’s current version.
3. Open `/approvals`; use Contributor/Admin to submit.
4. Open `/my-work` to confirm the pending summary.
5. Use Baseline Approver/Admin for a human decision.

## 6. Screens, buttons, and files

| Control | What it does | Status | Source file |
|---|---|---|---|
| New approval | Opens submission form | Implemented | `approvals-desk-page.tsx` |
| Submit request | Creates exact-version request with one approver step | Implemented | `approvals-desk-page.tsx` |
| All/Pending/Approved/Rejected | Filters queue | Implemented | `approvals-desk-page.tsx` |
| Search title or action | Applies query | Implemented | `approvals-desk-page.tsx` |
| Pagination | Changes limit/offset | Implemented | `approvals-desk-page.tsx` |
| Approval row | Loads steps and decision history | Implemented | `approvals-desk-page.tsx` |
| Approve | Records human approval | Implemented | `approvals-desk-page.tsx` |
| Reject | Records rejection; reason required | Implemented | `approvals-desk-page.tsx` |
| Withdraw | Withdraws pending request; reason required | Implemented | `approvals-desk-page.tsx` |
| Attach evidence | Adds evidence reference | Implemented | `approvals-desk-page.tsx` |
| Request changes | No control | Planned | — |
| My Work → Pending approvals | Read-only list/link | Implemented | `my-work-desk-page.tsx` |

## 7. API, data, and automated tests

Router: [`router.py`](../../../apps/api/src/masms_api/modules/approvalgates/router.py)  
Prefix: `/api/v1/approvals`

| Method | Path | Purpose |
|---|---|---|
| POST/GET | `/approvals` | Create/list |
| GET | `/approvals/{id}` | Read request |
| GET | `/{id}/workflow`, `/{id}/steps` | Frozen workflow detail |
| POST/GET | `/{id}/decisions` | Decide/history |
| POST/GET | `/{id}/evidence` | Evidence |
| POST | `/gate-check`, `/gate-assert` | Test/enforce gate |
| POST/GET | `/delegations` | Delegate/list |
| POST | `/delegations/{id}/revoke` | Revoke |
| POST | `/overrides` | Emergency override |
| POST | `/{id}/supersede` | Invalidate on material change |

Tests:

- `tests/unit/approvalgates/test_approvalgates_domain.py`
- `tests/integration/approvalgates/test_approvalgates_api.py`
- `uv run pytest tests/unit/approvalgates tests/integration/approvalgates -q --tb=short`

## 8. Test flows

Capture target id/version, request/version, steps, decision/evidence IDs, UI toast, gate response, audit, and outbox.

### F-SETUP

1. Locate a target entity and note version `N`.
2. Open `/approvals`; click **New approval**.
3. Enter title, action code, target type/id, target version `N`.
4. **Expected:** form identifies exact target; no decision yet.

### F-HAPPY

1. Click **Submit request**; expect “Approval request submitted” and Pending.
2. Open `/my-work`; expect it under **Pending approvals**.
3. Return to `/approvals`, select request, and **Attach evidence**.
4. Switch to Baseline Approver/Admin human role and click **Approve**.
5. Expect Approved, completed step, and append-only decision history.
6. POST gate-check for target/version `N`; expect allowed.

### F-VALIDATE

1. Submit without Title/Action code/Target type/version; browser required validation blocks.
2. Reject or withdraw without **Decision reason**.
3. Expect server rejection and Pending remains.

### F-AUTHZ

1. Viewer/Contributor sees Approve disabled and guidance banner.
2. Attempt decision as `X-Actor-Kind: agent`.
3. Attempt self-approval by recommendation source.
4. Expect forbidden and no decision row.

### F-TENANT

1. GET the request using another organization.
2. Attempt gate-check against its target/version.
3. Expect not-found/forbidden and no steps, decisions, or evidence disclosure.

### F-CONCUR

1. Load Pending request/version in two tabs.
2. Approve in tab A; reject in tab B with stale `expected_version`.
3. Expect conflict/terminal rejection and one effective decision.

### F-TRANS

1. Approve an already rejected/withdrawn request.
2. Withdraw an approved request.
3. Expect invalid state; history is not rewritten.

### F-GATE

1. Gate-check target version `N+1` after approving `N`.
2. Expect blocked: approval binds only `N`.
3. Materially edit target; POST supersede with reason.
4. Expect old request no longer unlocks downstream action.

### F-TERM

1. Verify Approved, Rejected, Withdrawn, or Superseded cannot receive another normal decision.
2. **Request changes** is Planned; do not invent a click path.
3. A replacement version requires a new request.

### F-RECOVER

1. Simulate failed decision request; reload queue/history before retry.
2. If no decision row exists and request remains Pending, retry once.
3. Temporal waiting/retry is Planned; do not claim worker recovery.

### F-CLEAN

Leave requests in explicit terminal states or clearly named Pending test state. Preserve decisions, evidence, supersede reasons, and audit history.

## 9. Security, privacy, and approvals

- Backend authorization and actor kind are authoritative.
- Human-only decisions cover scope, SRS, production, client acceptance, closure, and other high-risk gates.
- Evidence references must not contain secrets.
- Emergency override requires authority, reason, incident evidence, and retrospective review.
- UI role selector is a stub and cannot establish approver identity.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Request-changes workflow | Planned |
| Delegation/override UI | API only |
| Full authority matrix | Step assignee/delegation enforced; broader MOD-120 matrix advisory |
| Durable Temporal waits | Planned |
| Real authentication/step-up | Planned |

## 11. Related journeys

- [J-COORD](../../testing/CROSS_MODULE_JOURNEYS.md#j-coord-approvals-and-follow-ups)
- [J-QA](../../testing/CROSS_MODULE_JOURNEYS.md#j-qa-test-bug-change-release)
- `/my-work` aggregates pending approvals.

## 12. Pass / fail checklist

- [ ] Request binds target id and exact version
- [ ] Pending appears in Approvals and My Work
- [ ] Evidence attaches
- [ ] Human approver can approve
- [ ] Reject/withdraw require reason
- [ ] Agent cannot decide
- [ ] Self-approval is rejected
- [ ] Wrong target version remains blocked
- [ ] Stale decision conflicts
- [ ] Cross-tenant access is denied
- [ ] Request-changes marked Planned
- [ ] Automated result recorded
