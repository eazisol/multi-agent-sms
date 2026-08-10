"""Unit tests for MOD-020 domain kernel (typed IDs, actor, tenant, errors)."""

from __future__ import annotations

from uuid import UUID

import pytest
from masms_api.kernel import (
    ActorContext,
    ActorKind,
    ForbiddenError,
    NotFoundError,
    RequestContext,
    TenantContext,
    TenantMismatchError,
)
from masms_api.kernel.ids import as_actor_id, as_organization_id, as_project_id

ORG_A = as_organization_id("00000000-0000-4000-8000-000000000001")
ORG_B = as_organization_id("00000000-0000-4000-8000-000000000002")
ACTOR = as_actor_id("00000000-0000-4000-8000-000000000101")


def test_typed_ids_are_uuid_runtime() -> None:
    assert isinstance(ORG_A, UUID)
    assert as_organization_id(str(ORG_A)) == ORG_A


def test_actor_human_may_approve() -> None:
    human = ActorContext(actor_id=ACTOR, actor_kind=ActorKind.HUMAN, display_name="alice")
    agent = ActorContext(actor_id=ACTOR, actor_kind=ActorKind.AGENT, display_name="bot")
    assert human.may_approve_human_gates is True
    assert agent.may_approve_human_gates is False
    assert agent.is_human is False


def test_tenant_same_organization() -> None:
    tenant = TenantContext(organization_id=ORG_A)
    assert tenant.same_organization(ORG_A) is True
    assert tenant.same_organization(ORG_B) is False
    assert tenant.requires_project() is False

    with_project = TenantContext(organization_id=ORG_A, project_id=as_project_id(ORG_B))
    assert with_project.requires_project() is True


def test_request_context_from_parts_preserves_compat_properties() -> None:
    ctx = RequestContext.from_parts(
        organization_id=ORG_A,
        actor_id=ACTOR,
        actor_kind=ActorKind.SYSTEM,
        correlation_id=UUID("00000000-0000-4000-8000-000000000999"),
        display_name="sys",
    )
    assert ctx.organization_id == ORG_A
    assert ctx.actor_id == ACTOR
    assert ctx.actor_kind is ActorKind.SYSTEM
    assert ctx.display_name == "sys"
    assert ctx.tenant.project_id is None


def test_domain_error_codes() -> None:
    err = NotFoundError("missing")
    assert err.code == "not_found"
    assert err.status_code == 404
    forbidden = ForbiddenError("nope")
    assert forbidden.status_code == 403
    mismatch = TenantMismatchError()
    assert mismatch.code == "tenant_mismatch"
    assert mismatch.status_code == 403


def test_invalid_uuid_parse_raises() -> None:
    with pytest.raises(ValueError):
        as_organization_id("not-a-uuid")
