"""RFC 7807-style problem details payloads (MOD-020-MP-007)."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from masms_api.kernel.errors import AppError

PROBLEM_JSON_MEDIA_TYPE = "application/problem+json"
PROBLEM_TYPE_BASE = "https://masms.local/problems"


class ProblemDetails(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    code: str = Field(description="Stable machine code (MASMS extension)")
    correlation_id: UUID | None = None
    details: list[dict[str, Any]] | None = None


def problem_from_app_error(exc: AppError) -> ProblemDetails:
    return ProblemDetails(
        type=f"{PROBLEM_TYPE_BASE}/{exc.code}",
        title=exc.code,
        status=exc.status_code,
        detail=exc.message,
        code=exc.code,
        correlation_id=exc.correlation_id,
        details=exc.details,
    )


def problem_body(exc: AppError) -> dict[str, Any]:
    body = problem_from_app_error(exc).model_dump(mode="json")
    # Compatibility with existing web clients that read ``message``.
    body["message"] = exc.message
    return body
