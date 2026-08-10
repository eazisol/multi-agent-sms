"""Capacity domain rules (MOD-130)."""

from __future__ import annotations

from datetime import date, time
from decimal import Decimal

from masms_api.errors import ValidationAppError


def assert_proficiency(level: int) -> None:
    if level < 1 or level > 5:
        raise ValidationAppError("Proficiency must be between 1 and 5")


def assert_weekday(weekday: int) -> None:
    if weekday < 0 or weekday > 6:
        raise ValidationAppError("weekday must be 0 (Mon) through 6 (Sun)")


def assert_time_range(start: time, end: time) -> None:
    if start >= end:
        raise ValidationAppError("Availability start_time must be before end_time")


def assert_allocation_pct(value: Decimal) -> None:
    if value <= 0 or value > 100:
        raise ValidationAppError("allocation_pct must be greater than 0 and at most 100")


def assert_date_range(starts_on: date, ends_on: date, *, label: str = "period") -> None:
    if ends_on < starts_on:
        raise ValidationAppError(f"{label} ends_on must be on or after starts_on")


def is_business_day(*, weekday: int, is_holiday: bool) -> bool:
    """Simple Mon–Fri business day, excluding holidays."""
    return weekday < 5 and not is_holiday


def add_business_days(
    start: date,
    *,
    business_days: int,
    holiday_dates: set[date],
) -> date:
    if business_days < 0:
        raise ValidationAppError("business_days must be non-negative")
    current = start
    remaining = business_days
    # If start is not a business day, first advance to next business day when adding > 0
    while remaining > 0:
        current = date.fromordinal(current.toordinal() + 1)
        if is_business_day(weekday=current.weekday(), is_holiday=current in holiday_dates):
            remaining -= 1
    return current
