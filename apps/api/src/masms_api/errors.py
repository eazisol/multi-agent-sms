"""Structured API errors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass
class AppError(Exception):
    code: str
    message: str
    status_code: int
    details: list[dict[str, Any]] | None = None
    correlation_id: UUID | None = None


class NotFoundError(AppError):
    def __init__(self, message: str, *, correlation_id: UUID | None = None) -> None:
        super().__init__("not_found", message, 404, correlation_id=correlation_id)


class ConflictError(AppError):
    def __init__(self, message: str, *, correlation_id: UUID | None = None) -> None:
        super().__init__("conflict", message, 409, correlation_id=correlation_id)


class ValidationAppError(AppError):
    def __init__(
        self,
        message: str,
        *,
        details: list[dict[str, Any]] | None = None,
        correlation_id: UUID | None = None,
    ) -> None:
        super().__init__(
            "validation_error",
            message,
            422,
            details=details,
            correlation_id=correlation_id,
        )


class ForbiddenError(AppError):
    def __init__(self, message: str, *, correlation_id: UUID | None = None) -> None:
        super().__init__("forbidden", message, 403, correlation_id=correlation_id)


class ApprovalRequiredError(AppError):
    def __init__(self, message: str, *, correlation_id: UUID | None = None) -> None:
        super().__init__("approval_required", message, 409, correlation_id=correlation_id)


class InvalidTransitionError(AppError):
    def __init__(self, message: str, *, correlation_id: UUID | None = None) -> None:
        super().__init__("invalid_transition", message, 409, correlation_id=correlation_id)
