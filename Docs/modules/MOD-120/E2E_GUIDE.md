# MOD-120 — RBAC, Attribute-Based Access, Project Membership, and RLS

Shared rules: [Testing handbook](../../testing/README.md) · [Conventions](../../testing/TESTING_CONVENTIONS.md) · [Journeys](../../testing/CROSS_MODULE_JOURNEYS.md)

Module README: [README.md](README.md) · Verification log: [VERIFICATION.md](VERIFICATION.md)

## 1. Who this guide is for

| You | Use this guide to |
|---|---|
| First-time user | Create a role and permission, then grant the permission. |
| QA | Prove deny-before-grant, project membership, tenant scope, and UI truthfulness. |
| Developer | Inspect access routes, RLS migration, permission checks, and tests. |
| Owner / security reviewer | Confirm UI hiding is not treated as backend enforcement. |

## 2. What this module is

Access control decides what an actor may do in a tenant, project, module, document, environment, and approval context. Roles collect permissions, project membership adds scope, and PostgreSQL policies add database defense in depth.

In this company it means a “Project Manager” role can be granted `clients.read`, but a check still denies a project request when the actor is not an active member of that project.

## 3. Status honesty

| Item | Status | Notes |
|---|---|---|
| `/roles` role/permission/grant desk | Implemented | README “FE deferred” is stale |
| Permission and role-permission APIs | Implemented | Deny before grant |
| Project/module/document access APIs | Implemented | API only |
| Approval-authority and access-review APIs | Implemented | API only |
| Permission-check endpoint | Implemented | Explicit `role_id` required in M1 |
| Universal authorization middleware | Planned | Endpoint is not automatic enforcement |
| PostgreSQL RLS policies/session binding | Implemented in SQL/code | Not proven by SQLite tests |
| Actor-to-role automatic resolution | Planned | Caller passes role ID |
| Human Done AC-901 | Blocked | Not obtained |

## 4. Requirements and dependencies

- Complete [MOD-100](../MOD-100/E2E_GUIDE.md) to create roles/actors.
- Apply migration [`20260810_0006_mod120_access.py`](../../../migrations/versions/20260810_0006_mod120_access.py).
- UI: [`roles/page.tsx`](../../../apps/web/src/app/roles/page.tsx), [`roles-desk-page.tsx`](../../../apps/web/src/components/roles-desk-page.tsx).
- API: [`access/router.py`](../../../apps/api/src/masms_api/modules/access/router.py).
- Tests: [`tests/unit/access/`](../../../tests/unit/access/), [`tests/integration/access/test_access_api.py`](../../../tests/integration/access/test_access_api.py).

## 5. How to start

1. Start API/web and open `http://localhost:3000/roles`.
2. Keep a human test actor and active organization.
3. Use unique role and permission codes.
4. Use `/docs` to perform permission checks and API-only grants/reviews.
5. A real PostgreSQL session is required for meaningful RLS evidence.

## 6. Screens, buttons, and files

### Roles & Permissions — `/roles`

| Control / state | What happens | Status | Source |
|---|---|---|---|
| **Manage** | Toggles three management cards | Implemented | [`roles-desk-page.tsx`](../../../apps/web/src/components/roles-desk-page.tsx) |
| Create role: Code | Required | Implemented | same file |
| Create role: Title | Required | Implemented | same file |
| **Create role** | Success toast “Role created”; clears fields | Implemented | same file |
| Permission Code | Required; placeholder `identity.read` | Implemented | same file |
| Module key | Required; default `identity` | Implemented | same file |
| Action key | Required; default `read` | Implemented | same file |
| Permission Title | Required | Implemented | same file |
| **Create permission** | Success toast; clears code/title | Implemented | same file |
| Grant Role select | Current loaded role codes | Implemented | same file |
| Grant Permission select | Current permission codes | Implemented | same file |
| **Grant** | Disabled until both IDs; success toast | Implemented | same file |
| Roles list | Title, code, status badge | Implemented | same file |
| Permissions list | Title, code, status badge | Implemented | same file |
| Role pagination | Offset/limit, default 20 | Implemented | [`list-pagination.tsx`](../../../apps/web/src/components/list-pagination.tsx) |
| Permission pagination | Not present; API returns full list | N/A | Do not invent |
| “No roles” / “No permissions” | Empty states | Implemented | desk file |
| Loading/error toasts | Skeletons; load/create/grant error toasts | Implemented | desk + [`toast.ts`](../../../apps/web/src/lib/toast.ts) |
| Search/edit/revoke grant | Not present | N/A | Current desk is create/grant/list |

## 7. API, data, and automated tests

Prefix: `/api/v1/access`

| Method | Path |
|---|---|
| POST/GET | `/permissions` |
| POST | `/role-permissions` |
| POST | `/project-members` |
| POST | `/module-access` |
| POST | `/document-access` |
| POST | `/approval-authorities` |
| POST | `/reviews` |
| POST | `/reviews/{review_id}/complete` |
| POST | `/checks/permission` |

