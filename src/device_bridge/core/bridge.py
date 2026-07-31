import asyncio
import logging
from typing import Callable, List
from device_bridge.drivers.mock_serial import SerialHardwareDriver
from device_bridge.models.telemetry import SensorPayload

logger = logging.getLogger(__name__)


class AsyncDeviceBridge:
    """Asynchronous event-driven orchestrator bridging physical devices to application handlers."""

    def __init__(self, driver: SerialHardwareDriver) -> None:
        self.driver = driver
        self._callbacks: List[Callable[[SensorPayload], None]] = []
        self._running_task: asyncio.Task[None] | None = None

    def register_callback(self, callback: Callable[[SensorPayload], None]) -> None:
        """Registers listener callbacks to receive parsed telemetry packages."""
        self._callbacks.append(callback)

    async def start(self) -> None:
        """Starts the asynchronous hardware stream processing task."""
        await self.driver.connect()
        logger.info("Bridge connected to hardware driver on port %s", self.driver.port)
        self._running_task = asyncio.create_task(self._process_stream())

    async def _process_stream(self) -> None:
        try:
            async for payload in self.driver.read_telemetry_stream():
                logger.debug("Received payload from %s", payload.device_id)
                for cb in self._callbacks:
                    cb(payload)
        except asyncio.CancelledError:
            logger.info("Hardware streaming task gracefully cancelled.")
        finally:
            await self.driver.disconnect()

    async def stop(self) -> None:
        """Gracefully cancels the task and cleans up resources."""
        if self._running_task:
            self._running_task.cancel()
            await asyncio.gather(self._running_task, return_exceptions=True)
        logger.info("Bridge stopped.")