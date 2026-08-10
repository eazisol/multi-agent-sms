# ADR-0002 — Provisional language and package tooling

**Status:** Proposed (PENDING formal PRE approval)  
**Date (UTC):** 2026-08-10  
**Module:** MOD-000 / MOD-010  
**Requirements:** Cursor Rules 600–720, README Required Repository Decisions

## Context

Implementation needs pinned language versions and package managers before lockfiles and CI exist.

## Decision (provisional)

| Item | Choice |
|---|---|
| Python | 3.12 |
| Node.js | 22 LTS |
| Python packaging | uv (`pyproject.toml` + lockfile) |
| Node packaging | pnpm workspaces (when host activation succeeds) |

## Consequences

- Matches selected MOD-000 scaffold answers from the implementation session  
- pnpm activation failed on this host (`EPERM` via Corepack) — tracked in `PENDING_DECISIONS.md`  
- Changing versions later requires lockfile regeneration and CI updates  

## Rollback

Revisit via CR if engineering leads mandate different versions.
