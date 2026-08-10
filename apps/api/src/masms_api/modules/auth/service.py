"""Auth application service (sessions, MFA, invitations, service identities)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from masms_api.config import get_settings
from masms_api.errors import ForbiddenError, NotFoundError, ValidationAppError
from masms_api.kernel.actor import ActorKind
from masms_api.kernel.context import RequestContext
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.auth import domain
from masms_api.modules.auth.models import (
    AuthSession,
    ClientInvitation,
    MfaChallenge,
    ServiceIdentity,
)
from masms_api.modules.auth.provider import ValidatedIdentity
from masms_api.modules.auth.schemas import (
    InvitationCreate,
    MfaChallengeCreate,
    ServiceIdentityCreate,
    SessionCreate,
)
from masms_api.modules.auth.tokens import generate_opaque_token, hash_secret
from masms_api.observability.writer import ObservabilityWriter


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def resolve_session_token(db: Session, token: str) -> ValidatedIdentity:
    """Lookup an active local session by opaque bearer token."""
    token_hash = hash_secret(token)
    session = db.scalar(
        select(AuthSession).where(
            AuthSession.token_hash == token_hash,
            AuthSession.status == "active",
        )
    )
    if session is None:
        raise ForbiddenError("Invalid or revoked access token")
    if _as_utc(session.expires_at) <= datetime.now(UTC):
        session.status = "expired"
        db.add(session)
        db.commit()
        raise ForbiddenError("Access token expired")
    return ValidatedIdentity(
        organization_id=session.organization_id,
        actor_id=session.actor_id,
        actor_kind=ActorKind(session.actor_kind),
        display_name=session.display_name,
        idp_subject=session.idp_subject,
        assurance_level=session.assurance_level,
        session_id=session.id,
    )


class AuthService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)

    def create_session(self, data: SessionCreate) -> tuple[AuthSession, str]:
        raw = generate_opaque_token(prefix="sess")
        session = AuthSession(
            id=uuid4(),
            organization_id=data.organization_id,
            actor_id=data.actor_id,
            actor_kind=data.actor_kind,
            display_name=data.display_name,
            token_hash=hash_secret(raw),
            status="active",
            assurance_level=data.assurance_level,
            idp_subject=data.idp_subject,
            correlation_id=self.ctx.correlation_id,
            expires_at=datetime.now(UTC) + timedelta(minutes=data.ttl_minutes),
        )
        self.uow.add(session)
        self.uow.flush()
        self.obs.write_audit(
            action="session_create",
            entity_type="auth_session",
            entity_id=session.id,
            payload={"assurance_level": session.assurance_level},
        )
        self.uow.commit()
        self.uow.refresh(session)
        return session, raw

    def get_current_session(self, ctx: RequestContext) -> AuthSession:
        if ctx.session_id is None:
            raise ForbiddenError("No authenticated session on this request")
        return self._get_session(ctx.session_id)

    def revoke_session(self, session_id: UUID) -> AuthSession:
        domain.require_assurance(
            self.ctx.assurance_level,
            domain.ASSURANCE_MFA,
            action="session_revoke",
        )
        session = self._get_session(session_id)
        domain.assert_session_active(session.status)
        session.status = "revoked"
        session.revoked_at = datetime.now(UTC)
        self.uow.add(session)
        self.obs.write_audit(
            action="session_revoke",
            entity_type="auth_session",
            entity_id=session.id,
        )
        self.uow.commit()
        self.uow.refresh(session)
        return session

    def start_mfa(self, data: MfaChallengeCreate) -> tuple[MfaChallenge, str | None]:
        session = self._get_session(data.session_id)
        domain.assert_session_active(session.status)
        code = f"{uuid4().int % 1000000:06d}"
        challenge = MfaChallenge(
            id=uuid4(),
            organization_id=session.organization_id,
            session_id=session.id,
            method=data.method,
            status="pending",
            purpose=data.purpose,
            challenge_code_hash=hash_secret(code),
            expires_at=datetime.now(UTC) + timedelta(minutes=10),
        )
        self.uow.add(challenge)
        self.uow.commit()
        self.uow.refresh(challenge)
        env = get_settings().environment.value
        debug = code if env in {"local", "test", "development"} else None
        return challenge, debug

    def verify_mfa(self, *, challenge_id: UUID, code: str) -> AuthSession:
        challenge = self.db.scalar(select(MfaChallenge).where(MfaChallenge.id == challenge_id))
        if challenge is None:
            raise NotFoundError("MFA challenge not found")
        if challenge.status != "pending":
            raise ValidationAppError("MFA challenge is not pending")
        if _as_utc(challenge.expires_at) <= datetime.now(UTC):
            challenge.status = "expired"
            self.uow.add(challenge)
            self.uow.commit()
            raise ForbiddenError("MFA challenge expired")
        if hash_secret(code) != challenge.challenge_code_hash:
            raise ForbiddenError("Invalid MFA code")
        challenge.status = "verified"
        challenge.verified_at = datetime.now(UTC)
        session = self._get_session(challenge.session_id)
        if challenge.purpose == "step_up":
            session.assurance_level = max(session.assurance_level, domain.ASSURANCE_STEP_UP)
        else:
            session.assurance_level = max(session.assurance_level, domain.ASSURANCE_MFA)
        self.uow.add(challenge)
        self.uow.add(session)
        self.obs.write_audit(
            action="mfa_verify",
            entity_type="auth_session",
            entity_id=session.id,
            payload={"purpose": challenge.purpose, "assurance_level": session.assurance_level},
        )
        self.uow.commit()
        self.uow.refresh(session)
        return session

    def assert_step_up(self, *, session_id: UUID, action: str, required: int) -> AuthSession:
        session = self._get_session(session_id)
        domain.assert_session_active(session.status)
        domain.require_assurance(session.assurance_level, required, action=action)
        return session

    def create_invitation(self, data: InvitationCreate) -> tuple[ClientInvitation, str]:
        email = data.email.lower()
        existing = self.db.scalar(
            select(ClientInvitation).where(
                ClientInvitation.organization_id == self.ctx.organization_id,
                ClientInvitation.email == email,
                ClientInvitation.status == "pending",
            )
        )
        if existing is not None:
            raise ValidationAppError("A pending invitation already exists for this email")
        raw = generate_opaque_token(prefix="invite")
        invite = ClientInvitation(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            email=email,
            invited_role_code=data.invited_role_code,
            status="pending",
            token_hash=hash_secret(raw),
            invited_by_actor_id=self.ctx.actor_id,
            expires_at=datetime.now(UTC) + timedelta(hours=data.ttl_hours),
        )
        self.uow.add(invite)
        self.obs.write_audit(
            action="invitation_create",
            entity_type="client_invitation",
            entity_id=invite.id,
            payload={"email": invite.email, "role": invite.invited_role_code},
        )
        self.uow.commit()
        self.uow.refresh(invite)
        return invite, raw

    def create_service_identity(
        self, data: ServiceIdentityCreate
    ) -> tuple[ServiceIdentity, str]:
        actor_id = uuid4()
        client_id = f"svc_{data.service_key}_{uuid4().hex[:8]}"
        client_secret = generate_opaque_token(prefix="svcsec")
        identity = ServiceIdentity(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            actor_id=actor_id,
            service_key=data.service_key,
            display_name=data.display_name,
            status="active",
            client_id=client_id,
            client_secret_hash=hash_secret(client_secret),
            description=data.description,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(identity)
        self.obs.write_audit(
            action="service_identity_create",
            entity_type="service_identity",
            entity_id=identity.id,
            payload={"service_key": data.service_key, "client_id": client_id},
        )
        self.uow.commit()
        self.uow.refresh(identity)
        return identity, client_secret

    def _get_session(self, session_id: UUID) -> AuthSession:
        session = self.db.scalar(select(AuthSession).where(AuthSession.id == session_id))
        if session is None:
            raise NotFoundError("Session not found")
        if (
            session.organization_id != self.ctx.organization_id
            and self.ctx.actor_kind != ActorKind.SYSTEM
        ):
            raise ForbiddenError("Session outside organization scope")
        return session
