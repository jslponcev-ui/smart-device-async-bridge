import asyncio
import random
from typing import AsyncGenerator
from device_bridge.models.telemetry import DeviceStatus, SensorPayload


class SerialHardwareDriver:
    """Emulates an asynchronous data stream from a physical UART/Serial interface."""

    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200) -> None:
        self.port = port
        self.baudrate = baudrate
        self._is_connected = False

    async def connect(self) -> None:
        """Simulates establishing connection to physical hardware interface."""
        await asyncio.sleep(0.1)  # Simulate hardware connection delay
        self._is_connected = True

    async def disconnect(self) -> None:
        """Closes the connection safely."""
        self._is_connected = False

    async def read_telemetry_stream(self) -> AsyncGenerator[SensorPayload, None]:
        """Asynchronously yields decoded telemetry packets from the hardware stream."""
        if not self._is_connected:
            raise ConnectionError("Hardware interface is not connected.")

        while self._is_connected:
            await asyncio.sleep(0.5)  # Stream frequency

            # Simulate hardware reading sensor telemetry
            temp = round(random.uniform(18.0, 26.0), 2)
            hum = round(random.uniform(40.0, 60.0), 2)
            volt = round(random.uniform(3.2, 3.3), 2)

            yield SensorPayload(
                device_id="NABU-HW-001",
                temperature=temp,
                humidity=hum,
                voltage=volt,
                status=DeviceStatus.ONLINE,
            )