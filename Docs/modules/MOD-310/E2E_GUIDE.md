# MOD-310 — Assignment Recommendations and Ownership History

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Understand how a ticket gets an accountable assignee. |
| QA | Exercise recommendations, assignment, acknowledgment, and reassignment in OpenAPI. |
| Developer | Verify membership, availability, override, and append-only history rules. |
| Owner | Confirm recommendations do not silently allocate people. |

## 2. What this module is

This module ranks eligible project members by skill and capacity, records the selected assignment, waits for acknowledgment, and preserves every allocation and reassignment.

In this company it means the system may recommend an available developer, but a controlled assignment action establishes ownership and later changes never erase the old owner.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/api/v1/assignments` | **Implemented** | Recommendations, create, acknowledge, reassign, histories |
| Recommendation heuristic | **Implemented** | Deterministic skill/capacity logic; not AI |
| Unique assignments sidebar/desk | **Planned** | None found |
| Ticket desk assignment actions | **Planned** | `/tickets` does not call assignment APIs |
| OpenAPI test path | **Implemented** | Use `/docs` |
| Temporal acknowledgment wait | **Planned** | No durable wait |
| Header identity | **Stubbed** | Not login |
| Human Done approval | **Blocked** | AC-901 not obtained |

## 4. Requirements and dependencies

- Requires a ticket from MOD-300.
- Requires project membership, skills, capacity, and leave/availability data.
- Non-members and unavailable actors are blocked unless a supported override is explicit.
- Every override requires a reason.
- Allocation and reassignment histories are append-only.

## 5. How to start

1. Start API and database.
2. Create/select a project, ticket, and at least two project members.
3. Record ticket, project, and actor UUIDs.
4. Open `http://127.0.0.1:8000/docs`.
5. Supply the standard organization/actor headers through your API client.
6. The `/tickets` desk can locate the ticket, but assignment execution is API-only.

## 6. Screens, buttons, and files

| Control | What it does | Status | Source file |
|---|---|---|---|
| Tickets → ticket row | Selects a ticket | Implemented | `apps/web/src/components/tickets-desk-page.tsx` |
| Assignment recommendation button | No such control | Planned | — |
| Assign button | No such control | Planned | — |
| Acknowledge button | No such control | Planned | — |
| Reassignment history panel | No such control | Planned | — |
| OpenAPI **Try it out** | Sends documented API request | Implemented tooling | FastAPI OpenAPI |
| OpenAPI **Execute** | Executes request and displays response | Implemented tooling | FastAPI OpenAPI |

Do not invent a sidebar route. Use OpenAPI or an HTTP client for all implemented MOD-310 actions.

## 7. API, data, and automated tests

Router: [`router.py`](../../../apps/api/src/masms_api/modules/assignments/router.py)  
Prefix: `/api/v1/assignments`

| Method | Path | Purpose |
|---|---|---|
| POST | `/assignments/recommendations` | Rank eligible members |
| POST | `/assignments` | Create assignment |
| GET | `/assignments/tickets/{ticket_id}` | List assignment records |
| GET | `/assignments/tickets/{ticket_id}/recommendations` | Read recommendations |
| GET | `/assignments/tickets/{ticket_id}/allocation-history` | Read allocation history |
| GET | `/assignments/tickets/{ticket_id}/reassignment-history` | Read reassignment history |
| POST | `/assignments/{assignment_id}/acknowledge` | Assignee acknowledgment |
| POST | `/assignments/{assignment_id}/reassign` | Close old and create new ownership |

Use schemas shown by OpenAPI; do not guess body keys.

Automated evidence:

- `tests/unit/assignments/test_assignments_domain.py`
- `tests/integration/assignments/test_assignments_api.py`
- `uv run pytest tests/unit/assignments tests/integration/assignments -q --tb=short`

## 8. Test flows

Capture request/response JSON, IDs, timestamps, history arrays, and audit/outbox evidence.

### F-SETUP

1. Prepare a ticket and two project members; one should satisfy skill/capacity.
2. Open OpenAPI → `assignments`.
3. Confirm request headers identify the intended organization and human actor.
4. **Expected:** ticket/member IDs exist; no assignment yet.

### F-HAPPY

1. Execute `POST /recommendations` for the ticket/project.
2. Expect ranked recommendation rows for eligible members.
3. Execute `POST /assignments` with the selected actor.
4. Expect an active assignment and allocation history.
5. As the assignee, execute `POST /{assignment_id}/acknowledge`.
6. Expect acknowledgment persisted.
7. Execute `POST /{assignment_id}/reassign` to the second eligible member with a reason.
8. Expect old assignment closed, new assignment active, and reassignment history appended.
9. GET both history endpoints and capture all rows.

### F-VALIDATE

1. Submit recommendation/create with a missing ticket or assignee.
2. Expect validation/not-found problem JSON.
3. Attempt an override without a reason.
4. Expect rejection and no assignment.

### F-AUTHZ

1. Attempt acknowledgment as an actor other than the assignee.
2. Attempt allocation using an unauthorized actor.
3. Expect forbidden and unchanged ownership.
4. UI role selection is not backend authorization proof.

### F-TENANT

1. Reuse ticket/assignment IDs under another organization header.
2. Expect not-found/forbidden.
3. Histories must not disclose names, capacity, or assignments across tenants.

### F-CONCUR

N/A at the HTTP contract: assignment requests do not expose an `expected_version` field. Test competing reassignment behavior in automated/domain tests and record any duplicate-active-assignment defect.

### F-TRANS

1. Acknowledge an assignment twice or after it was closed.
2. Reassign a closed assignment.
3. Expect invalid state/conflict and no rewritten history.

### F-GATE

1. Recommend an unavailable/on-leave actor.
2. Expect exclusion or blocked assignment.
3. If override is supported by the schema, provide explicit override plus reason.
4. Expect override evidence; no silent bypass.

### F-TERM

1. Reassign the active record.
2. Confirm the previous allocation remains closed and immutable.
3. There is no UI/API delete path; history remains append-only.

### F-RECOVER

1. Simulate a failed acknowledgment request.
2. Retry the same intended acknowledgment after checking current state.
3. Because Temporal wait/retry is Planned, do not claim a worker recovered it.

### F-CLEAN

Leave one clearly identified active assignment. Preserve acknowledgment, allocation, reassignment, audit, and outbox history.

## 9. Security, privacy, and approvals

- Enforce organization, project membership, availability, and actor scope server-side.
- Capacity and leave data are sensitive; capture minimum test evidence.
- Recommendations are advisory, not human approval.
- Overrides require explicit reasons and appropriate authority.
- No agent should allocate resources beyond approved authority.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Assignment controls in Tickets | Planned |
| Dedicated assignment desk | Planned |
| Durable acknowledgment timeout/escalation | Planned |
| AI matching | Not used; deterministic heuristic |
| Browser E2E | Planned |

## 11. Related journeys

- MOD-300 supplies the ticket.
- MOD-100/MOD-110/MOD-130 supply membership, capacity, and availability.
- MOD-320 may govern status changes after assignment.
- MOD-350 is the future durable acknowledgment workflow.

## 12. Pass / fail checklist

- [ ] Recommendations include only eligible members
- [ ] Non-member assignment is rejected
- [ ] Unavailable actor requires valid override and reason
- [ ] Assignment creates allocation history
- [ ] Only assignee can acknowledge
- [ ] Reassignment closes prior ownership
- [ ] Reassignment history is append-only
- [ ] Cross-tenant IDs do not disclose data
- [ ] No nonexistent UI path was tested
- [ ] Automated command/result recorded
