# MOD-460 — Requirement Traceability, Audit Reports, and Evidence Exports

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

QA and auditors proving Must-Have requirements connect to tickets, tests, and releases. Also uses `/audit-logs` from [MOD-040](../MOD-040/E2E_GUIDE.md).

## 2. What this module is

Release is not allowed when Must-Haves lack a chain: requirement → ticket → test → (bug) → release. This desk registers must-haves, links, manifests, and sealed exports.

## 3. Status honesty

| Item | Status |
|---|---|
| `/traceability` coverage cards, must-have register, ticket link, manifest, export | Implemented |
| Add item + seal | Implemented shortcut |
| Test/release/document links | API (desk notes they are also required) |
| `/audit-logs` | Implemented read-only (MOD-040) |
| Reconcilable export files to object storage | Partial / preview |

## 4. Requirements and dependencies

- MVP-FR-013, MVP-NFR-005
- Needs project/requirement/ticket ids from earlier journeys

## 5. How to start

**Governance → Traceability**. Have a ticket id if you will add a link.

## 6. Screens, buttons, and files

Route: `/traceability`  
File: [`traceability-desk-page.tsx`](../../../apps/web/src/components/traceability-desk-page.tsx)

| Control | What happens | Status |
|---|---|---|
| Refresh | Reloads coverage | Implemented |
| Export sealed | Creates export record | Implemented |
| Coverage cards | Must-haves / coverage counts | Implemented |
| Register must-have | Code/title | Implemented |
| Add ticket link | Links requirement↔ticket | Implemented |
| Create draft manifest | Draft | Implemented |
| Add item + seal | Combined | Implemented |
| Manifest/export lists | Implemented | |

Audit: `/audit-logs` — [MOD-040](../MOD-040/E2E_GUIDE.md).

## 7. API, data, and automated tests

Prefix: `/api/v1/traceability`  
Router: [`modules/traceability/router.py`](../../../apps/api/src/masms_api/modules/traceability/router.py)  
Migration: `20260811_0030`

Tests: `tests/integration/traceability/`

```bash
uv run pytest tests/integration/traceability -q --tb=short
```

## 8. Test flows

### F-SETUP

Requirement and ticket ids from [MOD-240](../MOD-240/E2E_GUIDE.md) / [MOD-300](../MOD-300/E2E_GUIDE.md).

### F-HAPPY

1. Register a must-have.
2. Add ticket link.
3. Create draft manifest; **Add item + seal**.
4. **Export sealed**.
5. **Expected:** coverage numbers move; sealed manifest is not silently editable.

### F-VALIDATE

Empty manifest title — required.

### F-AUTHZ

Sealing/export is a sensitive action; still visible to header roles (server must org-scope).

### F-TENANT

Other org cannot see manifests.

### F-CONCUR

Seal with stale version — conflict if supported.

### F-TRANS

Edit a sealed manifest — rejected.

### F-GATE

Sealed evidence packs are controlled. Humans own release decisions that depend on them ([MOD-430](../MOD-430/E2E_GUIDE.md)).

### F-TERM

Sealed is terminal for that manifest version.

### F-RECOVER

N/A.

### F-CLEAN

Keep the manifest as UAT evidence ([MOD-620](../MOD-620/E2E_GUIDE.md)).

## 9. Security, privacy, and approvals

Exports may contain client names — treat as classified. Append-only audit.

## 10. Planned versus implemented

Full link types on the desk, downloadable signed files, 95% Must-Have gate wired into release UI.

## 11. Related journeys

- [J-INSIGHT](../../testing/CROSS_MODULE_JOURNEYS.md#j-insight-dashboard-reporting-traceability)
- [J-QA](../../testing/CROSS_MODULE_JOURNEYS.md#j-qa-test-bug-change-release)

## 12. Pass / fail checklist

| Step | Result |
|---|---|
| Register must-have | |
| Ticket link | |
| Seal manifest | |
| Export | |
| Sealed not editable | |
| Traceability tests run | |
