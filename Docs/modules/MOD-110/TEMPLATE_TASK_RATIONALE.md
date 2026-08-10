# MOD-110 Template Task Rationale

## FE-* marked n/a

Auth administration and invitation UI are deferred to a later UX pass (same approach as MOD-100). Backend sessions, MFA, invitations, and service identities are available via `/api/v1/auth`.

## WF-* notes

No Temporal / LangGraph auth workflows in M1. Session expiry is row-based (`expires_at`); reminder/escalation for invitations can attach later.

## Auth0 vs Cognito

Provisional IdP remains Auth0 (PRE still pending). Scaffold stores domain/audience settings and fail-closes JWKS validation. Cognito remains an AWS-aligned alternate pending architecture approval — do not treat either as production-ready from this module alone.
