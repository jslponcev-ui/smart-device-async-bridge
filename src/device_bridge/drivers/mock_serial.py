import asyncio
from collections.abc import AsyncGenerator
import random

from device_bridge.models.telemetry import DeviceStatus, SensorPayload


class SerialHardwareDriver:
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200) -> None:
        self.port = port
        self.baudrate = baudrate

    async def read_telemetry_stream(self) -> AsyncGenerator[SensorPayload, None]:
        device_id = "NABU-HW-001"
        while True:
            await asyncio.sleep(0.5)  # Simula frecuencia de muestreo de 2 Hz
            yield SensorPayload(
                device_id=device_id,
                temperature=round(random.uniform(18.0, 32.0), 2),
                humidity=round(random.uniform(30.0, 85.0), 2),
                voltage=round(random.uniform(3.1, 3.3), 2),
                status=DeviceStatus.ONLINE,
            )