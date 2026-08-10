"""Runtime environment matrix (MOD-030-MP-001)."""

from __future__ import annotations

from enum import StrEnum


class Environment(StrEnum):
    LOCAL = "local"
    TEST = "test"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


NON_PRODUCTION = frozenset(
    {
        Environment.LOCAL,
        Environment.TEST,
        Environment.DEVELOPMENT,
        Environment.STAGING,
    }
)


def parse_environment(value: str) -> Environment:
    normalized = value.strip().lower()
    try:
        return Environment(normalized)
    except ValueError as exc:
        allowed = ", ".join(sorted(e.value for e in Environment))
        raise ValueError(f"Unsupported MASMS_ENV '{value}'. Allowed: {allowed}") from exc


def is_production(env: Environment) -> bool:
    return env is Environment.PRODUCTION
