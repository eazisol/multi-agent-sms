# Change Control Process

**Artifact ID:** CHG-CTL-001  
**Module:** MOD-000  
**Requirements:** MVP-NFR-010, SRS Change Control, MOD-000-AC-002  
**Status:** Draft  
**Owner:** PENDING Product Owner  
**Version:** 0.1.0

## When a change request is required

Open a **Governance Change Request (GCR)** for any material change to:

- Approved SRS / requirement baselines  
- MVP scope or exclusions  
- Status/transition, follow-up/escalation, or approval-gate configuration baselines  
- Major architecture or infrastructure decisions  
- Security, privacy, retention, or model-data policies  
- Requirement → module mapping that alters delivery scope  

Editorial fixes that do not change meaning may be recorded as a patch note without a GCR only when the human document owner confirms non-materiality.

## Lifecycle

`draft → submitted → under_review → approved | rejected | withdrawn | superseded → applied → closed`

Rules:

1. Agents may draft and submit; agents must not approve.  
2. Approval binds to the **exact target entity and version**.  
3. Any material edit after submission creates a **new version** and invalidates the prior approval request.  
4. Rejection, override, withdrawal, and emergency action require a reason.  
5. History is append-only.  
6. Downstream implementation must not treat unapproved drafts as authoritative.

## Required GCR fields

- `change_request_key` (human-readable)  
- `organization_id`  
- `title`, `summary`, `rationale`  
- `impact` (scope, security, cost, schedule, risk)  
- `target_entity_type`, `target_entity_id`, `target_version`  
- `proposed_version`  
- `priority`  
- `status`  
- `owner_actor_id`, `created_by_actor_id`  
- `idempotency_key` (for API creates)  

## Relationship to product change requests (MOD-420)

| Type | Purpose | Module |
|---|---|---|
| Governance CR | Changes to MASMS product baselines, architecture, and engineering governance | MOD-000 |
| Project CR | Client/project scope, timeline, or requirement changes after baseline | MOD-420 |

Do not conflate the two. Project CRs still require human gates defined in the Approval Gates document.

## Runtime

GCRs are stored by the governance API (`/api/v1/governance/change-requests`).  
Approved documents remain immutable; applying an approved GCR produces a new baseline version.
