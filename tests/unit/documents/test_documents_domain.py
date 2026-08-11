"""Unit tests for MOD-250 document/scan domain."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from masms_api.errors import ForbiddenError, ValidationAppError
from masms_api.modules.documents import domain


def test_unsafe_scan_quarantines_and_blocks_available() -> None:
    assert domain.apply_scan_to_version_status("infected") == "quarantine"
    with pytest.raises(ForbiddenError):
        domain.assert_can_mark_available(
            status="quarantine",
            latest_verdict="infected",
            owner_actor_id="owner",
            effective_at=datetime.now(UTC),
        )


def test_clean_requires_owner_and_effective_date() -> None:
    with pytest.raises(ValidationAppError):
        domain.assert_can_mark_available(
            status="scanning",
            latest_verdict="clean",
            owner_actor_id="owner",
            effective_at=None,
        )
    domain.assert_can_mark_available(
        status="scanning",
        latest_verdict="clean",
        owner_actor_id="owner",
        effective_at=datetime(2026, 8, 11, tzinfo=UTC),
    )
    domain.assert_indexing_allowed(status="available", latest_verdict="clean")
    with pytest.raises(ForbiddenError):
        domain.assert_indexing_allowed(status="quarantine", latest_verdict="clean")


def test_access_covers_all_surfaces() -> None:
    domain.assert_access_granted(
        action="preview",
        version_status="available",
        can_download=False,
        can_preview=True,
        can_extract_text=False,
        can_use_embeddings=False,
    )
    with pytest.raises(ForbiddenError):
        domain.assert_access_granted(
            action="embeddings",
            version_status="available",
            can_download=True,
            can_preview=True,
            can_extract_text=True,
            can_use_embeddings=False,
        )
