import asyncio
import pytest
from device_bridge.core.bridge import AsyncDeviceBridge
from device_bridge.drivers.mock_serial import SerialHardwareDriver
from device_bridge.models.telemetry import SensorPayload


@pytest.mark.asyncio
async def test_hardware_bridge_stream() -> None:
    driver = SerialHardwareDriver(port="/dev/ttyUSB0")
    bridge = AsyncDeviceBridge(driver)

    received_payloads: list[SensorPayload] = []

    def handle_telemetry(payload: SensorPayload) -> None:
        received_payloads.append(payload)

    bridge.register_callback(handle_telemetry)

    await bridge.start()
    await asyncio.sleep(1.2)  # Permitir la captura de al menos 2 ticks
    await bridge.stop()

    assert len(received_payloads) >= 2
    assert received_payloads[0].device_id == "NABU-HW-001"
    assert received_payloads[0].temperature >= 18.0