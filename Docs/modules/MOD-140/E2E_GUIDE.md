# MOD-140 — Configuration Administration and Versioned Operational Rules

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Build a small workflow configuration through FastAPI `/docs`. |
| QA | Test draft-only editing, approval, activation, live checks, supersede, and rollback. |
| Developer | Verify configuration routes, lifecycle service, migration, and tests. |
| Owner / approver | Keep configuration activation governed and exact-version aware. |

## 2. What this module is

Configuration administration stores versioned operational rules outside application code: workflows, statuses, transitions, follow-up/reminder/escalation rules, and approval-workflow definitions. Drafts can be edited; only effective versions control live transition checks.

In this company it means a ticket workflow can be drafted and reviewed without affecting live tickets. After a human-approved activation, the exact version becomes effective and the prior effective version is superseded.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| Version create/approve/activate/rollback APIs | Implemented | Draft → approved → effective |
| Workflow/status/transition definition APIs | Implemented | Draft-only writes |
| Follow-up/reminder/escalation rule storage | Implemented | Definition storage |
| Approval-workflow definition storage | Implemented | Steps JSON |
| Live transition check | Implemented | Effective configuration only |
| Dedicated configuration desk | Planned | No frontend route/page |
| Temporal reminder/escalation execution | Planned | Rules are not scheduled/executed here |
| Template content catalog | Planned | Beyond approval steps deferred |
| Fine-grained approver UI/authority | Incomplete / API-dependent | Human governance still required |
| Human Done AC-901 | Blocked | Not obtained |

## 4. Requirements and dependencies

- Start API with [MOD-010](../MOD-010/E2E_GUIDE.md).
- Apply [`20260811_0008_mod140_config.py`](../../../migrations/versions/20260811_0008_mod140_config.py).
- API: [`configadmin/router.py`](../../../apps/api/src/masms_api/modules/configadmin/router.py).
- Service: [`configadmin/service.py`](../../../apps/api/src/masms_api/modules/configadmin/service.py).
- Tests: [`tests/unit/configadmin/`](../../../tests/unit/configadmin/), [`tests/integration/configadmin/test_config_api.py`](../../../tests/integration/configadmin/test_config_api.py).
- Use a human test actor and synthetic workflow codes.

## 5. How to start

1. Open `http://127.0.0.1:8000/docs`.
2. Expand the `config` operations under `/api/v1/config`.
3. Create one configuration version and copy its ID into subsequent request bodies.
4. There is no `/config` or configuration-admin product desk; all current manual testing is API-based.
5. Keep `/audit-logs` open in another tab for decision evidence where writers are wired.

## 6. Screens, buttons, and files

MOD-140 has no dedicated frontend screen, button, field, filter, empty state, pagination control, or toast.

| Surface | What exists today | Status | Source |
|---|---|---|---|
| Configuration desk | None | Planned | No page/component |
| OpenAPI **Try it out** / **Execute** | Generic FastAPI testing controls, not product UI | Implemented dev surface | [`configadmin/router.py`](../../../apps/api/src/masms_api/modules/configadmin/router.py) |
| Version request fields | Title, change reason, optional based-on version (schema-defined) | Implemented API | [`configadmin/schemas.py`](../../../apps/api/src/masms_api/modules/configadmin/schemas.py) |
| Rule request fields | Version/workflow/status/rule-specific fields | Implemented API | same file |
| Approve/activate/rollback operations | Separate API operations | Implemented | router file |
| Reminder execution controls | None | Planned | Temporal execution deferred |

Do not describe Swagger’s **Execute** button as a MASMS approval button. It merely sends the HTTP request under the supplied identity.

## 7. API, data, and automated tests

Prefix: `/api/v1/config`

| Method | Path |
|---|---|
| POST | `/versions` |
| POST | `/versions/{version_id}/approve` |
| POST | `/versions/{version_id}/activate` |
| POST | `/versions/rollback?restore_version_id=` |
| POST | `/workflows` |
| POST | `/statuses` |
| POST | `/transitions` |
| POST | `/followup-rules` |
| POST | `/reminder-rules` |
| POST | `/escalation-rules` |
| POST | `/approval-workflows` |
| POST | `/live/transitions/check` |

Current lifecycle: `draft → approved → effective`; a new effective version makes the prior one `superseded`; rollback marks the current version `rolled_back` and may restore an earlier version.

The integration test builds a ticket workflow with open/in-progress/done statuses, transition and rule definitions, proves draft live denial, forbids post-approval edits, activates, supersedes with v2, and restores v1.

```bash
uv run pytest tests/unit/configadmin tests/integration/configadmin -q --tb=short
```

[VERIFICATION.md](VERIFICATION.md) records an earlier 55-test suite but says Alembic apply was not run.

