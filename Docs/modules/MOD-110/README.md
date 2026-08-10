# MOD-110 — Authentication, Sessions, MFA, and Account Security

**Status:** Implementation draft (M1 API/DB complete; FE deferred)  
**Human Done (AC-901):** NOT obtained

## Purpose

Authenticate actors, manage sessions, raise assurance (MFA / step-up), invite clients, and register service identities — without treating Auth0 JWKS as production-ready until tenant config is approved.

## M1 delivered

| ID | Capability | Location |
|---|---|---|
| MP-001 | IdP contract (local + Auth0 fail-closed) | `modules/auth/provider.py` |
| MP-002 | Opaque token hashing / resolution | `tokens.py`, `resolve_session_token` |
| MP-003 | Sessions create / me / revoke | `auth_sessions`, `/api/v1/auth/sessions*` |
| MP-004 | MFA challenge + verify | `auth_mfa_challenges` |
| MP-005 | Step-up assert gate | `/api/v1/auth/step-up/assert` |
| MP-006 | Client invitations | `auth_client_invitations` |
| MP-007 | Service identities | `auth_service_identities` |

API prefix: `/api/v1/auth`  
Migration: `20260810_0005`  
Config: `MASMS_AUTH_PROVIDER` (`local` default), `MASMS_AUTH0_DOMAIN`, `MASMS_AUTH0_AUDIENCE`

## Acceptance notes

- Authenticated local sessions resolve via `Authorization: Bearer` (header stub remains for local/test)
- Session revoke requires assurance_level ≥ 2 (MFA)
- Immediate revoke invalidates subsequent bearer use
- Auth0 path remains fail-closed (no JWKS enabled)

## Limits

- Real Auth0 JWKS validation not enabled
- Cognito / AWS IdP alternate is pending PRE decision
- FE auth screens deferred (see TEMPLATE_TASK_RATIONALE)
- Invitation accept + email delivery not in this slice
