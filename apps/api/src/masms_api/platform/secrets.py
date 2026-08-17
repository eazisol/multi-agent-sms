"""Secret retrieval backends (MOD-030-MP-002).

Local development may read from process env / `.env`.
Non-local production must use the approved secret manager (AWS Secrets Manager).
Agents must never receive raw secret values in prompts or logs.
"""

from __future__ import annotations

import os
import re
from abc import ABC, abstractmethod
from typing import Final

from masms_api.platform.environment import Environment, is_production


class SecretBackendError(RuntimeError):
    pass


class SecretBackend(ABC):
    @abstractmethod
    def get_secret(self, name: str) -> str:
        """Return the secret value for ``name`` (never log the result)."""


class LocalEnvSecretBackend(SecretBackend):
    """Read secrets from already-loaded process settings / environ."""

    def __init__(self, values: dict[str, str]) -> None:
        self._values = values

    def get_secret(self, name: str) -> str:
        configured = self._values.get(name)
        if configured:
            return configured
        normalized = name.strip()
        for prefix in ("sm://", "sm:", "secrets/"):
            if normalized.startswith(prefix):
                normalized = normalized.removeprefix(prefix)
                break
        env_key = re.sub(r"[^A-Za-z0-9]+", "_", normalized).strip("_").upper()
        value = os.getenv(f"MASMS_SECRET_{env_key}") if env_key else None
        if not value:
            raise SecretBackendError(f"Secret '{name}' is not configured in local env")
        return value


class AwsSecretsManagerSecretBackend(SecretBackend):
    """Placeholder for AWS Secrets Manager.

    Real boto3/SDK wiring is deferred until PRE stack approval and IAM roles
    are provisioned. Instantiating this without a region fails closed.
    """

    def __init__(self, *, region: str | None, secret_prefix: str | None) -> None:
        if not region:
            raise SecretBackendError(
                "MASMS_AWS_REGION is required when MASMS_SECRET_BACKEND=secrets_manager"
            )
        self.region = region
        self.secret_prefix = (secret_prefix or "masms").rstrip("/")

    def get_secret(self, name: str) -> str:
        secret_id = f"{self.secret_prefix}/{name}"
        raise SecretBackendError(
            "AWS Secrets Manager client is not enabled in this scaffold; "
            f"configure an IAM role for region '{self.region}' "
            f"before reading secret '{secret_id}'"
        )


LOCAL_BACKEND: Final = "local_env"
SECRETS_MANAGER_BACKEND: Final = "secrets_manager"


def create_secret_backend(
    *,
    backend: str,
    environment: Environment,
    aws_region: str | None,
    secrets_prefix: str | None,
    local_values: dict[str, str],
) -> SecretBackend:
    name = backend.strip().lower()
    if is_production(environment) and name == LOCAL_BACKEND:
        raise SecretBackendError(
            "Production must not use local_env secret backend; "
            "set MASMS_SECRET_BACKEND=secrets_manager"
        )
    if name == LOCAL_BACKEND:
        return LocalEnvSecretBackend(local_values)
    if name == SECRETS_MANAGER_BACKEND:
        return AwsSecretsManagerSecretBackend(region=aws_region, secret_prefix=secrets_prefix)
    raise SecretBackendError(f"Unsupported MASMS_SECRET_BACKEND '{backend}'")
