# MOD-620 — Synthetic Projects, Agent Evaluation, and UAT Evidence

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Seed three samples and record UAT evidence. |
| QA | Verify sample/quality gates, human acceptance, and tenancy. |
| Developer | Trace UAT desk records to routes and tests. |
| Owner | Confirm the desk stores evidence and does not run Playwright or a model evaluation. |

## 2. What this module is

This module stores three synthetic sample-project records, recorded agent-quality scores, E2E/UAT result registries, and acceptance evidence.

In this company it means: create SAMPLE-A/B/C, mark their documented workflows passed, record an 85% evaluation, and submit a reference to a UAT pack.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| Seed SAMPLE-A/B/C | Implemented | Idempotent registry seed. |
| Mark passed and sample gate | Implemented | Records status; does not execute workflow. |
| Agent evaluation and quality gate | Stubbed measurement | Entered score, no live LLM evaluation. |
| Acceptance evidence record | Implemented | Created as submitted. |
| Human evidence acceptance | Implemented/API only | Agent actor rejected. |
| E2E/role-UAT registries | Implemented/API only | Stored results. |
| Playwright/browser execution | Planned | Not run by this desk. |

## 4. Requirements and dependencies

- Shared environment is running.
- Use only synthetic sample and evidence references.
- Marking passed requires separate real evidence in the tester log.
- A human must accept exact evidence; agents cannot.
- Existing sample statuses may already be passed.

## 5. How to start

1. Open **UAT** at `/uat`.
2. Note sample-project and agent-quality gates.
3. Use evaluation code `EVAL-620-E2E-01`.
4. Use evidence code `EV-620-E2E-01`.
5. Do not claim the buttons launch tests.

## 6. Screens, buttons, and files

Desk: [`uat-desk-page.tsx`](../../../apps/web/src/components/uat-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| Refresh | Reloads gates, samples, and evidence | Implemented | `uat-desk-page.tsx` |
| Seed SAMPLE-A / B / C | Creates/returns three synthetic records | Implemented registry | `uat-desk-page.tsx` |
| Mark passed | Changes one sample status to passed | Implemented record | `uat-desk-page.tsx` |
| Record evaluation | Stores entered score and sample count 20 | Stubbed measurement | `uat-desk-page.tsx` |
| Record evidence | Stores submitted evidence reference | Implemented | `uat-desk-page.tsx` |
| Sample-project gate | Shows passed count out of three | Implemented | `uat-desk-page.tsx` |
| Agent quality | Compares latest score to 80% | Implemented calculation | `uat-desk-page.tsx` |

There is no **Run Playwright**, **Accept evidence**, or live-model-evaluation button.

## 7. API, data, and automated tests

Prefix: `/api/v1/uat`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/uateval/router.py)  
Tests: [`test_uat_api.py`](../../../tests/integration/uateval/test_uat_api.py)

| Method | Path | Purpose |
|---|---|---|
| POST | `/sample-projects/seed` | Idempotent sample seed |
| GET | `/sample-projects` | List samples |
| POST | `/sample-projects/{code}/pass` | Record passed |
| GET | `/sample-gate` | Three-of-three calculation |
| POST/GET | `/agent-evaluations` | Recorded scores |
| GET | `/agent-quality` | Latest score vs 80 |
| POST/GET | `/acceptance-evidence` | Evidence records |
| POST | `/acceptance-evidence/{id}/accept` | Human-only acceptance |
| POST/GET | `/e2e-tests` | Result registry, not runner |

```bash
uv run pytest tests/integration/uateval -q --tb=short
```

## 8. Test flows

### F-SETUP

1. Open `/uat`.
2. **Expected UI:** two gates, sample card, evaluation form, evidence form/list.
3. **Evidence:** initial gate screenshot.

### F-HAPPY — sample gate

1. Click **Seed SAMPLE-A / B / C**.
2. **Expected UI:** exactly three rows, initially pending in a clean organization.
3. Capture external/manual evidence for each workflow.
4. Click **Mark passed** on A and B.
5. **Expected:** gate remains failed at 2/3.
6. Click **Mark passed** on C.
7. **Expected:** gate passes at 3/3.
8. **Expected data/audit:** three records only; repeated seed does not duplicate.

### F-HAPPY — evaluation and evidence

1. Enter unique evaluation code, agent code, accuracy `85`.
2. Click **Record evaluation**.
3. **Expected UI:** quality card shows 85% and passed against 80%.
4. Enter unique evidence code/title/reference.
5. Click **Record evidence**.
6. **Expected UI:** submitted evidence row appears.
7. **Evidence:** row ids and screenshots.
8. State that neither Playwright nor a live LLM evaluation ran.

### F-VALIDATE

1. Clear required fields and submit.
2. **Expected:** browser validation.
3. Enter an out-of-range accuracy through OpenAPI.
4. **Expected:** validation error and no evaluation row.

### F-AUTHZ

1. Create submitted evidence as human.
2. Call accept with `X-Actor-Kind: agent`.
3. **Expected:** `409`.
4. A named authorized human may accept the exact version through API.

### F-TENANT

Seed in A, list/get SAMPLE-A as B.

**Expected:** empty list and `404`; no cross-tenant evidence.

### F-CONCUR

Accept evidence with stale `expected_version`.

**Expected:** conflict and submitted status remains until valid human action.

### F-TRANS

Attempt to accept already accepted evidence.

**Expected:** terminal/invalid transition response.

### F-GATE

Sample and quality badges are evidence calculations only. They do not grant final UAT, client acceptance, deployment, or release approval.

### F-TERM

Accepted evidence has no desk edit/reopen action. Corrections require a new evidence version/record.

### F-RECOVER

Record a later evaluation score `70`.

**Expected:** latest quality card fails at 70%, proving latest recorded score drives the gate.

### F-CLEAN

Leave synthetic records and audit history. Do not mark samples passed without an evidence reference in the tester log.

## 9. Security, privacy, and approvals

- Use synthetic project data and sanitized evidence references.
- Agents may record/draft evidence but cannot accept it.
- Client acceptance and final UAT sign-off are human-only.
- Do not place secrets or PII in evidence references.
- SQLite API tests do not prove PostgreSQL RLS.

## 10. Planned versus implemented

| Target design | M1 behavior |
|---|---|
| Full project data seeder | Three registry rows |
| Workflow execution | Manual status record |
| Playwright runner | E2E result registry/API |
| Live model evaluation | Entered score |
| Final UAT approval desk | Human accept API only |
| Production release gate | Separate MOD-630 human process |

## 11. Related journeys

- MOD-600 provides security evidence.
- MOD-610 provides reliability evidence.
- MOD-630 consumes controlled pilot/readiness evidence.
- MOD-000 governs approved baselines.

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| UAT desk loads | |
| Seed creates only SAMPLE-A/B/C | |
| Re-seed is idempotent | |
| Two passed keeps gate failed | |
| Three passed makes gate pass | |
| 85% record passes quality gate | |
| Later 70% record fails gate | |
| Evidence appears submitted | |
| Agent acceptance is rejected | |
| Human exact-version acceptance works if authorized | |
| Cross-org samples are hidden | |
| No Playwright/live LLM claim made | |
| Automated test result recorded | |
