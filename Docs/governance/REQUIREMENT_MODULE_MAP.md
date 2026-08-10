# Requirement → Module Mapping

**Artifact ID:** REQ-MAP-001  
**Module:** MOD-000  
**Requirements:** MVP-NFR-010, SRS Change Control, MOD-000-AC-003  
**Status:** Draft  
**Owner:** PENDING Engineering Lead  
**Version:** 0.1.0  
**Created (UTC):** 2026-08-10T00:00:00Z

## Rule

Every implementation task must cite at least one requirement ID and one module ID.
Agents must not invent requirements. Unsupported work is recorded as pending or opened as a CR.

## Functional requirements

| Requirement ID | Title | Primary modules | Supporting modules |
|---|---|---|---|
| MVP-FR-001 | Identity, actors, roles and project access | MOD-100, MOD-110, MOD-120 | MOD-030, MOD-040 |
| MVP-FR-002 | Client, contact and query management | MOD-200, MOD-210 | MOD-220, MOD-510 |
| MVP-FR-003 | Requirement gathering and brief | MOD-230 | MOD-210, MOD-220, MOD-250, MOD-330 |
| MVP-FR-004 | Project and SRS management | MOD-240, MOD-260 | MOD-250, MOD-330 |
| MVP-FR-005 | Ticket and assignment management | MOD-300, MOD-310 | MOD-130, MOD-320 |
| MVP-FR-006 | Agent orchestration | MOD-350, MOD-360 | MOD-370, MOD-040 |
| MVP-FR-007 | Bidirectional follow-up engine | MOD-340 | MOD-350, MOD-440 |
| MVP-FR-008 | Human approval workflows | MOD-330 | MOD-420, MOD-430 |
| MVP-FR-009 | QA and bug lifecycle | MOD-400, MOD-410 | MOD-430 |
| MVP-FR-010 | Documents and knowledge | MOD-250, MOD-370 | MOD-040 |
| MVP-FR-011 | Messages and notifications | MOD-220, MOD-440 | MOD-510 |
| MVP-FR-012 | Dashboard and reporting | MOD-450 | MOD-460 |
| MVP-FR-013 | Audit and traceability | MOD-040, MOD-460 | MOD-240, MOD-300, MOD-400 |
| MVP-FR-014 | Gmail integration | MOD-510 | MOD-500, MOD-220 |
| MVP-FR-015 | Jira integration | MOD-520 | MOD-500, MOD-300 |
| MVP-FR-016 | Configuration administration | MOD-140, MOD-320 | MOD-000 |

## Non-functional requirements

| Requirement ID | Title | Primary modules | Supporting modules |
|---|---|---|---|
| MVP-NFR-001 | Security | MOD-110, MOD-120, MOD-600 | MOD-030 |
| MVP-NFR-002 | Client isolation | MOD-120, MOD-600 | MOD-370, MOD-500 |
| MVP-NFR-003 | Performance | MOD-610 | MOD-450 |
| MVP-NFR-004 | Reliability | MOD-350, MOD-610 | MOD-500 |
| MVP-NFR-005 | Audit | MOD-040, MOD-460 | All modules with controlled actions |
| MVP-NFR-006 | Availability | MOD-610 | MOD-030 |
| MVP-NFR-007 | Backup and recovery | MOD-030, MOD-600, MOD-610 | — |
| MVP-NFR-008 | AI governance | MOD-360, MOD-370, MOD-600 | — |
| MVP-NFR-009 | Privacy | MOD-600 | MOD-360, MOD-440 |
| MVP-NFR-010 | Configurability / change control | MOD-000, MOD-140, MOD-320 | MOD-330 |

## Phase 0 foundation (non-product FR but plan-mandatory)

| Module | Purpose | Plan / rule references |
|---|---|---|
| MOD-000 | Governance, baseline, change control | MVP-NFR-010, SRS Change Control |
| MOD-010 | Repo, toolchain, local environment | Cursor Rules 010, 600–720 |
| MOD-020 | Shared architecture / domain kernel | MVP-NFR-004, MVP-NFR-010 |
| MOD-030 | Env, secrets, CI/CD, deploy skeleton | MVP-NFR-001, MVP-NFR-007 |
| MOD-040 | Observability and audit foundation | MVP-FR-013, MVP-NFR-005 |

## MVP exclusions (do not map to delivery code)

From MVP SRS exclusions (abridged): automatic final pricing approval; fully autonomous sensitive client communication; automatic production deployment authorization; payroll; employee performance scoring; unrestricted code generation/merge/destructive DB execution; multiple competing communication/work-management providers in v1; full CRM/accounting/time-tracking replacement; autonomous legal/contractual/security-exception decisions.

## Change rule

Updates to this map that reassign scope across modules or add/remove requirement coverage require a governance change request and human approval.
