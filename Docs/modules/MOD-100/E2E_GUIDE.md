# MOD-100 — Organizations, Actors, Human Users, Agents, Teams, and Departments

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create a human user and team from `/users`. |
| QA | Test real forms, pagination, tenant scope, validation, and agent supervision. |
| Developer | Verify identity routes, actor separation, migration, and tests. |
| Owner | Confirm operational agents always have an active human supervisor. |

## 2. What this module is

Identity defines organizations and the people, agents, roles, departments, and teams that act inside them. Human users and agents each receive a distinct common actor identity so ownership and audit attribution can use one model without pretending an agent is a person.

In this company it means “Alice” can supervise “BD Agent,” both have different actor IDs, and a team can group actors for work without weakening human accountability.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/users` human/team desk | Implemented | README’s “FE deferred” is stale relative to current TSX |
| Human and team create/list | Implemented | Toasts and user pagination |
| Organization, actor, agent, role, department APIs | Implemented | `/api/v1/identity` |
| Team-member/reporting-line APIs | Implemented | API only |
| Active agent supervisor rule | Implemented | Requires active human supervisor |
| Auth0 user linking | Planned | MOD-110 |
| Full permission matrix | Planned | MOD-120 |
| Agent create UI | Planned / absent | API only |
| Human Done AC-901 | Blocked | Not obtained |

## 4. Requirements and dependencies

- Complete [MOD-010](../MOD-010/E2E_GUIDE.md); apply migration [`20260810_0004_mod100_identity.py`](../../../migrations/versions/20260810_0004_mod100_identity.py).
- UI: [`users/page.tsx`](../../../apps/web/src/app/users/page.tsx), [`users-desk-page.tsx`](../../../apps/web/src/components/users-desk-page.tsx).
- API: [`identity/router.py`](../../../apps/api/src/masms_api/modules/identity/router.py).
- Tests: [`tests/unit/identity/`](../../../tests/unit/identity/), [`tests/integration/identity/test_identity_api.py`](../../../tests/integration/identity/test_identity_api.py).
- Use synthetic names/emails.

## 5. How to start

1. Start API/web and open `http://localhost:3000/users`.
2. Keep the default organization and human actor for the UI happy path.
3. Use `/docs` for organization, agent, department, membership, and reporting-line routes.
4. Open `/audit-logs` after writes when audit evidence is expected.

## 6. Screens, buttons, and files

### Users & Teams — `/users`

| Control / state | What happens | Status | Source |
|---|---|---|---|
| **New user or team** | Toggles both create cards | Implemented | [`users-desk-page.tsx`](../../../apps/web/src/components/users-desk-page.tsx) |
| Full name | Required human name | Implemented | same file |
| Email | Required browser email field | Implemented | same file |
| Primary role code | Optional free text | Implemented | same file |
| **Create user** | POSTs human; success toast “User created”; clears fields | Implemented | same file |
| Code | Required team code | Implemented | same file |
| Name | Required team name | Implemented | same file |
| **Create team** | POSTs team; success toast “Team created”; clears fields | Implemented | same file |
| Users list | Full name, email, status badge | Implemented | same file |
| Teams list | Name, code, status badge | Implemented | same file |
| User pagination | Offset/limit; default 20 | Implemented | [`list-pagination.tsx`](../../../apps/web/src/components/list-pagination.tsx) |
| Team pagination | Not present; UI loads first 50 | N/A | Do not invent controls |
| “No users” / “No teams” | Empty states with create guidance | Implemented | desk file |
| Loading | Skeletons in both cards | Implemented | desk file |
| Load/create error | Toasts: unable/could not create | Implemented | desk + [`toast.ts`](../../../apps/web/src/lib/toast.ts) |
| Search, filters, edit, delete, detail links | Not present | N/A | Current list is read/create only |

## 7. API, data, and automated tests

Prefix: `/api/v1/identity`

| Method | Path |
|---|---|
| POST/GET | `/organizations` |
| POST/GET | `/humans` |
| POST/GET | `/agents` |
| GET | `/actors` |
| POST/GET | `/roles` |
| POST | `/departments` |
| POST/GET | `/teams` |
| POST | `/team-members` |
| POST | `/reporting-lines` |

The integration test creates organization → human supervisor → agent → role → department → team → membership → reporting line, then checks actor/role/team lists. It proves human and agent actor IDs differ. Run:

