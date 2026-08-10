"""Structured API errors — re-exported from the domain kernel."""

from masms_api.kernel.errors import (
    AppError,
    ApprovalRequiredError,
    ConflictError,
    ForbiddenError,
    InvalidTransitionError,
    NotFoundError,
    TenantMismatchError,
    ValidationAppError,
)

__all__ = [
    "AppError",
    "ApprovalRequiredError",
    "ConflictError",
    "ForbiddenError",
    "InvalidTransitionError",
    "NotFoundError",
    "TenantMismatchError",
    "ValidationAppError",
]
