# MOD-330 — Human Approval Gates, Delegation, Rejection, and Override

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Enforce exact-version human approval for high-risk actions, with multi-step workflows, decisions, delegations, evidence, and emergency overrides.

## M1 delivered

API: `/api/v1/approvals`  
Migration: `20260811_0019`

| ID | Entity |
|---|---|
| MP-001 | `apr_requests` |
| MP-002 | `apr_workflows` (frozen snapshot) |
| MP-003 | `apr_steps` |
| MP-004 | `apr_decisions` (append-only) |
| MP-005 | `apr_delegations` |
| MP-006 | `apr_evidence` |
| MP-007 | `apr_overrides` |

## Acceptance highlights

- **AC-001:** `gate-check` / `gate-assert` block dependents until exact-version approval or override
- **AC-002:** Requests lock `target_version`; wrong version does not unlock
- **AC-003:** Only humans decide; actors cannot approve their own recommendations

## Limits

- FE deferred
- Temporal waits for pending approvals deferred
- Full org approval-authority matrix from MOD-120 is advisory; step assignee + delegation enforced in M1