```bash
uv run pytest tests/unit/identity tests/integration/identity -q --tb=short
```

[VERIFICATION.md](VERIFICATION.md) records an earlier 37-test suite and migration apply; it also says FE deferred, which no longer matches the inspected current desk.

## 8. Test flows

### F-SETUP

1. Open `/users`. **Expected UI:** heading, toggle button, user/team cards; skeleton then rows or empty states. **Data:** active organization only. **Evidence:** screenshot.
2. Choose unique codes/emails, for example `qa.mod100.<timestamp>@example.test`.

### F-HAPPY

1. Click **New user or team**. Fill Full name, Email, optional Primary role code; click **Create user**.
2. **Expected UI:** “User created,” cleared fields, user listed with status. **Data/audit:** human row plus distinct actor row.
3. Fill team Code and Name; click **Create team**.
4. **Expected UI:** “Team created,” cleared fields, team listed.
5. In `/docs`, create an agent using the human user ID as supervisor. **Expected:** `201`, a different actor ID, supervisor ID retained.

### F-VALIDATE

1. Submit missing full name/email or invalid email. **Expected UI:** browser blocks required/type violation.
2. Submit missing team code/name. **Expected:** browser blocks.
3. Use duplicate email, team code, or invalid supervisor through API. **Expected:** problem response; no duplicate/orphan record. Capture actual code.

### F-AUTHZ

1. Repeat writes with an actor lacking identity administration authority when a policy fixture exists. **Expected:** backend denial.
2. Current header Role selector is a stub and this desk does not hide create controls by role; UI visibility is not authorization proof.
3. Agent actors must not gain human approval rights by being identity records.

### F-TENANT

1. Create human/team under organization A.
2. List under organization B. **Expected:** A records absent.
3. Attempt to use A human as B agent supervisor/team member. **Expected:** not found/forbidden; never cross-link tenants.

### F-CONCUR

1. Submit the same unique team code/email from two tabs simultaneously. **Expected:** at most one success; other request conflicts/validates.
2. There is no `expected_version` UI/API on these create/list routes, so stale-update testing is **N/A**.

### F-TRANS

N/A — current router exposes create/list only, not actor/team status transition endpoints.

### F-GATE

1. Attempt to create an operational agent without a supervisor or with a non-human/inactive supervisor.
2. **Expected:** rejected. A valid active human supervisor is mandatory.
3. Supervisor linkage is accountability, not approval to let an agent finalize human-only actions.

### F-TERM

N/A — no deactivate/delete/reopen routes are exposed in the inspected router or desk.

### F-RECOVER

1. Stop API and load/create. **Expected UI:** “Unable to load users and teams” or “Could not create …” toast; lists reset.
2. Restart API and reload. **Expected:** persisted rows reappear; avoid duplicate resubmission.

### F-CLEAN

1. Keep synthetic IDs in the test log for MOD-110/120/130 setup.
2. No delete control/API is documented; do not alter audit history or directly remove records.
3. Do not use real personal email addresses.

## 9. Security, privacy, and approvals

- Backend queries and relationships must stay organization-scoped.
- Emails and names are PII; use synthetic data and minimize screenshots.
- Agent creation requires an active human supervisor.
- Common actor rows do not erase human/agent distinction.
- Auth0 linking and full RBAC are not present; header identity remains a local/test stub.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Human/team create and lists | Implemented desk |
| Organization/agent/role/department/membership/reporting APIs | Implemented API only |
| Agent supervisor enforcement | Implemented |
| Agent/admin detail/edit/deactivate UI | Planned / absent |
| Auth0 linking | Planned under MOD-110 |
| Universal permission enforcement | Planned/incremental under MOD-120 |
| Search/team pagination | Not present in current desk |

## 11. Related journeys

- [J-LEARN](../../testing/CROSS_MODULE_JOURNEYS.md#j-learn-first-hour) uses the default actor context.
- Identity records seed access and capacity scenarios in MOD-120 and MOD-130.

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Users desk loads with real controls | |
| User create fields and toast verified | |
| Team create fields and toast verified | |
| User pagination works | |
| Empty/loading/error states recorded | |
| Human receives actor identity | |
| Agent receives a different actor identity | |
| Agent without valid human supervisor is rejected | |
| Duplicate/invalid create is rejected | |
| Cross-organization records do not leak/link | |
| No nonexistent search/edit/delete controls claimed | |
| Focused automated test result recorded | |
