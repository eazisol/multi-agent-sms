# MOD-630 — Controlled Pilot, Production Release, Operations, Final MVP Sign-Off

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

Owners and operations. This desk stores **pilot records**. It does not deploy production. **Sign as human** is a human-only gate.

## 2. What this module is

A controlled pilot needs a plan, named users, tests, limitations, and sign-offs from product, security, operations, and QA. MASMS records those artifacts so the company can prove who signed what.

An agent must not finalize production release, rollback, or pilot sign-off.

## 3. Status honesty

| Item | Status |
|---|---|
| `/pilot` plan, users, tests, gates, sign-offs | Implemented as records |
| Create plan, Add user, Approve production use, Record test | Implemented |
| Sign as human | Implemented; API must reject agents |
| Live production deploy / rollback | Planned / not this desk |
| GitHub production environment reviewers | See [MOD-030](../MOD-030/E2E_GUIDE.md) |
| Final MVP exit (FINAL/GATE checklists) | Still open at program level |

## 4. Requirements and dependencies

- MVP exit / final acceptance
- Depends on: MOD-600, MOD-610, MOD-620

Before a governed sign-off session, the human coordinator identifies:

- the exact pilot plan under review;
- the acceptance-test evidence version;
- the approved pilot-user list;
- the product representative;
- the security representative;
- the operations representative;
- the QA representative;
- each function's evidence reference;
- every failed, blocked, or high-risk item; and
- the separate authority responsible for any real deployment.

## 5. How to start

Complete [J-UAT](../../testing/CROSS_MODULE_JOURNEYS.md#j-uat-sample-projects-and-evidence-registry). Open **Administration → Pilot**. Use a **human** header role, not Agent (draft only).

## 6. Screens, buttons, and files

Route: `/pilot`  
File: [`pilot-desk-page.tsx`](../../../apps/web/src/components/pilot-desk-page.tsx)

| Control | What happens | Status |
|---|---|---|
| Refresh | Reloads gates and lists | Implemented |
| Acceptance / approval / readiness gate cards | Recorded gate status | Implemented |
| Create plan | POST plan | Implemented |
| Add user | Register pilot user | Implemented |
| Approve production use | Human approve that user | Implemented (human) |
| Record test | Acceptance test row | Implemented |
| Sign as human | Sign-off row | Implemented (human only) |
| Empty states | Explain next action | Implemented |

## 7. API, data, and automated tests

Prefix: `/api/v1/pilot`  
Router: [`modules/pilot/router.py`](../../../apps/api/src/masms_api/modules/pilot/router.py)  
Migration: `20260811_0037`

Tests: `tests/integration/pilot/`

```bash
uv run pytest tests/integration/pilot -q --tb=short
```

## 8. Test flows

### F-SETUP

Human actor. Prefer UAT samples already seeded.

### F-HAPPY

1. Create plan.
2. Add user with a role label.
3. **Approve production use** as human.
4. Record test.
5. **Sign as human** on a pending function.
6. **Expected:** status `signed`; gates update.

### F-VALIDATE

Create plan with empty required fields — browser/API error.

### F-AUTHZ

Switch Role to **Agent (draft only)** and **Sign as human**. **Expected:** API forbidden. This is a critical fail if it succeeds.

### F-TENANT

Other org cannot see the plan.

### F-CONCUR

Sign with stale version — conflict if supported.

### F-TRANS

Sign an already signed row — button disabled.

### F-GATE

Production use approval and sign-off are mandatory human gates. This guide does **not** instruct anyone to apply AWS production.

### F-TERM

Signed-off functions are terminal without an authorized reopen (if any).

### F-RECOVER

Rollback records, if present in API, are documentation — not a live cluster rollback.

### F-CLEAN

Leave the plan as evidence. Do not treat local sign-off as production go-live.

## 9. Security, privacy, and approvals

- Agents cannot sign.
- Production deploy/rollback remain outside this desk.
- Record reasons for any override (none on the current desk).

## 10. Planned versus implemented

Real production cutover, operations runbooks execution, and program-level FINAL/GATE closure.

## 11. Related journeys

- [J-PILOT](../../testing/CROSS_MODULE_JOURNEYS.md#j-pilot-controlled-pilot-records)

## 12. Pass / fail checklist

| Step | Result |
|---|---|
| Create plan + add user | |
| Approve production use (human) | |
| Record test | |
| Sign as human | |
| Agent sign rejected | |
| Did not perform live production deploy | |
| Pilot tests run | |
