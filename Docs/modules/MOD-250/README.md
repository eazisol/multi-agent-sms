# MOD-250 — Documents, Standard Templates, Versioning, and Secure File Storage

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Manage templates, versioned documents, attachment metadata, document permissions, and scan gating so unsafe files never become available or indexed.

## M1 delivered

API: `/api/v1/documents`  
Migration: `20260811_0014`

| ID | Entity |
|---|---|
| MP-001 | `doc_documents` |
| MP-002 | `doc_document_versions` (owner, status, version, effective_at) |
| MP-003 | `doc_templates` |
| MP-004 | `doc_template_versions` |
| MP-005 | `doc_attachments` (storage_key metadata; bytes via object store) |
| MP-006 | `doc_document_permissions` (download/preview/extract/embeddings) |
| MP-007 | `doc_scan_results` |

## Limits

- FE deferred; real S3 upload/download streaming deferred (metadata + storage_key only)
- Antivirus engine is stub verdicts recorded via API
- Embedding/index consumers still deferred (MOD-370); `indexing_allowed` gate only
