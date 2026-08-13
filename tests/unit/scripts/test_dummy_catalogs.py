"""Catalog size checks for dummy data used in local UI testing."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from dummy_catalogs import (  # noqa: E402
    ADRS,
    AGENT_CODES,
    APPROVAL_ACTIONS,
    BUGS,
    CLIENTS,
    CONFIG_WORKFLOW_CODES,
    CONTACTS,
    IDENTITY_AGENT_KEYS,
    KNOWLEDGE,
    NOTIFICATIONS,
    PEOPLE,
    PERMISSIONS,
    PROJECTS,
    QUERIES,
    QUERY_SOURCES,
    ROLES,
    SKILLS,
    TEAMS,
    WORKFLOW_CODES,
)


def test_dummy_catalogs_have_twenty_primary_entities() -> None:
    assert len(PEOPLE) == 20
    assert len(ROLES) == 20
    assert len(TEAMS) == 20
    assert len(CLIENTS) == 20
    assert len(CONTACTS) == 20
    assert len(PROJECTS) == 20
    assert len(QUERIES) == 20
    assert len(SKILLS) == 20
    assert len(PERMISSIONS) == 20
    assert len(ADRS) == 20
    assert len(KNOWLEDGE) == 20
    assert len(BUGS) == 20
    assert len(NOTIFICATIONS) == 20
    assert len(AGENT_CODES) == 6
    assert len(WORKFLOW_CODES) == 12
    assert len(IDENTITY_AGENT_KEYS) == 20
    assert len(CONFIG_WORKFLOW_CODES) == 20
    assert len(QUERY_SOURCES) == 20
    assert len(APPROVAL_ACTIONS) == 20


def test_dummy_catalogs_use_synthetic_contacts() -> None:
    assert all(email.endswith("@eazisols.example") for _, email, _ in PEOPLE)
    assert all("seed-" not in code for code, *_ in CLIENTS)
    assert all(not title.lower().startswith("seed") for _, title in PROJECTS)
