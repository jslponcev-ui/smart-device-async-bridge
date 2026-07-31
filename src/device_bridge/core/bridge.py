import asyncio
from collections.abc import Callable
import logging

from device_bridge.drivers.mock_serial import SerialHardwareDriver
from device_bridge.models.entities import DeviceClass, Entity
from device_bridge.models.telemetry import SensorPayload

logger = logging.getLogger(__name__)


class AsyncDeviceBridge:
    def __init__(self, driver: SerialHardwareDriver) -> None:
        self.driver = driver
        self.entities: dict[str, Entity] = {}
        self._callbacks: list[Callable[[dict[str, Entity]], None]] = []
        self._running_task: asyncio.Task[None] | None = None
        self._setup_entities()

    def _setup_entities(self) -> None:
        """Inicializa las entidades estilo Home Assistant para este dispositivo."""
        device_id = "NABU-HW-001"
        self.entities["temperature"] = Entity(
            unique_id=f"{device_id}_temperature",
            name="Nabu Device Temperature",
            device_class=DeviceClass.TEMPERATURE,
            unit_of_measurement="°C",
        )
        self.entities["humidity"] = Entity(
            unique_id=f"{device_id}_humidity",
            name="Nabu Device Humidity",
            device_class=DeviceClass.HUMIDITY,
            unit_of_measurement="%",
        )
        self.entities["voltage"] = Entity(
            unique_id=f"{device_id}_voltage",
            name="Nabu Device Voltage",
            device_class=DeviceClass.VOLTAGE,
            unit_of_measurement="V",
        )

    def register_callback(self, callback: Callable[[dict[str, Entity]], None]) -> None:
        self._callbacks.append(callback)

    def _process_payload(self, payload: SensorPayload) -> None:
        """Mapea la telemetría del hardware a los estados de las entidades."""
        self.entities["temperature"].update_state(payload.temperature)
        self.entities["humidity"].update_state(payload.humidity)
        self.entities["voltage"].update_state(payload.voltage)

        for cb in self._callbacks:
            try:
                cb(self.entities)
            except Exception as err:  # noqa: BLE001
                logger.error(f"Error in entity callback: {err}")

    async def _process_stream(self) -> None:
        try:
            async for payload in self.driver.read_telemetry_stream():
                self._process_payload(payload)
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