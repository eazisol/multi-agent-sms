"""Typed application settings."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from masms_api.platform.environment import Environment, parse_environment
from masms_api.platform.secrets import (
    LOCAL_BACKEND,
    SecretBackend,
    create_secret_backend,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MASMS_", env_file=".env", extra="ignore")

    env: str = "local"
    api_title: str = "MASMS API"
    api_version: str = "0.1.0"
    database_url: str = "sqlite+pysqlite:///:memory:"
    cors_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "http://localhost:3001,http://127.0.0.1:3001"
    )
    default_organization_id: str = "00000000-0000-4000-8000-000000000001"
    secret_backend: str = LOCAL_BACKEND
    aws_region: str | None = None
    secrets_prefix: str = "masms"
    redis_url: str | None = None
    auth_provider: str = "local"
    auth0_domain: str | None = None
    auth0_audience: str | None = None

    @field_validator("env")
    @classmethod
    def _validate_env(cls, value: str) -> str:
        return parse_environment(value).value

    @field_validator("auth_provider")
    @classmethod
    def _validate_auth_provider(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"local", "auth0"}:
            raise ValueError("MASMS_AUTH_PROVIDER must be 'local' or 'auth0'")
        return normalized

    @property
    def environment(self) -> Environment:
        return Environment(self.env)

    @property
    def cors_origin_list(self) -> list[str]:
        return [part.strip() for part in self.cors_origins.split(",") if part.strip()]

    def secret_provider(self) -> SecretBackend:
        local_values = {
            "database_url": self.database_url,
        }
        return create_secret_backend(
            backend=self.secret_backend,
            environment=self.environment,
            aws_region=self.aws_region,
            secrets_prefix=self.secrets_prefix,
            local_values=local_values,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
