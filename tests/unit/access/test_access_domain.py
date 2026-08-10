"""Unit tests for MOD-120 access domain."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from masms_api.errors import ForbiddenError, ValidationAppError
from masms_api.modules.access import domain


def test_permission_deny_by_default() -> None:
    with pytest.raises(ForbiddenError):
        domain.require_permission_granted(granted=False, permission_code="clients.read")
    domain.require_permission_granted(granted=True, permission_code="clients.read")


def test_project_membership_required() -> None:
    with pytest.raises(ForbiddenError):
        domain.require_project_membership(has_membership=False, project_id=uuid4())


def test_effective_window() -> None:
    now = datetime.now(UTC)
    domain.assert_effective_window(
        effective_from=now - timedelta(days=1),
        effective_to=now + timedelta(days=1),
        now=now,
    )
    with pytest.raises(ForbiddenError):
        domain.assert_effective_window(
            effective_from=now + timedelta(days=1),
            effective_to=None,
            now=now,
        )


def test_authority_and_document_principals() -> None:
    with pytest.raises(ValidationAppError):
        domain.assert_authority_subject(actor_id=None, role_code=None)
    with pytest.raises(ValidationAppError):
        domain.assert_document_principal(actor_id=None, role_code=None)
    domain.assert_authority_subject(actor_id=uuid4(), role_code=None)
    domain.assert_document_principal(actor_id=None, role_code="PM")
