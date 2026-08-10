# MOD-000 UI Role Variants and Access Rules

**Checklist ID:** CHK-MOD-000-RDY-005  
**Artifact ID:** UI-GOV-001  
**Module:** MOD-000 — Project Governance, Source Baseline, and Change Control  
**Requirements:** MVP-NFR-001, MVP-NFR-010, MVP-FR-008 (governance instances)  
**Status:** Draft (design complete for readiness; named humans still PENDING)  
**Owner:** PENDING Product Owner / Engineering Lead  
**Version:** 0.1.0  
**Created (UTC):** 2026-08-10T00:00:00Z  
**Effective date:** PENDING human approval of this matrix  
**Review date:** PENDING

## Purpose

Define UI variants and access rules for governance screens so frontend work (MOD-000-FE-*) and future RBAC (MOD-110/120) have an explicit deny-by-default matrix.  
Server authorization remains authoritative; UI hide/disable is never the only control.

## Principles

1. Deny by default.  
2. Agents never receive final-approve / reject / override controls that commit authority.  
3. Org scope is always enforced; no cross-organization navigation.  
4. Approved baselines/ADRs are read-only; edits require a new version / governance CR.  
5. Disabled actions show why (missing role, wrong status, stale version, approval required).  
6. Named human assignees for roles remain PENDING (`PENDING_DECISIONS.md`).

## UI role variants (governance module)

| Variant ID | Actor kind | Typical org roles (pending named people) | Purpose of UI |
|---|---|---|---|
| `gov.viewer` | human | Department members with governance read access; Client Viewer (if ever granted org-internal docs — default deny for clients) | Read-only lists and detail |
| `gov.contributor` | human | Engineers, PMs, BD preparing drafts | Create/edit drafts, submit for review |
| `gov.adr_approver` | human | Engineering Lead / Architect (authority level ≥4 for major infra) | Accept/deprecate ADRs; review CRs targeting ADRs |
| `gov.baseline_approver` | human | Product Owner / Management (authority level ≥3) | Approve/reject source baselines and mapping baselines |
| `gov.cr_approver` | human | Product Owner and/or Engineering Lead by impact | Approve/reject/apply governance change requests |
| `gov.admin` | human | Company Admin / Ops managing governance configuration | Full human governance actions within org + audit export |
| `gov.agent_drafter` | agent | Documentation / Orchestrator / specialized agents | Draft and submit only; no approve UI |
| `gov.forbidden` | any | Unauthenticated, wrong org, suspended | No module access |

Client-facing Product Owner roles may approve **project** artifacts (MOD-240/330) but do **not** by default approve platform governance baselines unless explicitly granted `gov.baseline_approver`.

## Screens (planned FE)

| Screen ID | Route (planned) | Description |
|---|---|---|
| `S-LIST-BASELINES` | `/governance/baselines` | Baseline register list |
| `S-DETAIL-BASELINE` | `/governance/baselines/:id` | Baseline detail, versions, approvals, audit |
| `S-FORM-BASELINE` | `/governance/baselines/new` / `:id/edit` | Create/edit draft baseline |
| `S-LIST-MAPPINGS` | `/governance/requirement-mappings` | Requirement → module map |
| `S-FORM-MAPPING` | `/governance/requirement-mappings/new` | Create mapping |
| `S-LIST-ADRS` | `/governance/architecture-decisions` | ADR list |
| `S-DETAIL-ADR` | `/governance/architecture-decisions/:id` | ADR detail |
| `S-FORM-ADR` | `/governance/architecture-decisions/new` | Create ADR |
| `S-LIST-CRS` | `/governance/change-requests` | Governance CR list |
| `S-DETAIL-CR` | `/governance/change-requests/:id` | CR detail + transitions |
| `S-FORM-CR` | `/governance/change-requests/new` | Create CR |
| `S-LIST-APPROVALS` | `/governance/approvals` | Approval decisions |
| `S-AUDIT` | `/governance/audit` | Governance audit trail |

## Action vocabulary

| Action | Meaning |
|---|---|
| `view_list` | See list/table |
| `view_detail` | Open detail |
| `create` | Create draft |
| `edit_draft` | Patch while mutable |
| `submit` | Transition toward review |
| `approve` | Authoritative approve/accept |
| `reject` | Reject with reason |
| `withdraw` | Withdraw own or permitted submission |
| `supersede` | Mark superseded after successor exists |
| `apply_cr` | Mark approved CR applied |
| `export_audit` | Export audit (sensitive) |

## Access matrix

