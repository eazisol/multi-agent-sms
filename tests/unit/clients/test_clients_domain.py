"""Unit tests for MOD-200 clients domain."""

from __future__ import annotations

from uuid import uuid4

import pytest
from masms_api.errors import ValidationAppError
from masms_api.modules.clients import domain


def test_authority_and_email() -> None:
    domain.assert_authority_level("decision_maker")
    with pytest.raises(ValidationAppError):
        domain.assert_authority_level("boss")
    assert domain.normalize_email("  A@B.com ") == "a@b.com"
    with pytest.raises(ValidationAppError):
        domain.assert_distinct_clients("a", "a")
    domain.assert_distinct_clients(uuid4(), uuid4())
