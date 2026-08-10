"""Typed application settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MASMS_", env_file=".env", extra="ignore")

    env: str = "local"
    api_title: str = "MASMS API"
    api_version: str = "0.1.0"
    database_url: str = "sqlite+pysqlite:///:memory:"
    cors_origins: str = "http://localhost:3000"
    default_organization_id: str = "00000000-0000-4000-8000-000000000001"

    @property
    def cors_origin_list(self) -> list[str]:
        return [part.strip() for part in self.cors_origins.split(",") if part.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
