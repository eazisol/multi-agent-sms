"""Shared list pagination helpers (MOD-020-MP-008)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from masms_api.kernel.errors import ValidationAppError

DEFAULT_MAX_PAGE_LIMIT = 100


class PageMeta(BaseModel):
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)
    total: int = Field(ge=0)
    has_more: bool


def normalize_paging(
    limit: int,
    offset: int,
    *,
    max_limit: int = DEFAULT_MAX_PAGE_LIMIT,
) -> tuple[int, int]:
    if limit < 1 or limit > max_limit:
        raise ValidationAppError(f"limit must be between 1 and {max_limit}")
    if offset < 0:
        raise ValidationAppError("offset must be >= 0")
    return limit, offset


def build_page_meta(*, limit: int, offset: int, total: int) -> PageMeta:
    return PageMeta(
        limit=limit,
        offset=offset,
        total=total,
        has_more=offset + limit < total,
    )
