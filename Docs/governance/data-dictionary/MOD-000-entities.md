# MOD-000 Entity Data Dictionary

**Status:** Draft  
**Module:** MOD-000  
**Owner:** PENDING Engineering Lead  
**Version:** 0.1.0

## Common columns

All business tables include unless noted:

| Column | Type | Notes |
|---|---|---|
| `id` | UUID PK | Generated server-side |
| `organization_id` | UUID | Tenant scope; required |
| `project_id` | UUID NULL | Null for org-level governance records |
| `status` | VARCHAR | Configurable vocabulary; app validates |
| `version` | INTEGER | Optimistic concurrency + immutable approved snapshots |
| `owner_actor_id` | UUID | Responsible owner |
| `created_by_actor_id` | UUID | Creator |
| `updated_by_actor_id` | UUID | Last updater |
| `created_at` / `updated_at` | TIMESTAMPTZ | UTC |
| `deleted_at` | TIMESTAMPTZ NULL | Soft delete |
| `metadata` | JSONB | Non-authoritative extras only |

Actor and organization foreign keys are **logical** until MOD-100 ships physical identity tables.

## Tables

### `gov_source_baselines`

Register of controlled source documents (SRS, specs, matrices).

| Column | Type | Notes |
|---|---|---|
| `baseline_key` | VARCHAR | Unique per org (e.g. `BL-SRS-001`) |
| `title` | VARCHAR | |
| `artifact_path` | VARCHAR | Repo-relative or URI reference (no secrets) |
| `document_version` | VARCHAR | External document version label |
| `classification` | VARCHAR | public/internal/confidential/restricted |
| `approval_status` | VARCHAR | draft/submitted/under_review/approved/rejected/superseded |
| `effective_from` / `effective_to` | TIMESTAMPTZ NULL | |
| `supersedes_id` | UUID NULL | Prior baseline row |
| `content_sha256` | VARCHAR NULL | Integrity fingerprint of referenced artifact when available |

**Immutability:** rows with `approval_status=approved` are immutable; changes require a new row/version via CR.

### `gov_requirement_mappings`

Maps requirement IDs to modules.

| Column | Type | Notes |
|---|---|---|
| `requirement_id` | VARCHAR | e.g. `MVP-FR-001` |
| `requirement_title` | VARCHAR | |
| `module_id` | VARCHAR | e.g. `MOD-100` |
| `mapping_role` | VARCHAR | `primary` or `supporting` |
| `notes` | TEXT NULL | |

Unique `(organization_id, requirement_id, module_id, mapping_role)` where not deleted.

### `gov_architecture_decisions`

ADR records.

| Column | Type | Notes |
|---|---|---|
| `adr_key` | VARCHAR | e.g. `ADR-0001` |
| `title` | VARCHAR | |
| `status` | VARCHAR | proposed/accepted/deprecated/superseded |
| `context` | TEXT | |
| `decision` | TEXT | |
| `consequences` | TEXT | |
| `security_notes` | TEXT NULL | |
| `document_path` | VARCHAR NULL | |

### `gov_change_requests`

Governance change requests against baselines/ADRs/maps.

| Column | Type | Notes |
|---|---|---|
| `change_request_key` | VARCHAR | |
| `title` / `summary` / `rationale` | TEXT | |
| `impact` | JSONB | Structured impact fields |
| `target_entity_type` | VARCHAR | baseline/adr/requirement_mapping/… |
| `target_entity_id` | UUID | |
| `target_version` | INTEGER | Exact version under change |
| `proposed_version` | INTEGER | |
| `priority` | VARCHAR | |
| `idempotency_key` | VARCHAR NULL | Unique per org when present |

### `gov_approval_records`

Exact-version approvals.

| Column | Type | Notes |
|---|---|---|
| `target_entity_type` | VARCHAR | |
| `target_entity_id` | UUID | |
| `target_version` | INTEGER | |
| `decision` | VARCHAR | approved/rejected/withdrawn/… |
| `approver_actor_id` | UUID | Must be human for approval |
| `authority_level` | INTEGER | Claimed level 1–5 |
| `reason` | TEXT NULL | Required for reject/withdraw/override |
| `decided_at` | TIMESTAMPTZ | |
| `correlation_id` | UUID | |

### `gov_audit_events`

Append-only controlled-action log for governance module.

| Column | Type | Notes |
|---|---|---|
| `actor_id` | UUID | |
| `actor_kind` | VARCHAR | human/agent/system/integration |
| `action` | VARCHAR | |
| `entity_type` / `entity_id` | VARCHAR / UUID | |
| `entity_version` | INTEGER NULL | |
| `reason` | TEXT NULL | |
| `source` | VARCHAR | api/ui/agent/… |
| `correlation_id` | UUID | |
| `payload_redacted` | JSONB | Never secrets |

## RLS (design)

Sensitive tables enable RLS keyed by `organization_id` using session `app.current_organization_id`.
Application filters do not replace RLS tests (MOD-000-SEC / MOD-120 hardening).

## Migration behavior

- Alembic revision under `migrations/versions/`  
- No cascade deletes  
- Soft delete filters on default queries  
- Approved baseline/ADR updates rejected at service layer
