# MOD-260 — Project Phases, Milestones, Roadmaps, Dependencies, and Baselines

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Select a project, add a phase, and complete a milestone. |
| QA | Verify milestone approval and predecessor completion gates. |
| Developer | Trace the desk’s fixed milestone shortcut to roadmap APIs. |
| Owner | Understand which baseline/dependency capabilities are API-only. |

## 2. What this module is

This module organizes a project into ordered phases and approval checkpoints. The API also supports deliverables, dependencies, requirement mappings, baselines, and forecasts.

In this company it means: add Discovery and Build phases, approve and complete the Discovery kickoff milestone, then complete phases in dependency-safe order.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/roadmap` project selector, phase/milestone lists | Implemented | Database-backed and project-scoped. |
| Add phase form | Implemented | Sequence is current phase count + 1. |
| Add milestone | Implemented shortcut | Fixed generated code, “Kickoff milestone,” current actor, today, approval required. |
| Approve/complete milestone and complete phase | Implemented | Role-gated in UI and policy-gated by API. |
| Dependencies, deliverables, requirement maps, baselines, forecasts | Implemented API only | No current desk controls. |
| Timeline/Gantt/dependency visualization | Planned | Lists only. |
| Capacity scheduling optimizer | Planned | Forecast API stores values only. |
| General approval engine | Planned | Local milestone approval. |
| Header identity | Stubbed | Not login. |
| Human M1 acceptance | Blocked | AC-901 not obtained. |

## 4. Requirements and dependencies

- MOD-240 must provide at least one project.
- Selected project uses `masms.workspace.projectId`.
- For full baseline API flow, create and approve a MOD-240 requirement.
- A milestone created by the desk always requires approval.
- Phase completion is blocked by unfinished predecessors, not unrelated sibling phases.
- No pagination exists on roadmap phase/milestone lists.

## 5. How to start

1. Start shared API/web.
2. Create/select a synthetic project in `/projects`.
3. Open `/roadmap`.
4. Use Contributor to add phases/milestones.
5. Use Baseline Approver/Admin for approve and complete actions.
6. Check the Workspace project selector before every destructive-looking status action.

## 6. Screens, buttons, and files

Screen: `/roadmap`  
Desk: [`roadmap-desk-page.tsx`](../../../apps/web/src/components/roadmap-desk-page.tsx)

| Control | What it does | Status | Source file |
|---|---|---|---|
| Workspace project | Selects project and writes workspace id. | Implemented | `roadmap-desk-page.tsx` |
| Add phase | Toggles form when a project is selected and role can create. | Implemented | `roadmap-desk-page.tsx` |
| Code | Required phase code; uppercased before POST. | Implemented | `roadmap-desk-page.tsx` |
| Title | Required phase title. | Implemented | `roadmap-desk-page.tsx` |
| Cancel | Closes phase form. | Implemented | `roadmap-desk-page.tsx` |
| Add phase submit | Creates next sequence phase. | Implemented | `roadmap-desk-page.tsx` |
| Add milestone | Creates fixed kickoff milestone for that phase. | Implemented shortcut | `roadmap-desk-page.tsx` |
| Complete phase | Completes phase if predecessor rules allow. | Implemented | `roadmap-desk-page.tsx` |
| Milestone row | Selects milestone for actions. | Implemented | `roadmap-desk-page.tsx` |
| Approve | Approves selected milestone. | Implemented | `roadmap-desk-page.tsx` |
| Complete | Completes selected milestone after approval. | Implemented | `roadmap-desk-page.tsx` |
| Phase list | Shows title, status, code and actions. | Implemented | `roadmap-desk-page.tsx` |
| Milestone list | Shows title, status, code, phase, target date. | Implemented | `roadmap-desk-page.tsx` |

The desk has no date/owner/title fields for milestones, no timeline, no dependency editor, and no baseline/forecast controls.

## 7. API, data, and automated tests

Prefix: `/api/v1/roadmap`  
Router: [`router.py`](../../../apps/api/src/masms_api/modules/roadmap/router.py)  
Migration: `20260811_0015`

| Method | Path |
|---|---|
| POST | `/phases` |
| GET | `/projects/{project_id}/phases` |
| GET | `/projects/{project_id}/milestones` |
| POST | `/phases/{phase_id}/complete` |
| POST | `/milestones` |
| POST | `/milestones/{id}/approve` |
| POST | `/milestones/{id}/complete` |
| POST | `/deliverables` |
| POST | `/phase-dependencies` |
| POST | `/requirement-maps` |
| POST | `/baselines` |
| POST | `/baselines/{id}/approve` |
| POST | `/forecasts` |

Tests: [`tests/unit/roadmap`](../../../tests/unit/roadmap), [`tests/integration/roadmap/test_roadmap_api.py`](../../../tests/integration/roadmap/test_roadmap_api.py)

```bash
uv run pytest tests/unit/roadmap tests/integration/roadmap -q --tb=short
```

## 8. Test flows

Capture project/phase/milestone ids, sequence, owner, target date, approval actor, statuses, dependency responses, and audit evidence.

### F-SETUP

1. Create/select an E2E project in MOD-240.
2. Open `/roadmap`; verify Workspace project value.
3. Role = Contributor.
4. Expected: phase/milestone lists load from that project.
5. Evidence: workspace id and GET responses.

### F-HAPPY

1. Click **Add phase**.
2. Code `DISCOVER`; Title `E2E Discovery 260`; submit.
3. Add second phase `BUILD`, `E2E Build 260`.
4. Expected: planned phases with sequences 1 and 2.
5. On Discovery click **Add milestone**.
6. Expected: selected “Kickoff milestone,” owner=current actor, target=today, requires approval.
7. Attempt **Complete** before approval; expect API denial.
8. Switch to authorized role; click **Approve**, then **Complete**.
9. Expected: milestone `completed`.
10. Click **Complete phase** for Discovery; expect `completed` if its gates allow.

### F-VALIDATE

1. Empty phase Code/Title must be browser-blocked.
2. Duplicate code for the same project should conflict.
3. API milestone without owner or target date should fail.
4. No project selected means Add phase is hidden and lists are empty.

### F-AUTHZ

1. Viewer cannot add phases/milestones.
2. Contributor sees completion/approval controls disabled under current matrix.
3. Attempt milestone/baseline approve with agent actor; expect denial where human approval is required.
4. Backend result is the evidence, not role hiding alone.

### F-TENANT

1. List phases/milestones for first project under another organization.
2. Expected: not found/forbidden or empty; no roadmap titles leak.
3. Attempt cross-project dependency/mapping ids; expect rejection.

### F-CONCUR

N/A — current roadmap mutations do not expose `expected_version` in the desk.

### F-TRANS

1. Complete approval-required milestone before approval; expect `403`.
2. Through API make Build depend on Discovery.
3. Try completing Build while Discovery is unfinished; expect `403`.
4. Complete Discovery, then Build; expect success.
5. Unrelated sibling phases need not be complete.

### F-GATE

1. Milestone approval records the approving actor before completion.
2. Roadmap baseline approval requires every approved requirement mapped to a phase.
3. Create baseline before mapping by API; approval must fail.
4. Map requirements, then have an authorized human approve exact baseline.
5. General MOD-330 approval workflow remains Planned.

### F-TERM

1. Completed milestone/phase has no reopen control.
2. Complete buttons are disabled for a completed phase.
3. Reopen must use an authorized future process; do not mutate status directly.
4. Approved baseline is immutable evidence.

### F-RECOVER

1. Fail Add milestone API; expect error toast and no phantom list item.
2. Fail refresh after successful create; reload and inspect before retrying to avoid duplicates.
3. Fail completion due to predecessor; complete predecessor, then retry.
4. No scheduling optimizer/retry workflow exists here.

### F-CLEAN

Leave labeled phases, milestones, dependencies, mappings, and baseline evidence. Do not delete approval/audit history. Keep the workspace project selected for related testing.

## 9. Security, privacy, and approvals

- Roadmap data is organization/project scoped.
- Milestone owner and target date are required accountability fields.
- Approval-required milestones cannot complete before approval.
- Baseline approval is exact-project/version evidence and must be human-governed.
- A roadmap does not itself approve a client-facing timeline commitment.
- Forecast values are records, not authoritative promises.

## 10. Planned versus implemented

| Target design | Current behavior |
|---|---|
| Timeline/Gantt/dependency graph | Two lists |
| Configurable milestone form | Fixed kickoff shortcut |
| Dependency and requirement mapping editor | API only |
| Baseline/forecast workspace | API only |
| Capacity optimizer | Stored forecast values |

## 11. Related journeys

- Project/requirements: [MOD-240](../MOD-240/E2E_GUIDE.md)
- Documents: [MOD-250](../MOD-250/E2E_GUIDE.md)
- Shared: [Cross-module journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

## 12. Pass / fail checklist

| Check | Result (pass / fail / skip / blocked) |
|---|---|
| Workspace project selector scopes lists | |
| Phase fields and sequence persist | |
| Add milestone creates documented fixed values | |
| Milestone completion before approval is blocked | |
| Authorized approval then completion succeeds | |
| Predecessor blocks successor completion | |
| Independent sibling completion rule holds | |
| Baseline mapping gate API works if tested | |
| No timeline/dependency visualization is falsely claimed | |
| Cross-project/tenant data does not leak | |
| Automated tests command and result recorded | |
