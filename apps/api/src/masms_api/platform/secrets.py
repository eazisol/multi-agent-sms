"""Secret retrieval backends (MOD-030-MP-002).

Local development may read from process env / `.env`.
Non-local production must use the approved secret manager (Azure Key Vault).
Agents must never receive raw secret values in prompts or logs.
"""

from __future__ import annotations

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
        if name not in self._values or not self._values[name]:
            raise SecretBackendError(f"Secret '{name}' is not configured in local env")
        return self._values[name]


class AzureKeyVaultSecretBackend(SecretBackend):
    """Placeholder for Azure Key Vault.

    Real Key Vault SDK wiring is deferred until PRE stack approval and Key Vault
    identities are provisioned. Instantiating this without a URI fails closed.
    """

    def __init__(self, vault_uri: str | None) -> None:
        if not vault_uri:
            raise SecretBackendError(
                "MASMS_KEY_VAULT_URI is required when MASMS_SECRET_BACKEND=key_vault"
            )
        self.vault_uri = vault_uri.rstrip("/")

    def get_secret(self, name: str) -> str:
        raise SecretBackendError(
            "Azure Key Vault client is not enabled in this scaffold; "
            f"configure workload identity for vault '{self.vault_uri}' "
            f"before reading secret '{name}'"
        )


LOCAL_BACKEND: Final = "local_env"
KEY_VAULT_BACKEND: Final = "key_vault"


def create_secret_backend(
    *,
    backend: str,
    environment: Environment,
    key_vault_uri: str | None,
    local_values: dict[str, str],
) -> SecretBackend:
    name = backend.strip().lower()
    if is_production(environment) and name == LOCAL_BACKEND:
        raise SecretBackendError(
            "Production must not use local_env secret backend; set MASMS_SECRET_BACKEND=key_vault"
        )
    if name == LOCAL_BACKEND:
        return LocalEnvSecretBackend(local_values)
    if name == KEY_VAULT_BACKEND:
        return AzureKeyVaultSecretBackend(key_vault_uri)
    raise SecretBackendError(f"Unsupported MASMS_SECRET_BACKEND '{backend}'")