Legend: `A` = allow (show enabled) · `D` = disable visible with reason · `H` = hide · `-` = deny/hide entire screen

### Source baselines

| Action | viewer | contributor | adr_approver | baseline_approver | cr_approver | admin | agent_drafter |
|---|---|---|---|---|---|---|---|
| view_list | A | A | A | A | A | A | A |
| view_detail | A | A | A | A | A | A | A |
| create | H | A | A | A | A | A | A |
| edit_draft | H | A* | A* | A* | A* | A | A* |
| submit | H | A* | A* | A* | A* | A | A* |
| approve | H | H | H | A | D† | A | H |
| reject | H | H | H | A | D† | A | H |
| supersede | H | H | H | A | D† | A | H |

\* Only when status is mutable (`draft` / `more_info_required` / equivalent) and `expected_version` matches.  
† Disable unless also granted `baseline_approver` or target is CR-linked baseline with delegated authority.

### Requirement mappings

| Action | viewer | contributor | adr_approver | baseline_approver | cr_approver | admin | agent_drafter |
|---|---|---|---|---|---|---|---|
| view_list / view_detail | A | A | A | A | A | A | A |
| create / edit_draft | H | A | A | A | A | A | A |
| Material remapping of scope | H | D‡ | D‡ | A | A | A | H |

‡ Requires an approved governance CR; show CR create CTA instead of silent edit.

### Architecture decisions (ADRs)

| Action | viewer | contributor | adr_approver | baseline_approver | cr_approver | admin | agent_drafter |
|---|---|---|---|---|---|---|---|
| view_list / view_detail | A | A | A | A | A | A | A |
| create / edit `proposed` | H | A | A | A | A | A | A |
| accept (approve) | H | H | A | H | D | A | H |
| deprecate / supersede | H | H | A | H | D | A | H |

### Governance change requests

| Action | viewer | contributor | adr_approver | baseline_approver | cr_approver | admin | agent_drafter |
|---|---|---|---|---|---|---|---|
| view_list / view_detail | A | A | A | A | A | A | A |
| create / edit draft / submit | H | A | A | A | A | A | A |
| approve / reject | H | H | D§ | D§ | A | A | H |
| apply_cr / close | H | H | H | H | A | A | H |
| withdraw | H | A‖ | A‖ | A‖ | A | A | A‖ |

§ Allow when CR target is ADR and user is `adr_approver`, or target is baseline and user is `baseline_approver`.  
‖ Own submissions only unless admin.

### Approvals & audit

| Action | viewer | contributor | adr_approver | baseline_approver | cr_approver | admin | agent_drafter |
|---|---|---|---|---|---|---|---|
| view approvals list/detail | A | A | A | A | A | A | A |
| create approval decision | H | H | A¶ | A¶ | A¶ | A | H |
| view audit | D# | D# | A | A | A | A | H |
| export_audit | H | H | H | H | H | A | H |

¶ Only for entity types within that variant’s approval scope and exact `target_version`.  
# Contributors/viewers may see audit on records they can open if classification ≤ Internal; Restricted audit is admin+.

## Empty / loading / forbidden UI rules

| State | Behavior |
|---|---|
| Loading | Skeleton on list/detail; no speculative enable of approve |
| Empty list | Role-specific empty copy + primary CTA only if `create` allowed |
| Forbidden (403) | Dedicated forbidden variant; no chrome that implies edit rights |
| Stale version | Block submit/approve; prompt refresh |
| Agent session | Badge “Agent — draft only”; approve controls absent (`H`) |

## Server enforcement mapping (current stub → future RBAC)

| UI rule | Current API enforcement (MOD-000) | Future (MOD-110/120) |
|---|---|---|
| Agent cannot approve | `ActorKind` must be `human` for approve transitions | Role permissions + authority level |
| Org isolation | `X-Organization-Id` filter + planned RLS | Session org + RLS + membership |
| Optimistic concurrency | `expected_version` | Same + ETag optional |
| Exact-version approval | Approval record stores `target_version` | Bind to approval workflow engine (MOD-330) |

## Out of scope for this matrix

- Project-level client PO approval of SRS/tickets (MOD-240/330)  
- Full permission admin UI (MOD-120/140)  
- Pixel-level visual design (MOD-000-FE + design system)

## Readiness satisfaction

This document satisfies **CHK-MOD-000-RDY-005** as the definition of UI role variants and access rules for MOD-000.  
Frontend implementation remains tracked under `CHK-MOD-000-FE-*` (still open).
