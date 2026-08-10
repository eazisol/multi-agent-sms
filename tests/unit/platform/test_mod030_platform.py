"""Unit tests for MOD-030 platform environment, secrets, and release gate."""

from __future__ import annotations

import pytest
from masms_api.config import Settings
from masms_api.platform.environment import Environment, parse_environment
from masms_api.platform.release_gate import evaluate_production_gate
from masms_api.platform.secrets import (
    KEY_VAULT_BACKEND,
    LOCAL_BACKEND,
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


def test_local_secret_backend() -> None:
    backend = create_secret_backend(
        backend=LOCAL_BACKEND,
        environment=Environment.LOCAL,
        key_vault_uri=None,
        local_values={"database_url": "sqlite+pysqlite:///:memory:"},
    )
    assert backend.get_secret("database_url").startswith("sqlite")


def test_production_forbids_local_secret_backend() -> None:
    with pytest.raises(SecretBackendError):
        create_secret_backend(
            backend=LOCAL_BACKEND,
            environment=Environment.PRODUCTION,
            key_vault_uri=None,
            local_values={"database_url": "x"},
        )


def test_key_vault_backend_fails_closed_without_client() -> None:
    backend = create_secret_backend(
        backend=KEY_VAULT_BACKEND,
        environment=Environment.STAGING,
        key_vault_uri="https://example.vault.azure.net/",
        local_values={},
    )
    with pytest.raises(SecretBackendError):
        backend.get_secret("database-url")


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
