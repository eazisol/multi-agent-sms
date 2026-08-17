# MOD-600 — Security, Privacy, Backup, and Recovery Records

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Observe the security gate and create safe registry records. |
| QA | Verify incident gating, training opt-in, recovery measurements, and tenancy. |
| Developer | Trace desk calls to securityhardening routes and tests. |
| Owner | Confirm backups/restores are records, not infrastructure operations. |

## 2. What this module is

This module stores security incidents, training policy, recovery evidence, legal holds, and related security registries.

In this company it means: opening a Critical incident closes the local gate, model-training opt-in needs human evidence, and backup/restore measurements can be recorded without touching production data.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| Critical-incident security gate | Implemented | Computed from open records. |
| Incident open/close | Implemented | Local registry lifecycle. |
| Training policy default-off | Implemented | Evidence required to enable. |
| Backup and restore-test records | Stubbed | No backup or restore executes. |
| Recovery validation API | Implemented | Computes from recorded measurements. |
| Legal-hold list | Implemented | Creation/release is API only. |
| Deletion jobs | Stubbed/API only | Simulated counters and hold checks. |
| Threat/PII/retention registries | Implemented/API only | Not automated scanners. |
| Production backup infrastructure | Planned | Non-testable here. |

## 4. Requirements and dependencies

- Shared environment is running.
- Use synthetic incident names and local backup references.
- Confirm no unrelated Critical incident will distort gate expectations.
- Enabling training is a human-governed policy action; use authorized test evidence only.
- Do not use production data.

## 5. How to start

1. Open **Security** at `/security`.
2. Note current gate and Critical-open count.
3. Use unique code `INC-600-E2E-01`.
4. Keep **Allow model training** unchecked until the gate test.
5. Use backup ref `bk-local-600-e2e-01`.

## 6. Screens, buttons, and files

Desk: [`security-desk-page.tsx`](../../../apps/web/src/components/security-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| Refresh | Reloads gate, policy, and legal holds | Implemented | `security-desk-page.tsx` |
| Save training policy | Persists default-off or evidenced opt-in | Implemented | `security-desk-page.tsx` |
| Open critical incident | Creates Critical open registry row | Implemented | `security-desk-page.tsx` |
| Close last opened incident | Closes only incident opened in this UI session | Implemented | `security-desk-page.tsx` |
| Record backup | Creates local backup metadata row | Stubbed operation | `security-desk-page.tsx` |
| Run restore test | Stores measured RPO/RTO row | Stubbed operation | `security-desk-page.tsx` |
| Legal holds | Lists rows created through API | Implemented read | `security-desk-page.tsx` |

## 7. API, data, and automated tests

Prefix: `/api/v1/security`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/securityhardening/router.py)  
Tests: [`test_security_api.py`](../../../tests/integration/securityhardening/test_security_api.py)

| Method | Path | Purpose |
|---|---|---|
| GET | `/gate` | Critical incident gate |
| GET/PUT | `/training-policy` | Organization policy |
| POST/GET | `/incidents` | Incident registry |
| POST | `/incidents/{id}/close` | Close with version |
| POST/GET | `/backups` | Backup records |
| POST/GET | `/restore-tests` | Measurement records |
| GET | `/recovery-validation` | Recorded-target validation |
| POST/GET | `/legal-holds` | Hold registry |

```bash
uv run pytest tests/integration/securityhardening -q --tb=short
```

These tests use in-memory SQLite and do not prove PostgreSQL RLS or real recovery.

## 8. Test flows

### F-SETUP

1. Open `/security`.
2. **Expected UI:** gate, policy, incident, backup, and legal-hold cards.
3. **Evidence:** initial gate count and policy state.

### F-HAPPY — Critical incident gate

1. Enter unique incident Code and Title.
2. Click **Open critical incident**.
3. **Expected UI:** toast says gate should fail; gate shows failed and count increases.
4. **Expected data/audit:** open Critical incident with version.
5. Click **Close last opened incident**.
6. **Expected UI:** gate returns to its prior state if no other Critical incidents remain.
7. **Evidence:** before/open/closed gate screenshots and incident id.

### F-HAPPY — recovery records

1. Enter backup ref, RPO `60`, RTO `120`.
2. Click **Record backup**.
3. Enter measured RPO `30`, measured RTO `90`.
4. Click **Run restore test**.
5. **Expected UI:** record-created toasts.
6. **Expected data:** restore result is passed; recovery validation is true.
7. **Evidence:** backup id and API JSON.
8. State explicitly: no files or databases were backed up or restored.

### F-VALIDATE

1. Check **Allow model training**, leave evidence empty, and save.
2. **Expected:** `409` or `422`; policy remains disabled.
3. Invalid numeric recovery values must be rejected or reported.

### F-AUTHZ

Only an authorized human may supply model-training approval evidence. The Role selector is not authentication. Agent-generated text is not approval evidence.

### F-TENANT

Create an incident in organization A, then list/close using B.

**Expected:** B list is empty and close returns `404`.

### F-CONCUR

Close an incident with stale `expected_version` through OpenAPI.

**Expected:** conflict; no silent close.

### F-TRANS

Attempt to close an already closed incident.

**Expected:** invalid transition/conflict.

### F-GATE

1. Default training policy is disabled.
2. Enabling requires non-empty authorized human evidence.
3. Critical open incidents make the security gate fail.
4. Never use this guide to accept a Critical production risk.

### F-TERM

Closed incidents cannot be reopened from this desk. Legal-hold release is an API action requiring a reason/policy process.

### F-RECOVER

Record a second restore measurement above targets, such as RPO `90` and RTO `180`.

**Expected:** result failed and recovery validation false. This only tests calculation over records.

### F-CLEAN

Close the synthetic incident if authorized. Leave audit and recovery records intact. Restore training policy to the approved organization setting.

## 9. Security, privacy, and approvals

- Training is denied by default.
- Never use real PII, secrets, production paths, or backup media.
- Legal holds must block governed deletion; do not bypass them.
- Production backup, restore, deletion, deployment, and risk acceptance require authorized humans.
- Tenant scope and append-only audit evidence are mandatory.

## 10. Planned versus implemented

| Target design | M1 behavior |
|---|---|
| Backup infrastructure | Metadata record |
| Executed restore drill | Measurement record |
| Automated threat scanning | Threat-model registry |
| Production deletion pipeline | Simulated deletion-job records |
| Auth0 and full policy middleware | Header identity plus service rules |
| Live RLS proof | Migration design; SQLite tests do not prove it |

## 11. Related journeys

- MOD-610 records reliability and DR evidence.
- MOD-620 stores UAT evidence.
- MOD-630 requires human production readiness.
- MOD-120 provides permission concepts.

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Security desk loads | |
| Open Critical incident fails gate | |
| Close incident restores gate where applicable | |
| Training defaults disabled | |
| Empty opt-in evidence is rejected | |
| Authorized evidence can update policy | |
| Backup row recorded | |
| Restore measurement recorded | |
| Recovery calculation matches targets | |
| Cross-org incident is hidden | |
| Stale close conflicts | |
| No real backup/restore claimed | |
| Automated test result recorded | |
