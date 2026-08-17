# MOD-130 — Skills, Availability, Capacity, Working Hours, and Business Calendars

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create a skill and record an actor allocation. |
| QA | Test eligibility, leave, calendars, holidays, SLA dates, validation, and tenant scope. |
| Developer | Verify capacity routes, migration, calculations, and tests. |
| Manager / owner | Treat results as assignment input, not unauthorized resource allocation approval. |

## 2. What this module is

Capacity records what people can do and when they are available: skills, proficiency, schedules, allocation percentage, leave, calendars, holidays, and on-call periods. It also evaluates a proposed assignment and adds business days for SLA calculations.

In this company it means the system can report that an actor has Python proficiency, 60% remaining capacity, and no blocking leave before a deadline. A human still decides material allocation outside approved authority.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/capacity` skill/allocation desk | Implemented | README “FE deferred” is stale |
| Skill and allocation create/list | Implemented | Skills paginated; allocations first 50 |
| Actor skill, availability, calendar, holiday, leave, on-call APIs | Implemented | API only |
| Assignment evaluation | Implemented | Skill/capacity/leave/calendar inputs |
| SLA business-day helper | Implemented | Skips weekends/holidays |
| Resource planning/approval workflow | Planned / outside desk | Do not auto-allocate |
| Project allocation FK | Stubbed/soft UUID | Project relation not hard FK here |
| Temporal scheduling | Planned | No worker in this module |
| Human Done AC-901 | Blocked | Not obtained |

## 4. Requirements and dependencies

- Complete [MOD-100](../MOD-100/E2E_GUIDE.md) for actor IDs.
- Apply [`20260810_0007_mod130_capacity.py`](../../../migrations/versions/20260810_0007_mod130_capacity.py).
- UI: [`capacity/page.tsx`](../../../apps/web/src/app/capacity/page.tsx), [`capacity-desk-page.tsx`](../../../apps/web/src/components/capacity-desk-page.tsx).
- API: [`capacity/router.py`](../../../apps/api/src/masms_api/modules/capacity/router.py).
- Tests: [`tests/unit/capacity/`](../../../tests/unit/capacity/), [`tests/integration/capacity/test_capacity_api.py`](../../../tests/integration/capacity/test_capacity_api.py).
- Use synthetic leave notes; notes may contain sensitive PII.

## 5. How to start

1. Start API/web and open `http://localhost:3000/capacity`.
2. The Actor id field starts with the current session actor ID and updates when that session actor changes.
3. Use `/docs` for detailed skill, schedule, calendar, leave, on-call, evaluation, and SLA scenarios.
4. Use fixed dates/calendars so expected results are reproducible.

## 6. Screens, buttons, and files

### Skills & Capacity — `/capacity`

| Control / state | What happens | Status | Source |
|---|---|---|---|
| **New skill or allocation** | Toggles two create cards | Implemented | [`capacity-desk-page.tsx`](../../../apps/web/src/components/capacity-desk-page.tsx) |
| Skill Code | Required; placeholder `python` | Implemented | same file |
| Skill Title | Required | Implemented | same file |
| Category | Optional UI text; default `general` | Implemented | same file |
| **Create skill** | Toast “Skill created”; clears code/title | Implemented | same file |
| Actor id | Required; defaults to session actor | Implemented | same file |
| Allocation % | Required free-text input; default `40` | Implemented | same file |
| Effective from | Required date; source default `2026-08-01` | Implemented | same file |
| **Create allocation** | Toast “Allocation created” | Implemented | same file |
| Skills list | Title, code, category, status | Implemented | same file |
| Allocations list | Percent, shortened actor ID, effective date, status | Implemented | same file |
| Skill pagination | Offset/limit; default 20 | Implemented | [`list-pagination.tsx`](../../../apps/web/src/components/list-pagination.tsx) |
| Allocation pagination | Not present; UI loads first 50 | N/A | Do not invent |
| “No skills” / “No allocations” | Empty states | Implemented | desk file |
| Loading/error | Skeletons and load/create error toasts | Implemented | desk + [`toast.ts`](../../../apps/web/src/lib/toast.ts) |
| Search/filter/edit/delete/evaluate buttons | Not present | N/A | Evaluation is API-only |

## 7. API, data, and automated tests

Prefix: `/api/v1/capacity`

| Method | Path |
|---|---|
| POST/GET | `/skills` |
| POST | `/actor-skills` |
| POST | `/availability` |
| POST/GET | `/allocations` |
| POST | `/calendars` |
| POST | `/holidays` |
| POST | `/leave` |
| POST | `/oncall` |
| POST | `/evaluate-assignment` |
| POST | `/sla/business-days` |

The integration test creates the complete calculation setup and proves 40% allocation leaves 60%, while one business day from Thursday 2026-08-13 with Friday holiday 2026-08-14 lands on Monday 2026-08-17 in `Asia/Karachi`.

