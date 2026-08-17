# MOD-300 — Tickets, Readiness, Delivery, and Completion

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create a ticket and move it through delivery. |
| QA | Prove readiness, Done, reopen, tenant, and concurrency rules. |
| Developer | Trace the desk to API routes and automated tests. |
| Owner | Confirm completion and reopen retain evidence. |

## 2. What this module is

Tickets turn approved requirements into controlled work. A ticket carries delivery detail, readiness checks, status, Done checks, and evidence.

In this company it means a developer cannot call a vague backlog item Ready, and completed work cannot silently return to development.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/tickets` desk | **Implemented** | Create, list, search, filter, paginate, transition, reopen |
| Readiness preparation | **Implemented** | Combined desk shortcut fills missing defaults and satisfies checks |
| Delivery transitions and Done checks | **Implemented** | Buttons call the ticket transition API |
| Assignment recommendations/history | **Implemented API** | MOD-310; not displayed by this desk |
| Configurable status-engine actions | **Implemented API** | MOD-320; this desk uses ticket-local transition buttons |
| Temporal assignment/escalation | **Planned** | No live durable workflow here |
| Header identity | **Stubbed** | Not authentication |
| Human Done approval | **Blocked** | README/verification say AC-901 not obtained |

## 4. Requirements and dependencies

- Requires an organization, project, phase, and approved requirement.
- Ready requires description, requirement link, acceptance criteria, estimate, Definition of Done, phase, owner/queue, and readiness checks.
- Done requires `passed_qa` plus satisfied Done checks.
- Reopen requires a human actor, reason, evidence, and current version.

## 5. How to start

1. Start API/web per [conventions](../../testing/TESTING_CONVENTIONS.md).
2. Create/select a project, phase, and requirement in their desks.
3. Open `/tickets`.
4. Paste the project UUID into **Workspace project** if it was not retained.
5. Use a human Contributor/Admin identity for lifecycle tests.

## 6. Screens, buttons, and files

Desk: [`tickets-desk-page.tsx`](../../../apps/web/src/components/tickets-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| Workspace project | Loads tickets for a project UUID | Implemented | `tickets-desk-page.tsx` |
| New ticket | Opens create form | Implemented | `tickets-desk-page.tsx` |
| Create ticket | Creates backlog ticket | Implemented | `tickets-desk-page.tsx` |
| Cancel | Closes create form | Implemented | `tickets-desk-page.tsx` |
| Search code or title | Applies `q` and resets offset | Implemented | `tickets-desk-page.tsx` |
| Status | Filters backlog through blocked | Implemented | `tickets-desk-page.tsx` |
| Pagination | Changes limit/offset | Implemented | `tickets-desk-page.tsx` |
| Ticket row | Selects ticket and loads checks | Implemented | `tickets-desk-page.tsx` |
| Prepare & mark Ready | Updates fields, links requirement, satisfies checks, transitions | Implemented shortcut | `tickets-desk-page.tsx` |
| assigned … done | Requests named delivery transition | Implemented | `tickets-desk-page.tsx` |
| Reopen with evidence | Adds justification evidence and reopens to `in_progress` | Implemented | `tickets-desk-page.tsx` |

The action area shows **Ready checks**, **Done checks**, status, and revision. There is no ticket detail route or history panel.

## 7. API, data, and automated tests

Prefix: `/api/v1/tickets`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/tickets/router.py)

| Method | Path | Purpose |
|---|---|---|
| POST | `/tickets` | Create |
| GET | `/tickets/projects/{project_id}` | Filtered page |
| GET/PATCH | `/tickets/{ticket_id}` | Read/update |
| POST | `/tickets/{ticket_id}/transitions` | Move status |
| POST | `/tickets/{ticket_id}/reopen` | Controlled reopen |
| POST | `/tickets/requirement-links` | Link requirement |
| POST | `/tickets/evidence` | Record evidence |
| GET/POST | readiness/done check routes | Inspect/satisfy gates |

Automated evidence:

- `tests/unit/tickets/test_tickets_domain.py`
- `tests/integration/tickets/test_tickets_api.py`
- `uv run pytest tests/unit/tickets tests/integration/tickets -q --tb=short`

## 8. Test flows

For every flow capture the UI state/toast, record id/status/version, API response, and audit/outbox row when emitted.

### F-SETUP

1. Select a project with phase and approved requirement.
2. Open `/tickets`; enter **Workspace project**.
3. **Expected UI:** ticket list or empty state.
4. **Expected data/audit:** no mutation from loading.
5. **Evidence:** project UUID and initial list screenshot.

### F-HAPPY

1. Click **New ticket**; enter unique code/title and useful delivery fields.
2. Click **Create ticket**. Expect backlog status and created toast.
3. Select it; click **Prepare & mark Ready**. Expect Ready and satisfied checks.
4. Click, in order, **assigned**, **in progress**, **code review**, **ready for qa**, **qa in progress**, **passed qa**, **done**.
5. Expect each persisted status; Done checks become satisfied before Done.
6. **Evidence:** ticket id, revisions, Ready/Done screenshots, transition audit/outbox.

### F-VALIDATE

1. Submit create with blank Code or Title. Browser required validation blocks it.
2. Use API to attempt Ready while required data/checks are missing.
3. Expect problem JSON; status remains backlog.
4. **Evidence:** validation text and response body.

### F-AUTHZ

1. Set UI role Viewer; **New ticket** must be hidden.
2. Attempt mutation with an unauthorized/backend actor.
3. Expect forbidden and no change. UI role hiding alone is not proof.

### F-TENANT

1. Read the ticket using another `X-Organization-Id`.
2. Expect not-found/forbidden, never ticket data.
3. Repeat list with the other organization and same project UUID.

### F-CONCUR

1. Note the selected revision in two tabs.
2. Transition in tab A, then submit tab B’s stale `expected_version`.
3. Expect conflict and no overwrite.

### F-TRANS

1. From backlog, directly request `done`.
2. From Ready, skip to `passed_qa`.
3. Expect invalid transition/gate error and unchanged status.

### F-GATE

1. Attempt Done before `passed_qa` or before Done checks.
2. Expect blocked completion.
3. Confirm requirement/readiness evidence exists before Ready.

### F-TERM

1. From Done, enter **Reopen reason** and click **Reopen with evidence**.
2. Expect `in_progress`, new evidence, and a human actor.
3. Agent actor, empty reason, or missing evidence must not reopen.

### F-RECOVER

1. Force an API failure while preparing Ready.
2. Expect **Could not prepare Ready** and no false success.
3. Reload and inspect partial persisted steps before retrying.

### F-CLEAN

Leave the ticket with an explicit terminal or active status and test prefix. Do not delete append-only evidence or audit history.

## 9. Security, privacy, and approvals

- Backend organization/project scope is mandatory.
- Requirement and completion gates are deterministic server rules.
- Reopen is human-only and evidence-backed.
- Do not put secrets or client PII in test descriptions/evidence.
- Human AC-901 remains blocked; this guide does not grant it.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Full ticket detail/history | Planned |
| Assignment UI in ticket actions | Planned; MOD-310 API exists |
| Config-driven action rendering | Planned; buttons are a fixed delivery sequence |
| Browser E2E automation | Planned |
| Live Temporal assignment waits | Planned |

## 11. Related journeys

- [J-WORK](../../testing/CROSS_MODULE_JOURNEYS.md#j-work-roadmap-ticket-assignment)
- [J-QA](../../testing/CROSS_MODULE_JOURNEYS.md#j-qa-test-bug-change-release)
- MOD-310 assignment and MOD-320 status engine are adjacent API capabilities.

## 12. Pass / fail checklist

- [ ] Project-scoped list loads
- [ ] Search, status, and pagination work
- [ ] Ticket creates in backlog
- [ ] Ready gate persists all prerequisites
- [ ] Delivery transitions cannot be skipped
- [ ] Done requires Passed QA and checks
- [ ] Stale revision conflicts
- [ ] Cross-tenant access does not disclose data
- [ ] Human reopen records reason and evidence
- [ ] Agent/unauthorized mutation is rejected
- [ ] Test command and result recorded
