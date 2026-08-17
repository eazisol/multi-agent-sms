# MOD-400 — Test Cases, Runs, Evidence, and Coverage

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create an approved test case and record a simulated pass. |
| QA | Check approval, evidence, coverage, validation, and stale-version behavior. |
| Developer | Inspect the Phase 4 API, persistence, outbox, and integration test. |
| Owner | Confirm displayed coverage is evidence-based and not a release approval. |

## 2. What this module is

MOD-400 stores test cases, steps, suites, plans, runs, evidence, and requirement coverage links.

In this company it means a QA analyst can link a Must-Have requirement to an approved case, run the desk shortcut against a named build, and retain environment/build evidence. The desk does not execute a real external test runner.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/test-cases` list, create, pagination | Implemented | Current Phase 4 desk |
| **Create & approve** | Implemented shortcut | Combines creation and approval |
| Coverage snapshot | Implemented | Uses supplied Must-Have requirement ID |
| **Run** | Stubbed | Records an immediate simulated passing run |
| Evidence | Implemented record | Text says “Desk evidence”; no uploaded artifact |
| Suites and plans | Implemented API | No desk controls |
| External CI/test runner | Planned | No live executor integration |
| Header identity | Stubbed | Not authentication |

The shortcut does not replace the target governance rule that approval should be a separate authorized human decision on an exact version.

## 4. Requirements and dependencies

- Phase: **Phase 4**, even where a checklist nests MOD-400 under Phase 3.
- Acceptance: Must-Have covered/uncovered summary; permission/negative cases count; evidence retains environment and build.
- Dependencies: running API/web, organization header identity, and optionally a project and requirement UUID.
- Only approved cases may start runs.
- Relevant outbox events include `testcase.case.created`, `testcase.run.started`, `testcase.run.completed`, and `testcase.coverage.linked`.

## 5. How to start

1. Start the shared environment from [TESTING_CONVENTIONS.md](../../testing/TESTING_CONVENTIONS.md).
2. Open `http://localhost:3000/test-cases`.
3. Optionally select a project first so `masms.workspace.projectId` pre-fills.
4. Obtain a real requirement UUID for a meaningful coverage test.
5. Use a unique code such as `TC-E2E-400-001`.

## 6. Screens, buttons, and files

Desk: [`test-cases-desk-page.tsx`](../../../apps/web/src/components/test-cases-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| **New case** | Toggles create form | Implemented | `test-cases-desk-page.tsx` |
| **Cancel** | Closes create form | Implemented | same |
| **Create & approve** | Creates, optionally links coverage, then approves | Implemented shortcut | same |
| **Run** | Starts local run and immediately completes `passed` with evidence | Stubbed execution | same |
| Coverage snapshot | Shows Must-Have covered/total and permission/negative count | Implemented | same |
| Pagination | Changes limit/offset | Implemented | same |
| Search/status/type controls | API supports them; desk does not show them | Planned UI | router |

Fields are Code, Title, Type, Priority, optional Must-Have requirement ID, optional Project ID, First step action, and Build ref.

## 7. API, data, and automated tests

Prefix: `/api/v1/test-cases`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/testcases/router.py)  
Integration test: [`test_testcases_api.py`](../../../tests/integration/testcases/test_testcases_api.py)  
Migration: `20260811_0024`

Key routes:

- `POST/GET /cases`; `GET /cases/{id}`
- `POST /cases/{id}/approve`
- `POST/GET /cases/{id}/coverage`
- `POST /coverage/summary`
- `POST/GET /runs`; `POST /runs/{id}/complete`
- `GET /runs/{id}/evidence`
- `POST/GET /suites` and `/plans`

Run:

```bash
uv run pytest tests/integration/testcases -q --tb=short
```

The repository verification log records an earlier one-test pass; rerun it before claiming the current checkout passes.

## 8. Test flows

For every numbered step capture the action, resulting UI, persisted ID/status/version or audit/outbox evidence, and a screenshot or response.

### F-SETUP

1. Load `/test-cases`; expect Cases and Coverage snapshot with no API error toast.
2. Record organization, actor, optional project ID, requirement ID, and test build reference.

### F-HAPPY

1. Click **New case**.
2. Enter code `TC-E2E-400-001`, title `Permission boundary case`, type `permission`, priority `P0`, a first step, and build `e2e-local-400`.
3. Enter a real Must-Have requirement UUID and click **Create & approve**.
4. Expect toast `Test case created and approved`, an `approved` badge, and **Run**.
5. Expect Coverage snapshot to show the supplied requirement covered and permission/negative count at least one.
6. Click **Run**.
7. Expect toast `Run completed with evidence`; API data should contain status `passed`, environment `local`, build `e2e-local-400`, title `Desk evidence`, and result `Desk M1 manual pass`.

### F-VALIDATE

1. Leave Code or Title empty and submit; browser-required validation must block.
2. Enter a non-UUID requirement ID; expect an error toast/problem response and no successful combined result.
3. API-create a draft and attempt a run; expect `422`.

### F-AUTHZ

1. Repeat approval with `X-Actor-Kind: agent`.
2. Record actual backend result; the desk has no approval-role hiding.
3. If an agent can approve, fail the human-governance expectation and raise a defect; do not describe the shortcut as human approval.

### F-TENANT

1. Create under organization A.
2. List/get with organization B.
3. Expect no organization A case, coverage, run, or evidence.

### F-CONCUR

1. Start a run and note version `1`.
2. Complete it once, then complete again with stale `expected_version: 1`.
3. Expect conflict or invalid transition and no second terminal result.

### F-TRANS

1. API-create a draft case.
2. Try to start its run.
3. Expect rejection because only `approved` cases run.

### F-GATE

1. Confirm the desk combines creation and approval.
2. Treat this as an implemented convenience, not proof of independent human review.
3. A release decision remains outside this module.

### F-TERM

1. Complete a run as `passed`.
2. Attempt another completion.
3. Expect the terminal run not to change.

### F-RECOVER

N/A — no external runner, queue retry, or recovery worker is exposed by this desk.

### F-CLEAN

1. Keep the case, run, coverage link, and evidence for traceability.
2. Do not delete append-only audit/outbox evidence.
3. Record generated IDs in the test session.

## 9. Security, privacy, and approvals

- Every query must remain organization-scoped; test cross-tenant access directly.
- Header identity is a stub and does not prove login.
- Do not place client secrets or production data in steps or evidence.
- Case approval should ultimately be human-authorized and exact-version bound.
- A simulated pass is not release acceptance.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Separate reviewed approval | Combined desk shortcut |
| Real test execution | Simulated immediate pass |
| Evidence uploads | Persisted text evidence |
| Full QA studio | List/create/run/coverage desk |
| Search and filters | API only |
| Browser E2E automation | Planned |

## 11. Related journeys

- [MOD-240 requirements](../MOD-240/E2E_GUIDE.md)
- [MOD-410 bugs](../MOD-410/E2E_GUIDE.md)
- [MOD-430 releases](../MOD-430/E2E_GUIDE.md)
- [MOD-460 traceability](../MOD-460/E2E_GUIDE.md)

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Page and coverage snapshot load | |
| Create & approve produces approved case | |
| Requirement coverage link appears | |
| Permission/negative count is honest | |
| Run records simulated pass and evidence | |
| Evidence retains environment/build | |
| Draft run is rejected | |
| Stale completion is rejected | |
| Cross-tenant data is hidden | |
| Human-approval shortcut limitation recorded | |
| Integration test command and output recorded | |
