# MOD-450 — Dashboard, Reporting, Search, Project Health, and Activity Timeline

**Status:** M1 Done (human AC-901 approved 2026-08-12)
**Human Done (AC-901):** Obtained 2026-08-12

## Purpose

Provide org-scoped dashboard snapshots reconciled from live source counts, project health, saved filters, indexed search documents, activity timeline, report definitions, and in-DB export previews.

## Honesty (M1 limits)

- Snapshots are **on-demand refresh**, not streaming or scheduled warehouse loads.
- Search is **indexed documents** (`rp_search_documents`), not a full-text search engine.
- Exports are **in-DB `payload_preview`**, not S3/file download artifacts.
- No BI warehouse / OLAP layer.
- FE is a desk for search + activity + filters + exports plus dashboard snapshot wiring — not a full analytics studio.
- AC-901 obtained 2026-08-12 (human owner sign-off).

## M1 delivered

API: `/api/v1/insights`  
Migration: `20260811_0029`  
FE: `/insights` (+ Dashboard snapshot panel)

| ID | Entity |
|---|---|
| MP-001 | `rp_dashboard_snapshots` |
| MP-002 | `rp_project_health` |
| MP-003 | `rp_saved_filters` |
| MP-004 | `rp_search_documents` |
| MP-005 | `rp_activity_events` |
| MP-006 | `rp_reports` |
| MP-007 | `rp_exports` |

## Acceptance behavior (M1)

- **AC-001:** `POST /insights/dashboard/refresh` recomputes org-scoped source counts into `rp_dashboard_snapshots`; `GET /insights/dashboard` returns latest; metrics include `projects_total` and `reconciled: true`
- **AC-002:** After refresh, `computed_at` / `refreshed_at` are current; `is_fresh` is true when age &lt; 60 seconds
- **AC-003:** Search and exports are org-scoped; a different `X-Organization-Id` cannot see another org's indexed items or export payloads
