# New UI — Design System Rollout

**Date:** 2026-08-11  
**Source:** `New UI.md`  
**Scope:** Full shell redesign + restyle of all existing desks; placeholders for modules without backend

## Delivered

- Collapsible sidebar + mobile drawer matching New UI information architecture
- Global header: breadcrumbs, search/command palette (⌘K), Create, notifications, AI, theme toggle, role switcher
- Light/dark theme tokens (indigo accent, cool gray surfaces)
- Geist typography via `geist` package
- Shared primitives: Button, Card, Field, StatusBadge, EmptyState, SkeletonRows, PageHeader
- Dashboard at `/`
- Existing desks restyled (Clients, Queries, Messages, Projects, Requirements, Documents, Roadmaps, Tickets, Governance baselines)
- Placeholder routes for upcoming modules (Follow-ups, Approvals, Agents, QA, Admin, etc.)

## Verification

| Check | Result |
|---|---|
| `npm --prefix apps/web run lint` | **passed** |
| `npm --prefix apps/web run build` | **passed** (37 routes) |

## Limits

- Placeholder modules are intentional “coming next” screens (no fake CRUD)
- Dashboard attention cards use illustrative sample content until those APIs exist
- Command palette navigates modules; full entity search deferred
- Auth remains header-stub session
