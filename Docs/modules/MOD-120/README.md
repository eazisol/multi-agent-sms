# MOD-120 — RBAC, Attribute-Based Access, Project Membership, and RLS

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Deny-by-default authorization using permissions, role grants, project membership, module/document access, approval authorities, tenant RLS session binding, and access reviews.

## M1 delivered

| ID | Entity | Table / API |
|---|---|---|
| MP-001 | Permissions | `auth_permissions` / `/api/v1/access/permissions` |
| MP-002 | Role permissions | `org_role_permissions` |
| MP-003 | Project members | `org_project_members` (soft `project_id` UUID) |
| MP-004 | Module access | `org_module_access` |
| MP-005 | Document access | `org_document_access` |
| MP-006 | Approval authorities | `org_approval_authorities` |
| MP-007 | RLS | migration policies + `apply_tenant_rls` |
| MP-008 | Access reviews | `org_access_reviews` |

Migration: `20260810_0006`  
Check helper: `POST /api/v1/access/checks/permission`

## Acceptance notes

- AC-001: `assert_client_scope` denies mismatched client IDs when both are set  
- AC-002: project-scoped checks require active membership  
- AC-003: FE deferred; API checks are authoritative  

## Limits

- Actor→role resolution from human `primary_role_code` not auto-wired (pass `role_id` to checks)
- Projects/clients tables not yet present — soft UUIDs
- FE admin screens deferred
