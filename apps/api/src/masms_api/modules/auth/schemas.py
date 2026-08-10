"""Auth API schemas (MOD-110)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SessionCreate(BaseModel):
    organization_id: UUID
    actor_id: UUID
    actor_kind: str = Field(default="human", max_length=32)
    display_name: str = Field(min_length=2, max_length=255)
    idp_subject: str | None = Field(default=None, max_length=255)
    assurance_level: int = Field(default=1, ge=1, le=3)
    ttl_minutes: int = Field(default=60, ge=5, le=1440)


class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    actor_kind: str
    display_name: str
    status: str
    assurance_level: int
    expires_at: datetime
    revoked_at: datetime | None
    created_at: datetime


class SessionCreateResponse(BaseModel):
    session: SessionRead
    access_token: str


class MfaChallengeCreate(BaseModel):
    session_id: UUID
    method: str = Field(default="totp", max_length=32)
    purpose: str = Field(default="login", max_length=64)


class MfaChallengeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    session_id: UUID
    method: str
    status: str
    purpose: str
    expires_at: datetime


class MfaChallengeCreateResponse(BaseModel):
    challenge: MfaChallengeRead
    debug_code: str | None = Field(
        default=None,
        description="Returned only in local/test environments for scaffold verification",
    )


class MfaVerify(BaseModel):
    challenge_id: UUID
    code: str = Field(min_length=4, max_length=16)


class StepUpRequest(BaseModel):
    session_id: UUID
    action: str = Field(min_length=3, max_length=128)
    required_assurance_level: int = Field(default=3, ge=2, le=3)


class InvitationCreate(BaseModel):
    email: str = Field(min_length=3, max_length=320, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    invited_role_code: str = Field(default="client", max_length=64)
    ttl_hours: int = Field(default=72, ge=1, le=720)


class InvitationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    email: str
    invited_role_code: str
    status: str
    expires_at: datetime
    accepted_at: datetime | None
    created_at: datetime


class InvitationCreateResponse(BaseModel):
    invitation: InvitationRead
    invite_token: str


class ServiceIdentityCreate(BaseModel):
    service_key: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_-]+$")
    display_name: str = Field(min_length=2, max_length=255)
    description: str | None = None


class ServiceIdentityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    service_key: str
    display_name: str
    status: str
    client_id: str
    created_at: datetime
    revoked_at: datetime | None


class ServiceIdentityCreateResponse(BaseModel):
    identity: ServiceIdentityRead
    client_secret: str
