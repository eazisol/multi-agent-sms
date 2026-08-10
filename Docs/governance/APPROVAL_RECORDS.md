# Approval Records Process

**Artifact ID:** APR-REC-001  
**Module:** MOD-000  
**Requirements:** MVP-FR-008 (governance instances), MVP-NFR-010, MOD-000-AC-002 / AC-901  
**Status:** Draft  
**Owner:** PENDING Product Owner  
**Version:** 0.1.0

## Principle

An approval applies only to the exact submitted entity version.
Agents submit and track. Configured humans decide.

## Lifecycle

`draft → submitted → assigned → acknowledged → under_review ↔ more_info_required → approved | rejected | withdrawn | expired | superseded → applied → closed`

## Mandatory for MOD-000

| Gate | Target | Minimum authority (pending named humans) | Agent may |
|---|---|---|---|
| Approve source baseline (e.g. MVP SRS) | `source_baseline` version | Product Owner / Management (Level 3+) | Draft/submit only |
| Approve ADR (major) | `architecture_decision` version | Engineering Lead / Architect (Level 4 for major infra) | Draft/submit only |
| Approve governance CR | `governance_change_request` version | Product Owner / Engineering Lead by impact | Draft/submit only |
| Mark MOD-000 Done | Module completion evidence | Named module owner | Prepare evidence only |

## Record fields

- Organization scope  
- Target type, ID, and **exact version**  
- Decision (`approved` / `rejected` / …)  
- Approver actor ID and authority level claimed  
- Reason (required for reject/override/withdraw)  
- Decision timestamp (UTC)  
- Correlation ID  
- Optional evidence references  

## Enforcement

- Backend rejects approve actions from agent actors.  
- Backend rejects approve when `target_version` mismatches current immutable candidate.  
- Material edit after submission → new version; prior approval request superseded.  
- Audit event written for submit, approve, reject, withdraw, override.

## Human naming (PENDING)

Named approvers for production gates are **not** finalized (see `PENDING_DECISIONS.md`).  
Do not treat placeholder roles as authorized individuals.
