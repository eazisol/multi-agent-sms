"""Operational health checks (MOD-040-MP-007)."""

from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


def check_database(session: Session) -> dict[str, Any]:
    try:
        session.execute(text("SELECT 1"))
        return {"status": "up"}
    except Exception as exc:  # noqa: BLE001 - readiness must return safe status
        return {"status": "down", "error": exc.__class__.__name__}


def check_redis(redis_url: str | None) -> dict[str, Any]:
    if not redis_url:
        return {"status": "skipped", "reason": "MASMS_REDIS_URL not configured"}
    # No redis client dependency in scaffold; surface configuration only.
    return {"status": "configured", "reason": "client wiring deferred; endpoint present"}


def build_readiness(*, db: Session, redis_url: str | None, env: str) -> dict[str, Any]:
    database = check_database(db)
    redis = check_redis(redis_url)
    ready = database.get("status") == "up"
    return {
        "status": "ready" if ready else "not_ready",
        "env": env,
        "checks": {
            "database": database,
            "redis": redis,
        },
    }
