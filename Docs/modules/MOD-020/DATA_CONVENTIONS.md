# MOD-020 Data Conventions (no physical tables for M1 identifiers)

Typed identifiers, actor context, tenant context, and domain errors are **application-layer contracts**, not database tables in this slice.

| Concept | Storage | Notes |
|---|---|---|
| OrganizationId / ClientId / ProjectId / ActorId / CorrelationId | UUID columns on business tables | Branded in Python via `NewType`; DB remains `uuid` |
| ActorKind | string / enum column or header | Values: human, agent, system, integration |
| TenantContext | derived from row `organization_id` (+ optional client/project) | Never trust client-supplied org alone once Auth0 lands |
| Domain errors | ephemeral API responses | Not persisted; audit evidence uses `gov_audit_events` / outbox |
| Unit of work | Session contract | `SqlAlchemyUnitOfWork` — no dedicated table |
| Outbox | `sys_outbox_messages` | Migration `20260810_0002`; publisher runtime deferred |
| Problem details / pagination | HTTP response contracts | Not tables |

Migrations for outbox publisher / broker workers are out of MOD-020 M1 scope.
