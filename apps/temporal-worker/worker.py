"""Run the local MASMS Temporal worker."""

from __future__ import annotations

import asyncio
import logging

from masms_api.config import get_settings
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import QueryIntakeWorkflow


async def main() -> None:
    settings = get_settings()
    address = settings.temporal_address or "localhost:7233"
    client = await Client.connect(address, namespace=settings.temporal_namespace)
    worker = Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=[QueryIntakeWorkflow],
    )
    await worker.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
