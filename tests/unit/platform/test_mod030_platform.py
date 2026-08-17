"""Unit tests for MOD-030 platform environment, secrets, and release gate."""

from __future__ import annotations

import pytest
from masms_api.config import Settings
from masms_api.platform.environment import Environment, parse_environment
from masms_api.platform.release_gate import evaluate_production_gate
from masms_api.platform.secrets import (
    LOCAL_BACKEND,
    SECRETS_MANAGER_BACKEND,
    SecretBackendError,
    create_secret_backend,
)
from pydantic import ValidationError


def test_parse_environment_matrix() -> None:
    assert parse_environment("local") is Environment.LOCAL
    assert parse_environment("STAGING") is Environment.STAGING
    with pytest.raises(ValueError):
        parse_environment("qa")


def test_settings_rejects_unknown_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MASMS_ENV", "not-real")
    with pytest.raises(ValidationError):
        Settings()


def test_provider_settings_default_to_safe_local_stubs() -> None:
    settings = Settings(_env_file=None)

    assert settings.header_identity_enabled is True
    assert settings.temporal_address is None
    assert settings.gmail_mode == "sim"
    assert settings.jira_mode == "sim"


def test_auth0_urls_are_derived_from_domain() -> None:
    settings = Settings(
        _env_file=None,
        auth_provider="auth0",
        auth0_domain="https://tenant.example.auth0.com/",
        auth0_audience="https://api.masms.local",
    )

    assert settings.header_identity_enabled is False
    assert settings.auth0_issuer == "https://tenant.example.auth0.com/"
    assert settings.auth0_jwks_url == (
        "https://tenant.example.auth0.com/.well-known/jwks.json"
    )


def test_settings_rejects_unknown_integration_mode() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, gmail_mode="production")


def test_local_secret_backend() -> None:
    backend = create_secret_backend(
        backend=LOCAL_BACKEND,
        environment=Environment.LOCAL,
        aws_region=None,
        secrets_prefix="masms",
        local_values={"database_url": "sqlite+pysqlite:///:memory:"},
    )
    assert backend.get_secret("database_url").startswith("sqlite")


def test_local_secret_backend_resolves_opaque_reference(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MASMS_SECRET_GMAIL_SANDBOX", '{"access_token":"test-only"}')
    backend = create_secret_backend(
        backend=LOCAL_BACKEND,
        environment=Environment.LOCAL,
        aws_region=None,
        secrets_prefix="masms",
        local_values={},
    )

    assert backend.get_secret("secrets/gmail_sandbox") == '{"access_token":"test-only"}'


def test_production_forbids_local_secret_backend() -> None:
    with pytest.raises(SecretBackendError):
        create_secret_backend(
            backend=LOCAL_BACKEND,
            environment=Environment.PRODUCTION,
            aws_region=None,
            secrets_prefix="masms",
            local_values={"database_url": "x"},
        )


def test_secrets_manager_backend_fails_closed_without_client() -> None:
    backend = create_secret_backend(
        backend=SECRETS_MANAGER_BACKEND,
        environment=Environment.STAGING,
        aws_region="us-east-1",
        secrets_prefix="masms/staging",
        local_values={},
    )
    with pytest.raises(SecretBackendError):
        backend.get_secret("database_url")


def test_production_gate_requires_human_fields() -> None:
    with pytest.raises(PermissionError):
        evaluate_production_gate(
            environment="production",
            confirmed=False,
            approver="owner@example.com",
            reason="Ship fix for outage",
            git_sha="abc123",
        )
    gate = evaluate_production_gate(
        environment="production",
        confirmed=True,
        approver="owner@example.com",
        reason="Ship fix for outage",
        git_sha="abc123",
    )
    assert gate.approver == "owner@example.com"
