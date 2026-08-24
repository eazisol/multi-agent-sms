"""Temporal adapter selection and client bridge tests."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from masms_api.modules.orchestrator import temporal_adapter as adapter_module
from masms_api.modules.orchestrator.temporal_adapter import (
    LiveTemporalAdapter,
    TemporalAdapter,
)


def test_factory_defaults_to_stub(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        adapter_module,
        "get_settings",
        lambda: SimpleNamespace(
            temporal_address=None,
            temporal_namespace="default",
            temporal_task_queue="masms-local",
        ),
    )

    assert type(adapter_module.get_temporal_adapter()) is TemporalAdapter


def test_factory_selects_live_adapter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        adapter_module,
        "get_settings",
        lambda: SimpleNamespace(
            temporal_address="localhost:7233",
            temporal_namespace="default",
            temporal_task_queue="masms-local",
        ),
    )

    assert isinstance(adapter_module.get_temporal_adapter(), LiveTemporalAdapter)


def test_live_adapter_starts_workflow(monkeypatch: pytest.MonkeyPatch) -> None:
    handle = SimpleNamespace(result_run_id="run-123")
    client = Mock()
    client.start_workflow = AsyncMock(return_value=handle)
    adapter = LiveTemporalAdapter(
        address="localhost:7233",
        namespace="default",
        task_queue="masms-local",
    )
    monkeypatch.setattr(adapter, "_client", AsyncMock(return_value=client))

    run_id = adapter.start_workflow(
        workflow_type="masms.query_intake",
        workflow_id="query_intake:test",
        input_payload={"query_id": "test"},
    )

    assert run_id == "run-123"
    client.start_workflow.assert_awaited_once()


def test_live_adapter_reads_completed_workflow_result(monkeypatch: pytest.MonkeyPatch) -> None:
    handle = SimpleNamespace(result=AsyncMock(return_value={"status": "completed"}))
    client = Mock()
    client.get_workflow_handle.return_value = handle
    adapter = LiveTemporalAdapter(
        address="localhost:7233",
        namespace="default",
        task_queue="masms-local",
    )
    monkeypatch.setattr(adapter, "_client", AsyncMock(return_value=client))

    assert adapter.wait_for_workflow_result(workflow_id="query_intake:test") == {
        "status": "completed"
    }
