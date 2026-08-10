# MOD-000 Governance Workflow Definition

**Checklist IDs:** MOD-000-WF-001 … WF-004 · CHK-MOD-000-WF-*  
**Artifact ID:** WF-GOV-001  
**Module:** MOD-000  
**Requirements:** MVP-NFR-010, SRS Change Control, MVP-FR-008 (governance approvals)  
**Status:** Draft  
**Owner:** PENDING Product Owner / Engineering Lead  
**Version:** 0.1.0  
**Created (UTC):** 2026-08-10T00:00:00Z

## Purpose

Define how governance objects move from draft to approved/closed, who owns each step, what waits apply, how events and correlation work, and what is deliberately deferred to Temporal, LangGraph, or notifications modules.

## Architecture routing (MOD-000-WF-002)

| Concern | Owner in MOD-000 | Future owner |
|---|---|---|
| State mutations (create, update, transition, approve) | **FastAPI** `GovernanceService` | same |
| Long-running waits / reminder timers / SLA escalation | **N/A in MOD-000** (no durable wait required for synchronous governance transitions) | Temporal (MOD-350) when approval SLAs need timed escalation |
| Bounded AI drafting of baselines/ADRs/CRs | **N/A in MOD-000** (humans/agents draft via API/UI only) | LangGraph (MOD-360) under supervision |
| Notifications | **N/A in MOD-000** | MOD-440 |

**Rule:** Agents and Temporal workers must not write governance tables directly. They call FastAPI APIs.

## Workflow catalog (MOD-000-WF-001)

### Common fields on every handoff

- Trigger  
- Owner (responsible actor role)  
- Inputs / outputs  
- Status before → after  
- Wait / reminder / escalation (if any)  
- Approval required?  
- Evidence required  
- Closure condition  

### WF-GOV-BASELINE — Source baseline approval

| Step | Trigger | Owner | Inputs | Outputs | Transition | Wait / escalate | Approval | Evidence | Closure |
|---|---|---|---|---|---|---|---|---|---|
| 1 Create | User/agent posts draft | Contributor / agent drafter | Artifact path, version label | Baseline `draft` v1 | — → draft | None | No | Audit `create` | — |
| 2 Submit | Owner submits | Contributor | Baseline id + expected_version | `submitted` | draft → submitted | Optional future SLA to review (Temporal) | No | Audit `transition` | — |
| 3 Review | Reviewer opens queue | Baseline approver / admin | Baseline at submitted | `under_review` | submitted → under_review | Same | No | Audit | — |
| 4a Approve | Human approves | Baseline approver / admin (**human only**) | exact version | `approved` + effective_from | under_review → approved | None in stub | **Yes** | Audit + optional approval record | Baseline immutable |
| 4b Reject | Human rejects with reason | Baseline approver / admin | reason | `rejected` | under_review → rejected | None | **Yes** (decision) | Audit with reason | May return to draft |
| 5 Supersede | Successor approved | Approver / admin | prior + new baseline | prior `superseded` | approved → superseded | None | Yes | Audit | Historical retention |

**More info loop:** `under_review` → `more_info_required` → `submitted` (reason required).

**Allowed transitions:** see `apps/api/.../governance/domain.py` `BASELINE_TRANSITIONS`.

### WF-GOV-ADR — Architecture decision

| Step | Trigger | Owner | Transition | Approval | Notes |
|---|---|---|---|---|---|
| Create | Draft ADR | Contributor / agent | → `proposed` | No | |
| Accept | Human accept | ADR approver / admin | proposed → accepted | **Human only** | Major infra still needs named Level 4 human (PENDING) |
| Deprecate / supersede | Policy change | ADR approver / admin | accepted → deprecated/superseded | Human | |

### WF-GOV-MAPPING — Requirement → module mapping

| Step | Trigger | Owner | Approval | Notes |
|---|---|---|---|---|
| Create / maintain | Contributor | Contributor / admin | Material remaps require governance CR | Unique (org, requirement, module, role) |

### WF-GOV-CR — Governance change request

| Step | Trigger | Owner | Transition | Approval | Closure |
|---|---|---|---|---|---|
| Draft | Material change needed | Contributor / agent | → draft | No | |
| Submit / review | Submitter | CR approver | → submitted → under_review | No until decision | |
| Approve | Human | CR / baseline / ADR approver by target type | → approved | **Human only** | |
| Apply | Admin / CR owner | → applied | Target new version created outside silent edit | Evidence of applied artifact |
| Close | Owner | → closed | Terminal | Children none (no child follow-ups in stub) |

Idempotency: create with `idempotency_key` returns existing row.

### WF-GOV-APPROVAL — Exact-version decision

