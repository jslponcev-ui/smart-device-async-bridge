import asyncio

import pytest

from device_bridge.core.bridge import AsyncDeviceBridge
from device_bridge.drivers.mock_serial import SerialHardwareDriver
from device_bridge.models.entities import Entity


@pytest.mark.asyncio
async def test_home_assistant_entity_mapping() -> None:
    driver = SerialHardwareDriver(port="/dev/ttyUSB0")
    bridge = AsyncDeviceBridge(driver)

    latest_entities: dict[str, Entity] = {}

    def handle_entity_update(entities: dict[str, Entity]) -> None:
        nonlocal latest_entities
        latest_entities = entities.copy()

    bridge.register_callback(handle_entity_update)

    await bridge.start()
    await asyncio.sleep(1.2)
    await bridge.stop()

    assert "temperature" in latest_entities
    assert latest_entities["temperature"].unit_of_measurement == "°C"
    assert latest_entities["temperature"].state is not None
    assert isinstance(latest_entities["temperature"].state, float)