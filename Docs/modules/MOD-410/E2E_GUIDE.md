# MOD-410 — Bug Lifecycle, QA Rejection, and Release Gate

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create, reject, and reopen a defect. |
| QA | Verify evidence, lifecycle rules, release blocking, and tenant isolation. |
| Developer | Inspect Phase 4 bug APIs, persistence, and integration coverage. |
| Owner | Confirm critical/high known-issue exceptions require authorization. |

## 2. What this module is

MOD-410 tracks defects from discovery through QA rejection, development reopen, assignment, fix, retest, verification, and known-issue handling.

In this company it means QA can reject a failed requirement with evidence, development can reopen the controlled loop, and release owners can see whether unresolved blocking bugs prevent release.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/bugs` list/create/pagination | Implemented | Phase 4 desk |
| **Reject** with configured desk evidence | Implemented | Reason is fixed by desk |
| **Reopen** rejected bug | Implemented | Returns status to `open` |
| Release gate card | Implemented | Advisory API snapshot |
| Search UI | Planned | `q` exists in API only |
| Status filter UI | Planned | API supports it |
| Severity filter UI | Planned | API supports it |
| Fix, retest, assignment, known issue UI | Planned | APIs exist; no desk controls |
| Live CI/release integration | Planned | Gate does not operate a deployer |

## 4. Requirements and dependencies

- Phase: **Phase 4**, regardless of checklist nesting.
- Reject requires reason and evidence; reopen returns to `open`.
- Critical/high or explicit `blocks_release` defects block the release gate unless verified/closed or covered by an approved known-issue exception.
- Dependencies: local API/web, organization identity, optional project UUID, and MOD-400 evidence for realistic defects.
- Key outbox events: `bug.created`, `bug.rejected`, `bug.reopened`, `bug.fix_submitted`, `bug.retested`.

## 5. How to start

1. Start services using [TESTING_CONVENTIONS.md](../../testing/TESTING_CONVENTIONS.md).
2. Open `http://localhost:3000/bugs`.
3. Set or paste a project UUID to scope the gate.
4. Use a unique bug code such as `BUG-E2E-410-001`.
5. Keep evidence synthetic and non-sensitive.

## 6. Screens, buttons, and files

Desk: [`bugs-desk-page.tsx`](../../../apps/web/src/components/bugs-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| **New bug** | Toggles create form | Implemented | `bugs-desk-page.tsx` |
| **Cancel** | Closes form | Implemented | same |
| **Create** | Creates defect | Implemented | same |
| **Reject** | Sends fixed reason plus Reject evidence default | Implemented | same |
| **Reopen** | Reopens a rejected defect | Implemented | same |
| Release gate card | Shows allowed or blocking codes for project scope | Implemented | same |
| Pagination | Changes list offset/limit | Implemented | same |
| Search/status/severity filters | Not rendered | Planned UI | router API |

The form contains Code, Title, Severity, optional Project ID, and Reject evidence default. Severity is free text, not a select.

## 7. API, data, and automated tests

Prefix: `/api/v1/bugs`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/bugs/router.py)  
Integration test: [`test_bugs_api.py`](../../../tests/integration/bugs/test_bugs_api.py)  
Migration: `20260811_0025`

Key API-only capabilities include history, links, assignments, fixes, retests, severity SLAs, known-issue requests, and decisions.

```bash
uv run pytest tests/integration/bugs -q --tb=short
```

The checked-in verification records one prior passing integration test. It is historical evidence, not a result for this session.

## 8. Test flows

Capture action, UI/toast, persisted state/audit, and screenshot or API response for each step.

### F-SETUP

1. Load `/bugs` and record organization, actor, and project ID.
2. Confirm the Release gate card is scoped to that project.
3. If necessary, use the API to configure a critical SLA with `blocks_release: true`.

### F-HAPPY

1. Click **New bug**.
2. Enter `BUG-E2E-410-001`, a title, severity `critical`, project ID, and evidence `QA screenshot E2E-410`.
3. Click **Create**; expect toast `Bug created`, `open` status, and gate blocked by the code.
4. Click **Reject**; expect `Bug rejected with evidence` and `rejected`.
5. Click **Reopen**; expect `Bug reopened` and `open`.
6. Verify history by API includes the controlled events.

### F-VALIDATE

1. Submit without Code or Title; browser-required validation must block.
2. Submit invalid severity text; expect backend validation/problem response.
3. Reject with invalid/stale version by API; expect conflict.

### F-AUTHZ

1. Attempt a known-issue approval with agent identity.
2. High-risk acceptance must require an authorized human.
3. If backend accepts an unauthorized actor, fail the test and open a security/governance defect.

### F-TENANT

1. Create a bug under organization A.
2. List/get/history it with organization B.
3. Expect no data leakage and no influence on B’s gate.

### F-CONCUR

1. Read the bug version in two clients.
2. Reject in client A.
3. Reopen/transition using client B’s stale version.
4. Expect conflict and preserved latest state.

### F-TRANS

1. Reject an open bug.
2. Attempt a fix/retest transition that is invalid for `rejected`.
3. Expect an invalid-transition response.

### F-GATE

1. With a critical unresolved bug, expect `release_allowed: false`.
2. Verify/retest it through API, or create and have a human approve a known-issue exception.
3. Expect `release_allowed: true` only when no unaccepted blocker remains.
4. Treat this gate as advisory to MOD-430, not a live deployment control.

### F-TERM

1. Put a bug in `verified` or `closed` using the API lifecycle.
2. Confirm the desk no longer shows **Reject**.
3. An unauthorized reopen from a terminal state must fail.

### F-RECOVER

1. Reopen a rejected bug with **Reopen**.
2. Expect the controlled development loop to resume at `open`.
3. Full fix/retest recovery is API-only on this desk.

### F-CLEAN

1. Leave lifecycle and gate evidence intact.
2. Do not erase audit/history.
3. Record bug, project, fix, retest, or known-issue IDs used.

## 9. Security, privacy, and approvals

- Deny cross-organization direct-object access.
- Do not store secrets or client PII in bug titles/evidence.
- Known-issue acceptance for critical/high risk is human-only.
- UI role selection is not backend authentication.
- A clear advisory gate is not approval to release or deploy.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Search/status/severity filtering | API exists; UI Planned |
| Full defect detail studio | List actions only |
| Fix/retest/assignment controls | API only |
| Live CI/deployer gate | Planned |
| Known-issue decision workspace | API only |
| Browser E2E suite | Planned |

## 11. Related journeys

- [MOD-400 tests](../MOD-400/E2E_GUIDE.md)
- [MOD-430 releases](../MOD-430/E2E_GUIDE.md)
- [MOD-460 traceability](../MOD-460/E2E_GUIDE.md)
- Shared [approval conventions](../../testing/TESTING_CONVENTIONS.md#human-only-actions-never-finalize-by-an-agent)

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Bug page and gate load | |
| Critical bug blocks scoped gate | |
| Create persists open bug | |
| Reject records reason and evidence | |
| Reopen returns bug to open | |
| Search UI gap recorded Planned | |
| Status filter UI gap recorded Planned | |
| Severity filter UI gap recorded Planned | |
| Stale version is rejected | |
| Cross-tenant data and gate isolated | |
| Human known-issue gate enforced | |
| Integration test output recorded | |