```bash
uv run pytest tests/unit/capacity tests/integration/capacity -q --tb=short
```

[VERIFICATION.md](VERIFICATION.md) records an earlier 52-test suite; migration apply was not run in that evidence.

## 8. Test flows

### F-SETUP

1. Create/identify a synthetic human actor in MOD-100.
2. Open `/capacity`. **Expected UI:** skeleton then lists/empty states; actor ID prefilled. **Data:** active organization only. **Evidence:** screenshot.
3. Use a unique skill code and fixed calendar dates.

### F-HAPPY

1. Toggle create cards; enter Code, Title, Category; click **Create skill**. **Expected:** success toast and listed skill.
2. Enter Actor id, `40`, and date; click **Create allocation**. **Expected:** toast and allocation row showing `40%`.
3. Through `/docs`, link actor proficiency `4`, add Monday availability, calendar and holiday.
4. Evaluate minimum proficiency `3`. **Expected:** eligible and remaining capacity `60`.
5. Add one business day across the fixed Friday holiday. **Expected:** Monday due date and calendar timezone.

### F-VALIDATE

1. Empty required fields. **Expected UI:** browser blocks.
2. Submit malformed actor UUID, allocation below/above allowed bounds, invalid date range, weekday/time, proficiency, or negative business days. **Expected:** validation/problem response; no row.
3. Duplicate skill code/calendar holiday. Record actual conflict behavior.

### F-AUTHZ

1. Attempt create/evaluate using an actor without capacity authority. **Expected:** backend denial when policy is wired.
2. Current desk does not hide controls by role; header Role is a stub. Do not accept UI visibility as authorization.
3. Assignment evaluation is advice/data, not authorization to allocate resources.

### F-TENANT

1. Create skill/allocation/calendar in organization A; list/evaluate from B.
2. **Expected:** no A rows, no cross-tenant actor/calendar/skill use.
3. A soft project UUID must still be organization/project scoped by service checks.

### F-CONCUR

1. Submit two allocations for the same actor/effective period concurrently. **Expected:** deterministic constraints/calculation; no silent over-allocation.
2. No `expected_version` field exists on current routes, so classic stale-version conflict is N/A. Record duplicate behavior as a gap if both are accepted unexpectedly.

### F-TRANS

N/A — inspected routes create/list/evaluate; no status transition endpoint is exposed.

### F-GATE

1. Evaluate an actor that appears eligible. **Expected:** response is a recommendation result only.
2. Do not finalize resource allocation outside approved authority. Required human approval remains external to this API slice.

### F-TERM

N/A — no close/cancel/reopen endpoints are exposed for skills, allocations, leave, or on-call records.

### F-RECOVER

1. Trigger desk load failure. **Expected:** “Unable to load skills and capacity” toast and cleared lists.
2. Restart API and reload; persisted rows return.
3. Correct missing skill/calendar data and rerun evaluation. **Expected:** a new deterministic result; no background retry worker is involved.

### F-CLEAN

1. Keep synthetic catalog/calendar IDs for dependent tests.
2. Do not enter real health/leave details; leave notes are sensitive.
3. No delete controls/routes are documented; avoid direct SQL cleanup and preserve audit evidence.

## 9. Security, privacy, and approvals

- Scope all actors, skills, allocations, leave, and calendars to organization/project.
- Treat leave type/notes and schedules as sensitive workforce data.
- Audit leave by entity ID and safe metadata, not note content.
- Evaluation must not bypass authorization, approved capacity, or human allocation authority.
- Timezone/date evidence should be explicit to avoid hidden locale assumptions.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Skill/allocation create and list desk | Implemented |
| Detailed workforce/calendar data | Implemented API only |
| Assignment evaluation and business-day math | Implemented |
| Allocation list pagination UI | Absent (first 50) |
| Edit/close/delete workflows | Planned / absent |
| Hard project foreign key | Soft UUID in this slice |
| Automated scheduling/Temporal execution | Planned |
| Resource approval workflow | Must be handled by governed downstream process |

## 11. Related journeys

- Capacity informs assignment and delivery journeys in [CROSS_MODULE_JOURNEYS.md](../../testing/CROSS_MODULE_JOURNEYS.md).
- Actor setup comes from [MOD-100](../MOD-100/E2E_GUIDE.md); permissions from [MOD-120](../MOD-120/E2E_GUIDE.md).

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Real create toggle/fields verified | |
| Skill created, toasted, and listed | |
| Allocation created, toasted, and listed | |
| Skill pagination works | |
| Allocation list correctly noted as first 50/no controls | |
| Invalid percentage/date/UUID rejected | |
| Skill/proficiency/availability evaluation checked | |
| Remaining capacity calculation checked | |
| Weekend/holiday/timezone SLA date checked | |
| Cross-organization data does not leak | |
| Evaluation not mistaken for allocation approval | |
| Focused automated test result recorded | |