## 8. Test flows

### F-SETUP

1. Use a unique title/code suffix. Create a version with title and change reason.
2. **Expected API:** `201`, status `draft`, version number. **Data/audit:** organization, creator, timestamps, exact ID. **Evidence:** redacted JSON.
3. Create workflow, statuses, and one allowed transition bound to that version.

### F-HAPPY

1. Add follow-up, reminder, escalation, and approval-workflow definitions to the draft.
2. Check live transition while draft. **Expected:** HTTP `200`, `allowed: false`.
3. Approve version. **Expected:** `approved`.
4. Activate version. **Expected:** `effective`.
5. Repeat live check. **Expected:** configured transition allowed; unconfigured transition denied.
6. Capture version/status and matching audit evidence.

### F-VALIDATE

1. Omit required title/code/version IDs; use duplicate workflow/status code, invalid hours, malformed steps, or unknown references.
2. **Expected:** validation/conflict/not found; no partial configuration.
3. Add a workflow after approval. **Expected:** `403`; draft-only edit rule enforced.

### F-AUTHZ

1. Attempt create/approve/activate/rollback with an unauthorized or agent actor.
2. **Expected:** backend denial where authority policy is wired; agents must not finalize governed operational configuration.
3. Swagger access and a successful schema submission do not prove permission enforcement. Record any missing authority enforcement as a gap.

### F-TENANT

1. Create version/workflow in organization A; reference/check/approve from B.
2. **Expected:** not found/forbidden, never A data or a cross-tenant live rule.
3. Live checks must select only B’s effective version.

### F-CONCUR

1. Approve or activate the same version concurrently; create two candidate versions from one base.
2. **Expected:** one deterministic effective version and no two active configurations for the same scope.
3. Router bodies expose no `expected_version`; record lack of optimistic version parameter and rely on transactional uniqueness/domain checks.

### F-TRANS

1. Try activate draft before approve. **Expected:** invalid transition.
2. Try edit after approve/effective. **Expected:** forbidden.
3. Activate v2. **Expected:** v2 effective, v1 superseded.
4. Try an unsupported state jump/repeated transition. **Expected:** rejected or deterministic idempotence, never silent lifecycle corruption.

### F-GATE

1. Submit exact draft version for human review.
2. Approve and activate as separate actions. **Expected:** decisions bind the submitted version; material edits require a new draft/version.
3. An agent may draft/recommend but must not provide final approval for major operational rules.

### F-TERM

1. `rolled_back` is terminal for the displaced version unless a documented restore operation selects it.
2. Effective versions are immutable; change by creating a new version.
3. Status definitions marked terminal affect consuming workflows only after their configuration is effective.

### F-RECOVER

1. Activate v2 so v1 is superseded.
2. POST rollback with `restore_version_id=v1`. **Expected:** v2 rolled back and v1 effective.
3. Check live transition. **Expected:** restored v1 behavior.
4. Reminder/escalation retries are **Planned** because Temporal execution is not implemented.

### F-CLEAN

1. Keep versions/rules as traceable synthetic evidence; do not direct-edit approved/effective rows.
2. Do not delete audit records.
3. Record which version remains effective so later tests are understandable.

## 9. Security, privacy, and approvals

- Scope definitions and live lookup to organization and applicable project/environment.
- Draft changes must not affect live behavior.
- Approval and activation must be backend-authorized, human-governed, audited, and exact-version bound.
- Rollback is high risk and requires reason/authority/evidence in production.
- Rule JSON must be schema-validated; do not treat retrieved text as executable instructions.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Versioned rule storage/lifecycle | Implemented |
| Effective-only live transition check | Implemented |
| Supersede and rollback/restore | Implemented |
| Config administration UI | Planned |
| Temporal reminder/escalation execution | Planned |
| Rich template catalog | Planned |
| Browser E2E automation | Not present |
| Production approval authority setup | Requires human configuration |

## 11. Related journeys

- Configured transitions and rules underpin the workflows in [CROSS_MODULE_JOURNEYS.md](../../testing/CROSS_MODULE_JOURNEYS.md).
- Follow the exact-version and human-only rules in [TESTING_CONVENTIONS.md](../../testing/TESTING_CONVENTIONS.md).

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Confirmed no dedicated frontend desk exists | |
| Draft version and rule definitions created | |
| Draft does not control live transition | |
| Draft-only editing enforced | |
| Invalid lifecycle jump rejected | |
| Human authorization/agent denial checked or gap recorded | |
| Approved version activates as effective | |
| Unconfigured live transition remains denied | |
| New activation supersedes prior effective version | |
| Rollback restores prior behavior | |
| Cross-organization configuration does not leak | |
| Temporal execution remains labeled Planned | |
| Focused automated test result recorded | |
