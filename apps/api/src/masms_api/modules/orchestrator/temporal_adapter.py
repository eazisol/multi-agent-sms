"""Temporal adapters for deterministic tests and the opt-in live runtime."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Coroutine
from typing import Any
from uuid import uuid4

from temporalio.client import Client

from masms_api.config import get_settings

logger = logging.getLogger(__name__)


class TemporalAdapter:
    """Deterministic stub used when no Temporal address is configured."""

    def start_workflow(
        self,
        *,
        workflow_type: str,
        workflow_id: str,
        input_payload: dict[str, Any] | None = None,
    ) -> str:
        run_id = f"stub-{uuid4()}"
        logger.info(
            "temporal_stub.start_workflow type=%s workflow_id=%s run_id=%s payload_keys=%s",
            workflow_type,
            workflow_id,
            run_id,
            sorted((input_payload or {}).keys()),
        )
        return run_id

    def signal_workflow(
        self,
        *,
        workflow_id: str,
        signal_name: str,
        payload: dict[str, Any] | None = None,
        run_id: str | None = None,
    ) -> None:
        logger.info(
            "temporal_stub.signal_workflow workflow_id=%s run_id=%s signal=%s payload_keys=%s",
            workflow_id,
            run_id,
            signal_name,
            sorted((payload or {}).keys()),
        )

    def wait_for_workflow_result(
        self,
        *,
        workflow_id: str,
        run_id: str | None = None,
        timeout_seconds: float = 5.0,
    ) -> dict[str, Any] | None:
        _ = workflow_id, run_id, timeout_seconds
        return None

    def cancel_workflow(
        self,
        *,
        workflow_id: str,
        run_id: str | None = None,
        reason: str | None = None,
    ) -> None:
        logger.info(
            "temporal_stub.cancel_workflow workflow_id=%s run_id=%s reason=%s",
            workflow_id,
            run_id,
            reason,
        )


class LiveTemporalAdapter(TemporalAdapter):
    """Synchronous application-service bridge to the asynchronous Temporal client."""

    def __init__(self, *, address: str, namespace: str, task_queue: str) -> None:
        self.address = address
        self.namespace = namespace
        self.task_queue = task_queue

    async def _client(self) -> Client:
        return await Client.connect(self.address, namespace=self.namespace)

    def start_workflow(
        self,
        *,
        workflow_type: str,
        workflow_id: str,
        input_payload: dict[str, Any] | None = None,
    ) -> str:
        async def start() -> str:
            client = await self._client()
            handle = await client.start_workflow(
                workflow_type,
                input_payload or {},
                id=workflow_id,
                task_queue=self.task_queue,
            )
            if not handle.result_run_id:
                raise RuntimeError("Temporal did not return a workflow run id")
            return handle.result_run_id

        return _run(start())

    def signal_workflow(
        self,
        *,
        workflow_id: str,
        signal_name: str,
        payload: dict[str, Any] | None = None,
        run_id: str | None = None,
    ) -> None:
        async def signal() -> None:
            client = await self._client()
            handle = client.get_workflow_handle(workflow_id, run_id=run_id)
            await handle.signal(signal_name, payload or {})

        _run(signal())

    def wait_for_workflow_result(
        self,
        *,
        workflow_id: str,
        run_id: str | None = None,
        timeout_seconds: float = 5.0,
    ) -> dict[str, Any] | None:
        async def wait() -> dict[str, Any] | None:
            client = await self._client()
            handle = client.get_workflow_handle(workflow_id, run_id=run_id)
            try:
                result = await asyncio.wait_for(handle.result(), timeout=timeout_seconds)
            except TimeoutError:
                return None
            if not isinstance(result, dict):
                raise RuntimeError("Temporal workflow returned an invalid completion result")
            return result

        return _run(wait())

    def cancel_workflow(
        self,
        *,
        workflow_id: str,
        run_id: str | None = None,
        reason: str | None = None,
    ) -> None:
        async def cancel() -> None:
            client = await self._client()
            handle = client.get_workflow_handle(workflow_id, run_id=run_id)
            await handle.cancel()

        logger.info(
            "temporal.cancel_workflow workflow_id=%s run_id=%s reason=%s",
            workflow_id,
            run_id,
            reason,
        )
        _run(cancel())


def _run[T](awaitable: Coroutine[Any, Any, T]) -> T:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(awaitable)
    awaitable.close()
    raise RuntimeError("LiveTemporalAdapter must be called from a synchronous service context")


def get_temporal_adapter() -> TemporalAdapter:
    """Select live Temporal only when its address is explicitly configured."""
    settings = get_settings()
    if settings.temporal_address:
        return LiveTemporalAdapter(
            address=settings.temporal_address,
            namespace=settings.temporal_namespace,
            task_queue=settings.temporal_task_queue,
        )
    return TemporalAdapter()
