import asyncio
from collections.abc import Callable
import logging

from device_bridge.drivers.mock_serial import SerialHardwareDriver
from device_bridge.models.telemetry import SensorPayload

logger = logging.getLogger(__name__)


class AsyncDeviceBridge:
    def __init__(self, driver: SerialHardwareDriver) -> None:
        self.driver = driver
        self._callbacks: list[Callable[[SensorPayload], None]] = []
        self._running_task: asyncio.Task[None] | None = None

    def register_callback(self, callback: Callable[[SensorPayload], None]) -> None:
        self._callbacks.append(callback)

    async def _process_stream(self) -> None:
        try:
            async for payload in self.driver.read_telemetry_stream():
                for cb in self._callbacks:
                    try:
                        cb(payload)
                    except Exception as err:  # noqa: BLE001
                        logger.error(f"Error in telemetry callback: {err}")
        except asyncio.CancelledError:
            logger.info("Telemetry stream processing cancelled cleanly.")
            raise

    async def start(self) -> None:
        if self._running_task is None or self._running_task.done():
            self._running_task = asyncio.create_task(self._process_stream())
            logger.info("Device bridge started processing stream.")

    async def stop(self) -> None:
        if self._running_task and not self._running_task.done():
            self._running_task.cancel()
            try:
                await self._running_task
            except asyncio.CancelledError:
                pass
            logger.info("Device bridge stopped successfully.")