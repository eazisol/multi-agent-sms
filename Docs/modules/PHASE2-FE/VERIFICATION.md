# Phase 2 Frontend Batch

**Date:** 2026-08-11  
**Scope:** Shared shell + Clients, Queries, Projects/SRS, Documents, Roadmap desks  
**Deferred:** MOD-220 Comms, MOD-230 Requirements gathering desks

## Routes

| Path | Module |
|---|---|
| `/clients` | MOD-200 |
| `/queries` | MOD-210 |
| `/projects` | MOD-240 |
| `/documents` | MOD-250 |
| `/roadmap` | MOD-260 |
| `/governance/baselines` | MOD-000 (existing) |

## Verification

| Check | Result |
|---|---|
| `npm --prefix apps/web run lint` | **passed** |
| `npm --prefix apps/web run build` | **passed** |

## Limits

- Auth remains header-stub session (org/actor ids from env defaults)
- Queries/Projects/Documents list APIs are CRUD-lite — desks use localStorage workspace ids
- Accessibility/responsiveness covered at desk-form level; full a11y audit deferred
