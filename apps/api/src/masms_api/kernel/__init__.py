"""Shared domain kernel and API standards (MOD-020)."""

from masms_api.kernel.actor import ActorContext, ActorKind
from masms_api.kernel.concurrency import assert_expected_version
from masms_api.kernel.context import RequestContext
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
from masms_api.kernel.ids import (
    ActorId,
    ClientId,
    CorrelationId,
    EntityId,
    OrganizationId,
    ProjectId,
)
from masms_api.kernel.outbox import OutboxMessage, enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.problem import PROBLEM_JSON_MEDIA_TYPE, ProblemDetails, problem_body
from masms_api.kernel.tenant import TenantContext
from masms_api.kernel.uow import SqlAlchemyUnitOfWork

__all__ = [
    "ActorContext",
    "ActorId",
    "ActorKind",
    "AppError",
    "ApprovalRequiredError",
    "ClientId",
    "ConflictError",
    "CorrelationId",
    "EntityId",
    "ForbiddenError",
    "InvalidTransitionError",
    "NotFoundError",
    "OrganizationId",
    "OutboxMessage",
    "PROBLEM_JSON_MEDIA_TYPE",
    "PageMeta",
    "ProblemDetails",
    "ProjectId",
    "RequestContext",
    "SqlAlchemyUnitOfWork",
    "TenantContext",
    "TenantMismatchError",
    "ValidationAppError",
    "assert_expected_version",
    "build_page_meta",
    "enqueue_outbox",
    "normalize_paging",
    "problem_body",
]
