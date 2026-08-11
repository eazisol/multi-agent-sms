# MOD-260 — Project Phases, Milestones, Roadmaps, Dependencies, and Baselines

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Plan project phases and milestones, map approved requirements to phases, model dependencies, snapshot baselines, and allow independent multi-phase completion.

## M1 delivered

API: `/api/v1/roadmap`  
Migration: `20260811_0015`

| ID | Entity |
|---|---|
| MP-001 | `pm_phases` |
| MP-002 | `pm_milestones` (owner, date, status, approval) |
| MP-003 | `pm_deliverables` |
| MP-004 | `pm_phase_dependencies` |
| MP-005 | `pm_project_baselines` (+ `pm_requirement_phase_maps` for AC-001) |
| MP-006 | `pm_forecasts` |

## Limits

- FE deferred; MOD-330 approval engine deferred (local milestone approve)
- Capacity forecasts are recorded values only (no scheduling optimizer)
