# MASMS Governance Package (MOD-000)

**Module:** MOD-000 — Project Governance, Source Baseline, and Change Control  
**Requirement mapping:** MVP-NFR-010, SRS Change Control  
**Document status:** Draft — pending human owner approval (MOD-000-AC-901)  
**Owner (pending):** Product Owner / Engineering Lead  
**Version:** 0.1.0  
**Effective date:** PENDING human approval  
**Review date:** PENDING

## Purpose

Establish one approved source of truth, requirement-to-module traceability, architecture decision discipline, change control, and approval evidence before and during implementation.

## Contents

| Artifact | Path | Purpose |
|---|---|---|
| Source baseline register | `SOURCE_BASELINE_REGISTER.md` | Identifies approved/draft sources of truth |
| Requirement → module map | `REQUIREMENT_MODULE_MAP.md` | Maps every MVP FR/NFR to implementation modules |
| Change control process | `CHANGE_CONTROL.md` | Versioning and CR rules for material changes |
| Approval records process | `APPROVAL_RECORDS.md` | Exact-version approval lifecycle |
| Pending decisions | `PENDING_DECISIONS.md` | Tooling/provider decisions not yet formally approved |
| ADRs | `adrs/` | Architecture and tooling decisions |
| Data dictionary | `data-dictionary/MOD-000-entities.md` | Runtime entity design for governance API |

## Acceptance criteria (module)

| ID | Criterion | Status |
|---|---|---|
| MOD-000-AC-001 | One approved source of truth is identified | Draft register exists; human approval PENDING |
| MOD-000-AC-002 | Material changes require a new version and human approval | Process documented; runtime enforced in API |
| MOD-000-AC-003 | Every implementation task maps to a module and requirement ID | Map published; keep updated with CRs |
| MOD-000-AC-900 | Critical/High defects resolved | No open Critical/High for this module yet |
| MOD-000-AC-901 | Human owner approves completion evidence | **Blocked — requires authorized human** |

## Runtime

Governance entities are also persisted via `apps/api` under `/api/v1/governance/*`.  
Authorized human approval remains mandatory for approving baselines, ADRs, and change requests; agents may draft and submit only.

## Related docs

- `Docs/Multi_Agent_Software_House_Management_System_MVP_SRS_v1.0.md`
- `Docs/Multi-Agent_Software_House_Management_System_Comprehensive_Specification_v1.1_Corrected.md`
- `MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md`
- `AGENTS.md`
