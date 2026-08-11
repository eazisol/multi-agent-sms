# Phase 2–3 Frontend Desks

**Date:** 2026-08-11  
**Scope:** Shared shell + Clients, Queries, Comms, Requirements, Projects/SRS, Documents, Roadmap, Tickets

## Routes

| Path | Module |
|---|---|
| `/clients` | MOD-200 |
| `/queries` | MOD-210 |
| `/comms` | MOD-220 |
| `/requirements` | MOD-230 |
| `/projects` | MOD-240 |
| `/documents` | MOD-250 |
| `/roadmap` | MOD-260 |
| `/tickets` | MOD-300 |
| `/governance/baselines` | MOD-000 (existing) |

## Verification

| Check | Result |
|---|---|
| `npm --prefix apps/web run lint` | **passed** |
| `npm --prefix apps/web run build` | **passed** |

## Limits

- Auth remains header-stub session
- Several APIs are CRUD-lite — desks use localStorage workspace ids where list endpoints are thin
- Full a11y audit deferred; form-level labels/focus are present
