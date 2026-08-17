# MOD-250 — Documents, Templates, Versioning, and Secure File Storage

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Register a document and simulate a clean release. |
| QA | Verify filters, scan gates, availability, scope, and permission APIs. |
| Developer | Distinguish metadata simulation from real object storage. |
| Owner | Confirm unsafe versions cannot become available or indexed. |

## 2. What this module is

This module records controlled documents, their versions, classifications, scan results, permissions, and availability. The current desk registers file metadata; it does not upload bytes.

In this company it means: register “Architecture Overview,” add metadata for `architecture.pdf`, record a simulated clean scan, then mark that version available.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/documents` create, selection, search, filters, paging | Implemented | Current UI supersedes stale README. |
| Document version metadata form | Implemented | Generates storage key, PDF type, and fixed 1024-byte size. |
| Scan verdict recording | Stubbed | Tester selects Clean/Infected/Suspicious; no antivirus engine runs. |
| Mark available gate | Implemented | API requires a clean scan and effective time. |
| Real file picker and S3 upload/download | Stubbed/Planned | No file input and no byte transfer. |
| Templates, attachments, permissions, access-check | Implemented API only | No matching controls. |
| Embedding/index consumer | Planned | `indexing_allowed` gate only. |
| Header identity | Stubbed | Not login. |
| Human M1 acceptance | Blocked | AC-901 not obtained. |

## 4. Requirements and dependencies

- MOD-240 project selection is optional but recommended.
- Project id persists as `masms.workspace.projectId`.
- Selected document persists as `masms.workspace.documentId`.
- New UI documents always use classification `internal`; classification dropdown filters existing records.
- Available version needs owner, effective date, and clean scan.
- Real S3 and antivirus providers are not part of this test.

## 5. How to start

1. Start shared API/web.
2. Select a synthetic project in `/projects`.
3. Open `/documents`.
4. Use Contributor to create/add version.
5. Use Baseline Approver/Admin to expose **Mark available**.
6. Never enter a real storage key, secret, or client filename.

## 6. Screens, buttons, and files

Screen: `/documents`  
Desk: [`documents-desk-page.tsx`](../../../apps/web/src/components/documents-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| New document | Toggles metadata form. | Implemented | `documents-desk-page.tsx` |
| Title | Required document title. | Implemented | `documents-desk-page.tsx` |
| Cancel | Closes document form. | Implemented | `documents-desk-page.tsx` |
| Create document | Creates internal document, links workspace project, opens version form. | Implemented | `documents-desk-page.tsx` |
| Search title | Server `q` filter. | Implemented | `documents-desk-page.tsx` |
| Status | Any, Active, Draft, Archived. | Implemented | `documents-desk-page.tsx` |
| Classification | Any, Internal, Confidential, Restricted, Public. | Implemented filter | `documents-desk-page.tsx` |
| Scope to workspace project | Adds/removes `project_id` list filter. | Implemented | `documents-desk-page.tsx` |
| Document row | Selects document and stores workspace id. | Implemented | `documents-desk-page.tsx` |
| Pagination | Changes offset/page size. | Implemented | `list-pagination.tsx` |
| Add version | Toggles version metadata form. | Implemented | `documents-desk-page.tsx` |
| File name | Required text only; no file picker. | Stubbed storage | `documents-desk-page.tsx` |
| Cancel version | Closes version form. | Implemented | `documents-desk-page.tsx` |
| Add version submit | Generates `uploads/<time>/<name>`, PDF metadata, 1024 bytes. | Stubbed storage | `documents-desk-page.tsx` |
| Scan result | Clean, Infected, Suspicious selected by tester. | Stubbed provider | `documents-desk-page.tsx` |
| Record scan | Stores selected simulated verdict. | Stubbed provider | `documents-desk-page.tsx` |
| Mark available | Sets current time and asks API to release version. | Implemented gate | `documents-desk-page.tsx` |

There is no real file chooser, progress bar, preview, download, template, permission, or version-history browser.

## 7. API, data, and automated tests

Prefix: `/api/v1/documents`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/documents/router.py)  
Migration: `20260811_0014`

| Method | Path |
|---|---|
| POST | `/templates` |
| POST | `/template-versions` |
| POST | `/template-versions/{id}/publish` |
| POST / GET | `/api/v1/documents` |
| GET | `/api/v1/documents/{document_id}` |
| POST | `/versions` |
| POST | `/versions/{id}/available` |
| POST | `/attachments` |
| POST | `/permissions` |
| POST | `/scan-results` |
| POST | `/access-check` |

Tests: [`tests/unit/documents`](../../../tests/unit/documents), [`tests/integration/documents/test_documents_api.py`](../../../tests/integration/documents/test_documents_api.py)

```bash
uv run pytest tests/unit/documents tests/integration/documents -q --tb=short
```

## 8. Test flows

Capture document/version ids, generated metadata, verdict, status, effective time, indexing flag, workspace scope, and API/audit evidence.

### F-SETUP

1. Select an E2E project; open `/documents`.
2. Role = Contributor.
3. Expected: scope checkbox is visible and checked when workspace project exists.
4. Evidence: project/document localStorage values and list request.

### F-HAPPY

1. Click **New document**.
2. Title `E2E Architecture Overview 250`; click **Create document**.
3. Expected: selected internal draft attached to workspace project; Add version form opens.
4. Enter File name `e2e-architecture.pdf`; click **Add version**.
5. Expected: version 1 “uploaded” toast; inspect metadata only.
6. Select **Clean** and click **Record scan**.
7. Switch to authorized role and click **Mark available**.
8. Expected: version status `available`, effective time set, `indexing_allowed=true`.
9. Search title; test Draft/Active filters as appropriate, Internal classification, workspace scope, and pagination.
10. Explicitly record that no bytes were uploaded.

### F-VALIDATE

1. Empty Title or File name must be browser-blocked.
2. Mark a fresh version available without scan through API; expect `422`.
3. Submit malformed permission/access action through API; expect validation problem.
4. The UI does not validate actual PDF content because no file exists.

### F-AUTHZ

1. Viewer should not see New document/Add version.
2. **Mark available** is disabled without approve capability.
3. Backend access-check must separately enforce download, preview, extract, and embeddings.
4. UI role state is not authentication.

### F-TENANT

1. List documents under another organization; expect no first-org title.
2. Request document/version access with another organization/project.
3. Expected: not found/forbidden and no storage metadata leak.
4. Verify workspace project filtering does not replace backend tenant scope.

### F-CONCUR

N/A — current desk has no `expected_version` mutation. Version numbers are append-only.

### F-TRANS

1. Create a version; do not scan; try available — expect `422`.
2. Record **Infected**; try available — expect `403`, quarantined/non-indexable state.
3. Record **Suspicious**; verify it does not pass the clean gate.
4. Only a clean version with owner/effective time becomes available.

### F-GATE

1. Scan result is a release gate, but the current verdict is tester-simulated.
2. Availability action requires an approve-capable UI role.
3. Capture exact version id and scan row used by the decision.
4. Do not claim antivirus or production release approval occurred.

### F-TERM

1. Available version is authoritative for that version number.
2. New content must create another version.
3. Infected/quarantined content must never be available or indexed.
4. No delete/reopen controls exist on the desk.

### F-RECOVER

1. Fail scan API; expect “Scan failed.”
2. Reload: selected in-memory `version` is cleared, so inspect API/test data before retry.
3. Fail availability; expect error and unchanged version.
4. No object-store retry can be tested because no upload occurs.

### F-CLEAN

Leave synthetic document/version/scan evidence. Clear filters. Do not delete scan, permission, audit, or authoritative version history.

## 9. Security, privacy, and approvals

- Classification filter is not authorization; backend checks remain mandatory.
- Storage keys must be tenant/project scoped and must never contain secrets.
- Unsafe scan verdicts block availability and indexing.
- Access surfaces are separately permissioned.
- A simulated scan must never be represented as a real malware scan.
- No production file release is approved by this guide.

## 10. Planned versus implemented

| Target design | Current behavior |
|---|---|
| File picker + S3 byte upload/download | Metadata-only simulation |
| Antivirus provider | Tester-selected verdict |
| Preview/download | No desk controls |
| Template and permission administration | API only |
| Knowledge indexing | Gate field only |

## 11. Related journeys

- Project context: [MOD-240](../MOD-240/E2E_GUIDE.md)
- Communications attachments: [MOD-220](../MOD-220/E2E_GUIDE.md)
- Shared: [Cross-module journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

## 12. Pass / fail checklist

| Check | Result (pass / fail / skip / blocked) |
|---|---|
| Document creates against expected workspace project | |
| Search/status/classification/scope/pagination work | |
| Version form is recorded metadata-only | |
| No file picker or S3 upload is falsely documented | |
| Availability without scan is blocked | |
| Infected/suspicious verdict cannot become available | |
| Clean simulated scan permits available state | |
| Separate access permissions are API-tested if in scope | |
| Cross-tenant metadata does not leak | |
| Provider scan/upload recorded Stubbed | |
| Automated tests command and result recorded | |
