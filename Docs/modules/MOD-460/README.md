# MOD-460 — Requirement Traceability, Audit Reports, and Evidence Exports

**Status:** Implementation draft (M1); AC-901 NOT obtained  
**Human Done (AC-901):** Not obtained

## Purpose

Provide org-scoped requirement-to-ticket/test/release/document link registry, ticket-test links, must-have coverage gating (≥95% for release-ready), module-local controlled-action audit coverage, evidence manifests with checksum sealing, and reconcilable in-DB evidence exports.

## Honesty (M1 limits)

- Links are **registry edges** (UUID references), not live FK enforcement to tickets/tests/releases/documents across modules.
- Exports are **in-DB `payload_preview` JSON**, not S3/file download artifacts.
- Audit coverage is **module-local** `tr_action_audits` plus observability `write_audit` on controlled mutations — not a global platform audit completeness proof.
- FE is a desk for must-haves, one link type, coverage, manifest seal/export — not a full traceability matrix studio.
- AC-901 human owner approval has **not** been obtained.

## M1 delivered

API: `/api/v1/traceability`  
Migration: `20260811_0030`  
FE: `/traceability`

### Checklist main points (DB-001..006)

| ID | Entity |
|---|---|
| MP-001 / DB-001 | `tr_requirement_ticket_links` |
| MP-002 / DB-002 | `tr_requirement_test_links` |
| MP-003 / DB-003 | `tr_requirement_release_links` |
| MP-004 / DB-004 | `tr_requirement_document_links` |
| MP-005 / DB-005 | `tr_ticket_test_links` |
| MP-006 / DB-006 | `tr_evidence_manifests` |

### M1 support tables (for AC; not extra checklist MPs)

| Table | Purpose |
|---|---|
| `tr_must_have_requirements` | Registry for AC-001 coverage calculation |
| `tr_evidence_manifest_items` | Manifest item list + checksum inputs |
| `tr_evidence_exports` | Export jobs with reconciliation_hash |
| `tr_action_audits` | Module-local audit mirror for AC-002 |

## Acceptance behavior (M1)

- **AC-001:** `GET /traceability/coverage` over registered must-haves; complete = ticket+test+release+document links; `release_ready` only when coverage ≥ 95%
- **AC-002:** Every controlled mutation writes `tr_action_audits` and `ObservabilityWriter.write_audit`; `GET /traceability/audit-coverage` returns `coverage_pct` / `complete` when audited_count == action_count (100%)
- **AC-003:** Evidence export includes `organization_id`, manifest checksum, item counts; payload reconcilable against manifest items; cross-org GET returns 404
