"""Unit tests for MOD-130 capacity domain."""

from __future__ import annotations

from datetime import date, time
from decimal import Decimal

import pytest
from masms_api.errors import ValidationAppError
from masms_api.modules.capacity import domain


def test_validation_helpers() -> None:
    domain.assert_proficiency(3)
    with pytest.raises(ValidationAppError):
        domain.assert_proficiency(6)
    domain.assert_weekday(0)
    with pytest.raises(ValidationAppError):
        domain.assert_weekday(7)
    domain.assert_time_range(time(9, 0), time(17, 0))
    with pytest.raises(ValidationAppError):
        domain.assert_time_range(time(17, 0), time(9, 0))
    domain.assert_allocation_pct(Decimal("50"))
    with pytest.raises(ValidationAppError):
        domain.assert_allocation_pct(Decimal("0"))


def test_add_business_days_skips_weekend_and_holiday() -> None:
    # Friday 2026-08-14 + 1 business day -> Monday 2026-08-17
    friday = date(2026, 8, 14)
    assert domain.add_business_days(friday, business_days=1, holiday_dates=set()) == date(
        2026, 8, 17
    )
    # Thursday 2026-08-13 + 1 with Friday holiday -> Monday
    thursday = date(2026, 8, 13)
    assert domain.add_business_days(
        thursday, business_days=1, holiday_dates={date(2026, 8, 14)}
    ) == date(2026, 8, 17)