The check returns HTTP `200` with `allowed: false` for expected authorization denials. If `role_id` is omitted, the reason states it is required in M1. Project-scoped checks first require active membership.

```bash
uv run pytest tests/unit/access tests/integration/access -q --tb=short
```

[VERIFICATION.md](VERIFICATION.md) records an earlier 49-test SQLite run and explicitly does not prove PostgreSQL RLS.

## 8. Test flows

### F-SETUP

1. Open `/roles`, observe skeleton then lists/empty states. **Expected data:** active organization only. **Evidence:** screenshot and org ID.
2. Create or identify a synthetic role and project/actor IDs.

### F-HAPPY

1. Click **Manage**; create role `QA_PM_<suffix>`.
2. Create permission `qa.records.read` with module `qa`, action `read`, title.
3. Select both and click **Grant**. **Expected UI:** three success toasts; role/permission listed.
4. POST permission check with role ID/code. **Expected data:** `allowed: true`, reason `granted`.

### F-VALIDATE

1. Leave required fields empty. **Expected UI:** browser blocks.
2. Submit duplicate role/permission/grant. **Expected:** conflict/validation; no duplicate.
3. Permission check without `role_id`. **Expected:** `200`, `allowed: false`, M1 reason.

### F-AUTHZ

1. Check permission before grant. **Expected:** `allowed: false`.
2. Grant, then check. **Expected:** true.
3. Remember this endpoint is not universal middleware. Test each protected resource’s own backend authorization separately; visible **Manage** controls do not prove authority.

### F-TENANT

1. Create role/permission in organization A; list/check/grant in B.
2. **Expected:** no A records or cross-tenant grant.
3. Run PostgreSQL RLS test by binding tenant A/B sessions if an approved fixture exists. SQLite result must be labeled **not RLS evidence**.

### F-CONCUR

1. Submit the same role-permission grant concurrently. **Expected:** one effective grant; duplicate rejected/idempotent according to actual constraint.
2. No `expected_version` appears on create/grant routes; stale-update flow is N/A.

### F-TRANS

1. Create access review, then complete it with summary/findings. **Expected:** status `completed`.
2. Complete again or use unknown review ID. **Expected:** invalid/terminal/not found; no overwritten findings.

### F-GATE

1. Create approval authority with action, role, environment, and optional threshold through `/docs`.
2. **Expected:** authority row is stored in tenant scope.
3. This configuration does not itself approve any target. Consuming approval service must validate actor, scope, effective dates, threshold, environment, and exact version.

### F-TERM

1. Completed access review is terminal in current API.
2. Grant revocation/reopen UI and endpoints are absent; mark **Planned/N/A**, never direct-edit records.

### F-RECOVER

1. Trigger desk load failure. **Expected:** “Unable to load roles and permissions”; lists reset.
2. Restart API and reload. **Expected:** persisted roles/permissions return; grant selects repopulate.
3. If tenant session binding fails, deny access rather than disabling RLS.

### F-CLEAN

1. Retain synthetic role/permission IDs for dependent tests.
2. There is no desk delete/revoke; do not remove audit history or modify policies ad hoc.
3. Record whether tests used SQLite or PostgreSQL.

## 9. Security, privacy, and approvals

- Deny by default until an explicit applicable grant exists.
- Combine permission with organization, project membership, client/document/module scope, environment, dates, and actor kind.
- Enforce on the backend; UI controls are convenience only.
- RLS is defense in depth and must be tested on PostgreSQL, not inferred from migration presence.
- Approval authority is eligibility, not the approval decision.

## 10. Planned versus implemented

| Target | Today |
|---|---|
| Role/permission/grant desk | Implemented |
| Explicit permission check | Implemented |
| Project/module/document/authority/review APIs | Implemented API only |
| Automatic actor role loadout | Planned |
| Universal router middleware | Not implemented |
| PostgreSQL RLS policy SQL | Present; live proof pending |
| Grant revoke/edit UI | Planned / absent |
| Projects/clients foreign keys | Soft UUIDs in this slice |

## 11. Related journeys

- Every journey in [CROSS_MODULE_JOURNEYS.md](../../testing/CROSS_MODULE_JOURNEYS.md) must apply these checks at its resource boundary.
- Identity setup: [MOD-100](../MOD-100/E2E_GUIDE.md).

## 12. Pass / fail checklist

| Step | Result (pass / fail / skip / blocked) |
|---|---|
| Manage toggle and all real fields verified | |
| Role created and listed | |
| Permission created and listed | |
| Grant selects/button/toast verified | |
| Denied before grant; allowed after grant | |
| Missing role ID returns denied | |
| Project check denies without membership | |
| Cross-organization grant/list is blocked | |
| SQLite result not claimed as RLS proof | |
| Access review terminal behavior checked | |
| Approval authority not mistaken for approval | |
| Focused automated test result recorded | |