| Step | Trigger | Owner | Rules |
|---|---|---|---|
| Decide | Approver records decision | Human only | Binds `target_entity_type`, `target_entity_id`, `target_version`; reason required for reject/withdraw/override |

### Human intervention points (conflict / missing authority)

- Agent attempts approve/reject → **403 forbidden**  
- Stale `expected_version` → **409 conflict**  
- Invalid transition → **409 invalid_transition**  
- Edit approved baseline → **409 approval_required** (create CR / new version)  
- Missing named human approver in production → **block Done** (AC-901 / RDY-003 PENDING)

## Status summary

### Baseline `approval_status`

`draft` → `submitted` → `under_review` ↔ `more_info_required` → `approved` | `rejected` | `withdrawn` · `approved` → `superseded`

### ADR `status`

`proposed` → `accepted` → `deprecated` | `superseded`

### Change request `status`

`draft` → `submitted` → `under_review` → `approved` → `applied` → `closed`  
also `rejected` / `withdrawn` → `closed`

## Waits, reminders, escalations (MOD-000 scope)

| Item | MOD-000 behavior | Later |
|---|---|---|
| Synchronous review handoffs | Immediate API transitions; no timer | — |
| Approval SLA reminders | **Not implemented** | Temporal + MOD-340 follow-ups |
| Escalation ladder | Documented in Approval Gates / Follow-Up Docs; not auto-fired | MOD-340 / MOD-350 |
| Parent/child follow-ups | N/A (no governance follow-up entity yet) | MOD-340 |

## Domain events and outbox (MOD-000-WF-003)

### Event names (defined now; publisher may be stubbed)

| Event type | When | Payload (redacted) |
|---|---|---|
| `governance.baseline.created` | create | id, org, baseline_key, version |
| `governance.baseline.transitioned` | status change | id, from, to, version, actor |
| `governance.baseline.approved` | approved | id, version, effective_from |
| `governance.adr.transitioned` | ADR status change | id, adr_key, to, version |
| `governance.change_request.created` | CR create | id, key, target_* |
| `governance.change_request.transitioned` | CR status change | id, to, version |
| `governance.approval.decided` | approval record | target_*, decision, authority_level |

### Publication rules

1. Persist business row + outbox row in the **same DB transaction** (when outbox table exists — MOD-020).  
2. Until outbox ships, **audit events** (`gov_audit_events`) are the durable local evidence stream.  
3. Consumers must be **idempotent** on `(event_id)` or `(entity_type, entity_id, action, entity_version, action_id)`.  
4. **Correlation ID** required on every API call (`X-Correlation-Id`) and stored on audit/approval rows.  
5. **Causation ID** (optional header later) links follow-on events to the triggering event.  
6. Retry: exponential backoff; after N failures → dead-letter with reason; replay is manual/admin with audit.  
7. No secrets/PII in event payloads; use `payload_redacted` pattern already on audit rows.

### Current runtime

- Correlation IDs: **implemented** on API → audit  
- Outbox table + publisher/consumer: **not implemented** (tracked MOD-020 / MOD-500)  
- DLQ/replay tooling: **defined here**, not built  

## Notifications (MOD-000-WF-004)

| Topic | MOD-000 |
|---|---|
| Recipients / channels / quiet hours / digests | Deferred to **MOD-440** |
| Governance-specific hooks | When MOD-440 exists: notify baseline approvers on `submitted` / `under_review`; notify submitter on approve/reject |

No notification sending from MOD-000 code paths.

## Evidence and closure checklist per workflow

- [ ] Audit row written for create/update/transition/approval  
- [ ] Version incremented on mutating transitions  
- [ ] Human actor for approve/reject  
- [ ] Reason present when required  
- [ ] Approved baselines/ADRs treated immutable in service  
- [ ] CR idempotency honored when key provided  

## Related code / docs

- Domain transitions: `apps/api/src/masms_api/modules/governance/domain.py`  
- Service mutations: `.../governance/service.py`  
- UI role gates: `docs/governance/UI_ROLE_VARIANTS.md`  
- Approvals process: `docs/governance/APPROVAL_RECORDS.md`  
- Change control: `docs/governance/CHANGE_CONTROL.md`

## Satisfaction of plan tasks

| Task | Result |
|---|---|
| MOD-000-WF-001 | **Done** — workflows defined above |
| MOD-000-WF-002 | **N/A** — no durable waits/AI reasoning in MOD-000; FastAPI owns mutations |
| MOD-000-WF-003 | **Done (definition)** — events, outbox, idempotency, correlation, retry/DLQ/replay rules documented; runtime outbox deferred |
| MOD-000-WF-004 | **N/A** — notifications deferred to MOD-440 |
