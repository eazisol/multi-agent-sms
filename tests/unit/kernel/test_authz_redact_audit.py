"""Unit tests for MOD-020 authz, redaction, and audit catalog."""

from __future__ import annotations

from uuid import UUID

import pytest
from masms_api.kernel import (
    STANDARD_AUDIT_ACTIONS,
    ForbiddenError,
    TenantMismatchError,
    assert_project_scope,
    assert_same_organization,
    redact_mapping,
)
from masms_api.kernel.ids import as_organization_id, as_project_id

ORG_A = as_organization_id("00000000-0000-4000-8000-000000000001")
ORG_B = as_organization_id("00000000-0000-4000-8000-000000000002")
PROJECT_A = as_project_id("00000000-0000-4000-8000-000000000011")
PROJECT_B = as_project_id("00000000-0000-4000-8000-000000000012")


def test_assert_same_organization_denies_cross_tenant() -> None:
    with pytest.raises(TenantMismatchError):
        assert_same_organization(
            active_organization_id=ORG_A,
            resource_organization_id=ORG_B,
        )
    assert_same_organization(
        active_organization_id=ORG_A,
        resource_organization_id=ORG_A,
    )


def test_assert_project_scope_denies_mismatch_and_missing_active() -> None:
    with pytest.raises(ForbiddenError):
        assert_project_scope(
            active_project_id=PROJECT_A,
            resource_project_id=PROJECT_B,
        )
    with pytest.raises(ForbiddenError):
        assert_project_scope(
            active_project_id=None,
            resource_project_id=PROJECT_A,
            require_active_project=True,
        )
    # Pre-project resource with no active project is allowed
    assert_project_scope(active_project_id=None, resource_project_id=None)
    assert_project_scope(active_project_id=PROJECT_A, resource_project_id=PROJECT_A)


def test_redact_mapping_masks_secrets_recursively() -> None:
    payload = {
        "ok": "visible",
        "api_token": "super-secret",
        "nested": {"password": "x", "name": "alice"},
        "list": [{"authorization": "Bearer abc"}, {"id": "1"}],
    }
    redacted = redact_mapping(payload)
    assert redacted["ok"] == "visible"
    assert redacted["api_token"] == "[REDACTED]"
    assert redacted["nested"]["password"] == "[REDACTED]"
    assert redacted["nested"]["name"] == "alice"
    assert redacted["list"][0]["authorization"] == "[REDACTED]"
    assert redacted["list"][1]["id"] == "1"
    # Original not mutated
    assert payload["api_token"] == "super-secret"


def test_standard_audit_actions_catalog() -> None:
    required = {
        "create",
        "read_sensitive",
        "update",
        "delete",
        "assignment",
        "transition",
        "approval",
        "rejection",
        "override",
        "export",
        "integration",
        "agent_action",
    }
    assert required.issubset(STANDARD_AUDIT_ACTIONS)
    assert isinstance(UUID("00000000-0000-4000-8000-000000000001"), UUID)
