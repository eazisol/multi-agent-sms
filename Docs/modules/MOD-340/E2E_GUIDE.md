# MOD-340 — Follow-Ups, Reminders, and Escalations

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Open and close a traceable follow-up. |
| QA | Test due dates, overdue processing, evidence, and parent-child gates. |
| Developer | Verify API, reminders, escalation, and SLA behavior. |
| Owner | Confirm unanswered work remains owned and visible. |

## 2. What this module is

Follow-ups track a required response between people or teams, with owner, recipient, deadline, reminder/escalation rules, and closure evidence.

In this company it means a client clarification cannot disappear in chat: it remains open, owned, due, and escalated until evidence satisfies the closure condition.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/follow-ups` desk | **Implemented** | Create, filter, search, paginate, evidence, close, overdue |
| Query-linked creation | **Implemented** | Selects inquiry; project fallback |
| Reminder/escalation lists | **Implemented** | Detail cards |
| Parent-child and SLA pause | **Implemented API** | No desk controls |
| Process overdue | **Implemented** | Manual button/API execution |
| Scheduled Temporal waits | **Planned** | No live scheduler |
| Notification delivery | **Planned** | MOD-440 |
| Business calendar | **Stubbed** | Weekday-skip heuristic |
| Human Done approval | **Blocked** | AC-901 not obtained |

## 4. Requirements and dependencies

- Requires a query or workspace project source.
- Requires owner, recipient, required response, closure condition, due rule, and rule version.
- Closure requires evidence.
- Mandatory open child follow-ups block parent closure.
- Delivery of reminders is separate from reminder/escalation record creation.

## 5. How to start

1. Start API/web.
2. Create/select a query; optionally select a project.
3. Open `/follow-ups`.
4. Use a Contributor/Admin human role.
5. For overdue testing, prepare an already-due record through approved test fixtures/API.

## 6. Screens, buttons, and files

Desk: [`follow-ups-desk-page.tsx`](../../../apps/web/src/components/follow-ups-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| New follow-up | Opens form | Implemented | `follow-ups-desk-page.tsx` |
| Linked inquiry | Selects query source; project fallback | Implemented | `follow-ups-desk-page.tsx` |
| Open follow-up | Creates with session actor owner/recipient | Implemented | `follow-ups-desk-page.tsx` |
| Open/Closed/All | Filters status | Implemented | `follow-ups-desk-page.tsx` |
| Search title | Applies query | Implemented | `follow-ups-desk-page.tsx` |
| Pagination | Changes limit/offset | Implemented | `follow-ups-desk-page.tsx` |
| Add evidence | Records closure evidence | Implemented | `follow-ups-desk-page.tsx` |
| Close follow-up | Closes if gates pass | Implemented | `follow-ups-desk-page.tsx` |
| Process overdue | Creates due reminder/escalation rows | Implemented | `follow-ups-desk-page.tsx` |
| Reminders/Escalations | Lists event rows | Implemented | `follow-ups-desk-page.tsx` |
| Pause/resume SLA | No controls | Implemented API only | `router.py` |

## 7. API, data, and automated tests

Router: [`router.py`](../../../apps/api/src/masms_api/modules/followups/router.py)  
Prefix: `/api/v1/follow-ups`

| Method | Path | Purpose |
|---|---|---|
| POST/GET | `/follow-ups` | Create/list |
| GET | `/follow-ups/{id}` | Read |
| POST/GET | `/{id}/children` | Link/list children |
| GET | `/{id}/reminders`, `/{id}/escalations` | Event lists |
| GET | `/{id}/deadline` | Business deadline |
| POST | `/{id}/sla-pauses`, `/{id}/sla-pauses/resume` | Pause/resume |
| POST | `/{id}/closure-evidence` | Evidence |
| POST | `/{id}/close` | Close |
| POST | `/{id}/process-overdue` | Create due events |

Tests:

- `tests/unit/followups/test_followups_domain.py`
- `tests/integration/followups/test_followups_api.py`
- `uv run pytest tests/unit/followups tests/integration/followups -q --tb=short`

## 8. Test flows

Capture source/query, follow-up ID, due time, owner/recipient, evidence, reminder/escalation counts, audit, and outbox.

### F-SETUP

1. Select a query and open `/follow-ups`.
2. Click **New follow-up**.
3. Confirm **Linked inquiry** contains the selected query.
4. **Expected:** required response/closure defaults and due offset are visible.

### F-HAPPY

1. Enter Title, Required response, Closure condition, and Due offset.
2. Click **Open follow-up**; expect “Follow-up opened” and Open status.
3. Select it; enter **Closure evidence** and optional note.
4. Click **Add evidence**; expect evidence toast.
5. Click **Close follow-up**; expect Closed.
6. Filter **Closed** and confirm it remains listed.

### F-VALIDATE

1. Submit blank Title/Required response/Closure condition.
2. Expect browser required validation.
3. API-create without effective/provided rule version; expect rejection.
4. Close without evidence; expect blocked.

### F-AUTHZ

1. Viewer must not see **New follow-up**.
2. Attempt close as an unauthorized actor.
3. Expect disabled control or backend forbidden and unchanged Open status.

### F-TENANT

1. Read/list known follow-up under another organization.
2. Expect not-found/forbidden.
3. Reminder/escalation/evidence endpoints must not leak.

### F-CONCUR

N/A in the current public follow-up contract: no `expected_version` is exposed for close/process operations. Record duplicate-event behavior and rely on service tests for consistency.

### F-TRANS

1. Close an already Closed follow-up or add an invalid child relation.
2. Expect invalid state/conflict.
3. Existing evidence/history must remain.

### F-GATE

1. Link an open mandatory child through OpenAPI.
2. Attempt parent **Close follow-up**.
3. Expect blocked until child closes.
4. Close child with evidence; retry parent.

### F-TERM

1. Confirm Closed appears only under Closed/All.
2. No reopen control/API exists in this module.
3. Reopen is **Planned/non-testable**; do not modify terminal rows directly.

### F-RECOVER

1. Select an overdue Open item and click **Process overdue**.
2. Expect toast counts and refreshed Reminders/Escalations.
3. Retry; verify thresholds/idempotency do not create improper duplicates.
4. Do not claim notification delivery or Temporal scheduling.

### F-CLEAN

Close test records where evidence is valid. Leave deliberately overdue records clearly named and preserve event/audit history.

## 9. Security, privacy, and approvals

- Tenant/project/source scope applies to every list and child record.
- Required responses and evidence may contain client data; use sanitized values.
- Owner, responsible party, next action, and due/review date must remain explicit.
- Manual overdue processing does not prove email/SNS delivery.
- Parent closure cannot bypass mandatory children.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Temporal scheduled reminders | Planned |
| Notification delivery | Planned |
| Full business calendar matrix | Stubbed weekday heuristic |
| Parent-child/SLA desk controls | API only |
| Reopen flow | Planned |

## 11. Related journeys

- Queries can create linked clarification follow-ups.
- `/my-work` shows open follow-ups owned/received by the actor.
- MOD-350 will coordinate durable waits; MOD-440 will deliver notifications.

## 12. Pass / fail checklist

- [ ] Query-linked follow-up opens
- [ ] Required fields are enforced
- [ ] Search/status/pagination work
- [ ] Close without evidence is blocked
- [ ] Evidence-backed close succeeds
- [ ] Mandatory child blocks parent
- [ ] Overdue processing creates correct rows
- [ ] No live delivery/scheduler claim made
- [ ] Cross-tenant records are hidden
- [ ] Closed record remains auditable
- [ ] Automated result recorded
