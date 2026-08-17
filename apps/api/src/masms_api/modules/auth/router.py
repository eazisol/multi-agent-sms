"""Auth HTTP routes (MOD-110)."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from masms_api.config import get_settings
from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.auth.schemas import (
    InvitationCreate,
    InvitationCreateResponse,
    InvitationRead,
    MfaChallengeCreate,
    MfaChallengeCreateResponse,
    MfaChallengeRead,
    MfaVerify,
    ServiceIdentityCreate,
    ServiceIdentityCreateResponse,
    ServiceIdentityRead,
    SessionCreate,
    SessionCreateResponse,
    SessionRead,
    StepUpRequest,
)
from masms_api.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> AuthService:
    return AuthService(db, ctx)


@router.get("/provider")
def auth_provider_info() -> dict[str, object]:
    settings = get_settings()
    return {
        "provider": settings.auth_provider,
        "auth0_domain_configured": bool(settings.auth0_domain),
        "auth0_audience_configured": bool(settings.auth0_audience),
        "jwks_enabled": True,
        "header_identity_enabled": settings.header_identity_enabled,
        "note": "Auth0 mode validates JWTs and requires a pre-linked MASMS human user",
    }


@router.get("/me")
def current_identity(
    ctx: RequestContext = Depends(get_request_context),
) -> dict[str, object]:
    return {
        "organization_id": ctx.organization_id,
        "actor_id": ctx.actor_id,
        "actor_kind": ctx.actor_kind.value,
        "display_name": ctx.display_name,
        "assurance_level": ctx.assurance_level,
    }


@router.post("/sessions", response_model=SessionCreateResponse, status_code=201)
def create_session(
    body: SessionCreate,
    service: AuthService = Depends(_service),
) -> SessionCreateResponse:
    session, token = service.create_session(body)
    return SessionCreateResponse(
        session=SessionRead.model_validate(session),
        access_token=token,
    )


@router.get("/sessions/me", response_model=SessionRead)
def current_session(
    service: AuthService = Depends(_service),
    ctx: RequestContext = Depends(get_request_context),
) -> SessionRead:
    session = service.get_current_session(ctx)
    return SessionRead.model_validate(session)


@router.post("/sessions/{session_id}/revoke", response_model=SessionRead)
def revoke_session(
    session_id: UUID,
    service: AuthService = Depends(_service),
) -> SessionRead:
    return SessionRead.model_validate(service.revoke_session(session_id))


@router.post("/mfa/challenges", response_model=MfaChallengeCreateResponse, status_code=201)
def start_mfa(
    body: MfaChallengeCreate,
    service: AuthService = Depends(_service),
) -> MfaChallengeCreateResponse:
    challenge, debug_code = service.start_mfa(body)
    return MfaChallengeCreateResponse(
        challenge=MfaChallengeRead.model_validate(challenge),
        debug_code=debug_code,
    )


@router.post("/mfa/verify", response_model=SessionRead)
def verify_mfa(
    body: MfaVerify,
    service: AuthService = Depends(_service),
) -> SessionRead:
    session = service.verify_mfa(challenge_id=body.challenge_id, code=body.code)
    return SessionRead.model_validate(session)


@router.post("/step-up/assert", response_model=SessionRead)
def assert_step_up(
    body: StepUpRequest,
    service: AuthService = Depends(_service),
) -> SessionRead:
    session = service.assert_step_up(
        session_id=body.session_id,
        action=body.action,
        required=body.required_assurance_level,
    )
    return SessionRead.model_validate(session)


@router.post("/invitations", response_model=InvitationCreateResponse, status_code=201)
def create_invitation(
    body: InvitationCreate,
    service: AuthService = Depends(_service),
) -> InvitationCreateResponse:
    invite, token = service.create_invitation(body)
    return InvitationCreateResponse(
        invitation=InvitationRead.model_validate(invite),
        invite_token=token,
    )


@router.post("/service-identities", response_model=ServiceIdentityCreateResponse, status_code=201)
def create_service_identity(
    body: ServiceIdentityCreate,
    service: AuthService = Depends(_service),
) -> ServiceIdentityCreateResponse:
    identity, secret = service.create_service_identity(body)
    return ServiceIdentityCreateResponse(
        identity=ServiceIdentityRead.model_validate(identity),
        client_secret=secret,
    )
