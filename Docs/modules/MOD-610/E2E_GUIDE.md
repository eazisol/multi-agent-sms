# MOD-610 — Performance, Reliability, Replay, and DR Records

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Record a performance value, replay lifecycle, and runbook. |
| QA | Verify SLO calculations, transitions, idempotency, and isolation. |
| Developer | Trace reliability UI actions to API state machines and tests. |
| Owner | Confirm no load test, Temporal replay, or live DR ran. |

## 2. What this module is

This module stores measured-performance claims, SLO calculations, replay state, failure evidence, and DR runbook documents.

In this company it means: record “p95 was 1800 ms,” evaluate it against a 2000 ms budget, and exercise a local replay record from pending through failed, resumed, and completed.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| API/dashboard SLO cards | Implemented | Computed from latest recorded values. |
| Record performance run | Stubbed measurement | Does not execute k6/load generation. |
| Replay state machine | Implemented registry | Does not resume Temporal. |
| Simulate fail and Resume | Stubbed actions | Resume button also completes. |
| DR runbook registry | Implemented | Document record, not procedure execution. |
| Live load monitoring | Planned | No production telemetry proof. |
| Live DR/failover | Planned | Non-testable here. |

## 4. Requirements and dependencies

- Shared environment is running.
- Use unique codes/idempotency keys.
- Existing latest records may affect SLO cards.
- Use local/pilot wording, never production claims.
- No production infrastructure action is authorized.

## 5. How to start

1. Open **Reliability** at `/reliability`.
2. Note initial API and Dashboard SLO cards.
3. Use code `PERF-610-E2E-01`.
4. Use replay key `replay-610-e2e-01`.
5. Use runbook code `DR-610-E2E-01`.

## 6. Screens, buttons, and files

Desk: [`reliability-desk-page.tsx`](../../../apps/web/src/components/reliability-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| Refresh | Reloads SLO cards and runbooks | Implemented | `reliability-desk-page.tsx` |
| Record run | Stores supplied p95 value | Stubbed measurement | `reliability-desk-page.tsx` |
| Create replay | Creates pending registry row | Implemented registry | `reliability-desk-page.tsx` |
| Simulate fail | Marks current replay failed | Stubbed | `reliability-desk-page.tsx` |
| Resume | Resumes then immediately completes record | Stubbed shortcut | `reliability-desk-page.tsx` |
| Record runbook | Stores local restore document metadata | Implemented registry | `reliability-desk-page.tsx` |
| API SLO | Shows 2000 ms budget calculation | Implemented | `reliability-desk-page.tsx` |
| Dashboard SLO | Shows 3000 ms budget calculation | Implemented | `reliability-desk-page.tsx` |

## 7. API, data, and automated tests

Prefix: `/api/v1/reliability`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/reliability/router.py)  
Tests: [`test_reliability_api.py`](../../../tests/integration/reliability/test_reliability_api.py)

| Method | Path | Purpose |
|---|---|---|
| GET | `/api-slo` | API budget calculation |
| GET | `/dashboard-slo` | Dashboard budget calculation |
| POST/GET | `/performance-tests` | Measurement records |
| POST/GET | `/replays` | Replay registry |
| POST | `/replays/{id}/fail` | Failed state |
| POST | `/replays/{id}/resume` | Resumed state |
| POST | `/replays/{id}/complete` | Completed state |
| POST/GET | `/dr-runbooks` | Runbook records |
| POST | `/dr-runbooks/{id}/approve` | Human-governed API action |

```bash
uv run pytest tests/integration/reliability -q --tb=short
```

## 8. Test flows

### F-SETUP

1. Open `/reliability`.
2. **Expected UI:** two SLO cards and three record/action areas.
3. **Evidence:** initial screenshot and organization id.

### F-HAPPY — recorded API SLO

1. Enter unique Code, Suite `api-normal`, p95 `1800`.
2. Click **Record run**.
3. **Expected UI:** success toast; API SLO shows 1800 against 2000 and passed.
4. **Expected data/audit:** one performance-test row.
5. **Evidence:** row via API and SLO card.
6. Record that no load generator ran.

### F-HAPPY — replay lifecycle

1. Enter workflow and unique idempotency key.
2. Click **Create replay**; expect status `pending`.
3. Click **Simulate fail**; expect `failed`.
4. Click **Resume**; expect final `completed`.
5. **Expected data/audit:** versions increment across failed, resumed, completed.
6. **Evidence:** statuses and replay id.
7. Record that Temporal was not contacted.

### F-VALIDATE

1. Clear required fields and submit.
2. **Expected:** browser validation.
3. Create the same idempotency key twice via OpenAPI.
4. **Expected:** duplicate is `409`.

### F-AUTHZ

Runbook approval and production DR decisions require authorized humans. The desk records drafts only and has no approval button.

### F-TENANT

Create a replay in organization A and list/resume as B.

**Expected:** B list is empty; transition returns `404`.

### F-CONCUR

Fail/resume with stale `expected_version`.

**Expected:** conflict and unchanged current state.

### F-TRANS

Resume a completed replay.

**Expected:** `409`; completed state remains terminal.

### F-GATE

SLO badges are calculations over entered records, not release approval. A passed badge must not authorize production deployment or risk acceptance.

### F-TERM

Completed replay cannot resume. Approved runbook governance is API-only and must preserve history.

### F-RECOVER

The fail → resume → complete sequence is the recovery test for the registry. It is not a workflow replay or disaster-recovery exercise.

### F-CLEAN

Leave unique records and audit evidence. Do not label the runbook “executed” unless a separately authorized real exercise occurred.

## 9. Security, privacy, and approvals

- Do not put secrets or client data in error strings, workflow names, or runbooks.
- Production failover, rollback, and infrastructure changes require explicit human approval.
- Tenant scope applies to all measurements and replay records.
- Idempotency keys must not leak sensitive identifiers.
- A DR document is not evidence that recovery succeeded.

## 10. Planned versus implemented

| Target design | M1 behavior |
|---|---|
| k6/live load run | Manually supplied p95 record |
| Production telemetry SLO | Latest stored measurement |
| Temporal replay/resume | Registry transitions |
| Executed DR runbook | Runbook metadata/document preview |
| Automated failover | None |
| Browser E2E | Manual guide and API tests |

## 11. Related journeys

- MOD-500 covers integration relay simulations.
- MOD-600 covers backup/recovery records.
- MOD-620 records acceptance evidence.
- MOD-630 controls human production readiness.

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Reliability desk loads | |
| 1800 ms record passes 2000 ms API budget | |
| Above-budget record fails card | |
| Replay creates pending | |
| Simulate fail reaches failed | |
| Resume reaches completed | |
| Duplicate key conflicts | |
| Completed replay cannot resume | |
| Cross-org replay is hidden | |
| Runbook record appears | |
| No live load/Temporal/DR claim made | |
| Automated test result recorded | |
