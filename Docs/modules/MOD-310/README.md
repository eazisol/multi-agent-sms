# MOD-310 — Skill- and Capacity-Based Assignment and Ownership History

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Recommend and approve ticket assignments using project membership, skills, capacity, and leave; preserve immutable allocation and reassignment history.

## M1 delivered

API: `/api/v1/assignments`  
Migration: `20260811_0017`

| ID | Entity |
|---|---|
| MP-001 | `asg_assignments` |
| MP-002 | `asg_assignment_recommendations` |
| MP-003 | `asg_allocation_history` (append-only) |
| MP-004 | `asg_acknowledgments` |
| MP-005 | `asg_reassignment_history` (append-only) |

## Acceptance highlights

- **AC-001:** Non-members and unavailable actors blocked (unless explicit override)
- **AC-002:** Overrides require a reason
- **AC-003:** Allocation / reassignment history is append-only

## Limits

- FE deferred
- Recommendation scoring is deterministic capacity+skill heuristic (not LangGraph)
- Temporal wait-for-ack deferred
