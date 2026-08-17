# MOD-430 — Releases, Deployment Records, Production Approval, and Closure

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Package and submit a release, then record a deployment request. |
| QA | Verify production approval, backup, traceability, and closure gates. |
| Developer | Inspect Phase 4 release/deployment APIs and integration coverage. |
| Owner | Ensure production approval/deployment remains human-controlled. |

## 2. What this module is

MOD-430 stores release packages, traceability links, production approvals, backup and migration evidence, deployment/check records, rollbacks, and completion acceptance.

In this company it means a release owner assembles evidence and requests production approval, while operations records what was requested and checked. A “production deployment” here is a database **record**, not a live AWS, CI, or infrastructure deployment.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/releases` create/submit/list/pagination | Implemented | Phase 4 desk |
| **Approve prod** | Implemented UI | Must be used only by authorized human |
| `/deployments` list/status filter/pagination | Implemented | Reads release deployment records |
| **Start deployment** | Implemented record creation | Does not deploy software |
| Production option in UI | Implemented | UI allows selection before knowing all gates |
| Backend production gate | Implemented | Rejects unapproved or missing-backup production |
| Package links | Stubbed data when omitted | Random synthetic UUIDs for five link types |
| Live deployer/CI/AWS | Planned | No infrastructure action |
| Rollback/closure/check UI | Planned | APIs exist |

## 4. Requirements and dependencies

- Phase: **Phase 4**.
- Production requires an approved release and confirmed backup; evidence is required by release approval.
- Closure requires both client and internal acceptance.
- Dependencies: traced requirements/tickets/tests/bugs/CRs/documents, human production approver, and backup evidence.
- Production deployment or rollback must never be finalized by an agent.

## 5. How to start

1. Start services from [TESTING_CONVENTIONS.md](../../testing/TESTING_CONVENTIONS.md).
2. Open `/releases`; prepare unique code `REL-E2E-430-001`.
3. Use a real requirement UUID when available.
4. Understand that omitted package links are generated with `crypto.randomUUID()` and do not prove real linked records.
5. Arrange a named human production approver before clicking **Approve prod**.

## 6. Screens, buttons, and files

Release desk: [`releases-desk-page.tsx`](../../../apps/web/src/components/releases-desk-page.tsx)  
Deployment desk: [`deployments-desk-page.tsx`](../../../apps/web/src/components/deployments-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| **New release** | Toggles package form | Implemented | `releases-desk-page.tsx` |
| **Create & submit** | Creates six link entries and submits | Implemented; synthetic links possible | same |
| **Approve prod** | Records production approval evidence | Implemented; human-only | same |
| Release pagination | Changes list page | Implemented | same |
| **Start deployment** | Opens deployment-record form | Implemented | `deployments-desk-page.tsx` |
| Release select | Selects any loaded release/status | Implemented | same |
| Environment select | `staging` or `production` | Implemented | same |
| **Start** | Requests/records deployment | Implemented record | same |
| Deployment status filter | all/requested/succeeded/failed | Implemented | same |
| Deployment pagination | Changes page | Implemented | same |

The package form accepts Code, Title, Version label, and optional Requirement ID. Ticket, test, bug, change-request, and document links are always synthetic random UUIDs in this desk.

## 7. API, data, and automated tests

Prefix: `/api/v1/releases`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/releases/router.py)  
Integration test: [`test_releases_api.py`](../../../tests/integration/releases/test_releases_api.py)  
Migration: `20260811_0027`

Routes cover releases/items/traceability, submit/approve, backups, migration plans, deployments/checks, rollbacks, and completion reports.

```bash
uv run pytest tests/integration/releases -q --tb=short
```

The verification file records one historical pass. Rerun before claiming current success.

## 8. Test flows

Capture action, expected UI/toast, persisted status/version/audit, and screenshots or responses.

### F-SETUP

1. Load `/releases` and `/deployments`.
2. Record organization, actor, approver, real requirement ID, and build reference.
3. Prepare separate releases for negative and happy paths.

### F-HAPPY

1. On `/releases`, click **New release**.
2. Enter `REL-E2E-430-001`, title, version `1.0.0-e2e`, and a real requirement ID.
3. Click **Create & submit**; expect `ready_for_approval` and toast `Release submitted for production approval`.
4. Record that five package link IDs are synthetic.
5. Have the authorized human click **Approve prod**; expect `approved`.
6. Add confirmed backup and migration plan through API.
7. Open `/deployments`, click **Start deployment**, select release, `production`, and build ref.
8. Click **Start**; expect `Deployment requested` and status `requested`.
9. Do not claim any AWS/live environment changed.

### F-VALIDATE

1. Leave release Code or Title empty; browser validation blocks.
2. Click **Start deployment** when no releases exist; **Start** must be disabled.
3. Use invalid UUID/build values through API; expect problem response.

### F-AUTHZ

1. Attempt approval and production start using `X-Actor-Kind: agent`.
2. Backend must deny human-only production authority.
3. If accepted, fail and raise a critical governance/security defect.

### F-TENANT

1. Create release/deployment under organization A.
2. List/get them under organization B.
3. Expect not found/empty; no package evidence or status leaks.

### F-CONCUR

1. Read release version in two clients.
2. Submit/approve in client A.
3. Start or approve with client B’s stale `expected_version`.
4. Expect conflict and no duplicate state transition.

### F-TRANS

1. Create a draft release through API.
2. Use `/deployments` UI to select `production` if listed and click **Start**.
3. Backend must reject unapproved production even though the UI permits selection.
4. Verify approved-without-backup production also fails.

### F-GATE

1. Draft/unapproved production: expect conflict.
2. Approved but no confirmed backup: expect validation failure.
3. Approved plus confirmed backup: production record may be created.
4. Human production approval is still required; record approver and evidence.

### F-TERM

1. Record deployment check and completion through API.
2. Client-only acceptance must not close.
3. Both client and internal acceptance may close the release.
4. Closed release must not silently reopen.

### F-RECOVER

1. Use rollback API only with explicit authorized human approval.
2. Record reason/evidence; do not execute a real rollback.
3. No rollback button or live recovery worker exists in the desk.

### F-CLEAN

1. Retain release, approval, backup, deployment, and check records.
2. Do not delete audit or acceptance evidence.
3. Mark every random link as synthetic in the session notes.

## 9. Security, privacy, and approvals

- Production deployment and rollback are high-risk human-only actions.
- Backend enforcement is mandatory even when UI offers `production`.
- Header identity/role is not real authentication.
- Never use real backup credentials, secret URLs, or client data in test evidence.
- Random package UUIDs are not traceability proof.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Real CI/AWS deployment | Database record only |
| Verified package relationships | Several synthetic UUID links |
| Dedicated approval workflow | Desk button plus backend service |
| Backup/check/rollback/closure UI | API only |
| Strong authenticated approver | Planned |
| Browser E2E automation | Planned |

## 11. Related journeys

- [MOD-410 release gate](../MOD-410/E2E_GUIDE.md)
- [MOD-420 approved changes](../MOD-420/E2E_GUIDE.md)
- [MOD-460 evidence](../MOD-460/E2E_GUIDE.md)
- Shared [human-only actions](../../testing/TESTING_CONVENTIONS.md#human-only-actions-never-finalize-by-an-agent)

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Release create & submit works | |
| Synthetic package links disclosed | |
| Authorized human approval recorded | |
| Unapproved production rejected by backend | |
| Approved-without-backup rejected | |
| Approved-with-backup deployment record created | |
| Deployment described as record, not live deploy | |
| Stale version rejected | |
| Cross-tenant release/deployment hidden | |
| Dual acceptance required for closure | |
| Rollback remains human-controlled | |
| Integration test output recorded | |
