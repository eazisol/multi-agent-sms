# Source Baseline Register

**Artifact ID:** BASELINE-REG-001  
**Module:** MOD-000  
**Requirements:** MVP-NFR-010, SRS Change Control  
**Status:** Draft  
**Owner:** PENDING named Product Owner  
**Version:** 0.1.0  
**Created (UTC):** 2026-08-10T00:00:00Z  
**Effective date:** PENDING human approval  
**Review date:** PENDING

## Rule

Only one *approved* functional source of truth governs implementation at a time.
Supporting Docs clarify process and constraints but do not silently override an approved SRS version.
Material edits create a new version and require a change request plus human approval.

## Register

| Baseline ID | Artifact | Path / location | Version | Classification | Approval status | Effective date | Supersedes | Notes |
|---|---|---|---|---|---|---|---|---|
| BL-SRS-001 | MVP SRS | `Docs/Multi_Agent_Software_House_Management_System_MVP_SRS_v1.0.md` | v1.0 | Internal | Draft for Stakeholder Review | PENDING | — | Functional SoT candidate (MOD-000-AC-001) |
| BL-SPEC-001 | Comprehensive Specification | `Docs/Multi-Agent_Software_House_Management_System_Comprehensive_Specification_v1.1_Corrected.md` | v1.1 Corrected | Internal | Corrected Content-Complete Draft for Review | PENDING | — | Supporting consolidation; not a silent override of SRS |
| BL-PLAN-001 | Module-wise Implementation Plan | `MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md` | Implementation Baseline Draft | Internal | Draft | PENDING | — | Execution order only; does not invent product scope |
| BL-CHK-001 | Complete Development Checklist | `MASMS_CURSOR_COMPLETE_DEVELOPMENT_CHECKLIST.md` | Working | Internal | Draft | PENDING | — | Evidence gate; unchecked ≠ complete |
| BL-RULES-001 | Cursor Rules Package | `.cursor/rules/`, `AGENTS.md`, `CURSOR_RULES_MASTER.md` | Installed package | Internal | Installed | PENDING formal product approval of governed sections | — | Engineering constraints derived from Docs |
| BL-TECH-001 | Tech Stack | `Docs/Multi-Agent Software House Management System Tech Stack.md` | Draft | Internal | Draft | PENDING | — | Stack guidance |
| BL-SEC-001 | Security and Access Requirements | `Docs/Multi-Agent Software House Management System Security and Access Requirements.md` | Draft | Confidential | Draft | PENDING | — | Security policy candidate |
| BL-APR-001 | Human Approval Gates | `Docs/Multi-Agent Software House Management System  Human Approval Gates.md` | Draft | Internal | Draft | PENDING | — | Approval gate matrix |
| BL-WF-001 | Workflows | `Docs/Multi-Agent Software House Management System Workflows.md` | Draft | Internal | Draft | PENDING | — | 12 bidirectional workflows |
| BL-ST-001 | Statuses and Transitions | `Docs/Multi-Agent Software House Management System Define Statuses and Transition Rules.md` | Draft | Internal | Draft | PENDING | — | Configurable status models |
| BL-FU-001 | Follow-Up and Escalation Rules | `Docs/Multi-Agent Software House Management System Follow-Up and Escalation Rules.md` | Draft | Internal | Draft | PENDING | — | SLA / escalation defaults |
| BL-RACI-001 | Responsibility Matrix | `Docs/Multi-Agent Software House Management System Human and Agent Responsibility Matrix.md` | Draft | Internal | Draft | PENDING | — | Human vs agent authority |
| BL-DATA-001 | Required Data Structure | `Docs/Multi-Agent Software House Management System Required Data Structure.md` | Draft | Internal | Draft | PENDING | — | Entity design guidance |
| BL-ACC-001 | Success and Acceptance Criteria | `Docs/Multi-Agent Software House Management System Success and Acceptance Criteria.md` | Draft | Internal | Draft | PENDING | — | Acceptance / exit criteria |

## Precedence (when conflicting)

1. Legal / Security policy (when approved)  
2. Client contract (when applicable)  
3. Approved MVP SRS version  
4. Approved Change Request against that SRS  
5. Approved project process  
6. Comprehensive Spec / supporting Docs  
7. Implementation plan / checklist / Cursor rules  

Unresolved conflicts → record as **pending** and open a clarification / change request. Do not invent or broaden scope.

## Human actions required

1. Name the Product Owner and Engineering Lead responsible for this register.  
2. Approve BL-SRS-001 (or a successor version) as the functional baseline.  
3. Approve or formally exclude supporting baselines above.  
4. Record approvals in `APPROVAL_RECORDS.md` and in the governance API.
