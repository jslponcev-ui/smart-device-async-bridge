from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DeviceClass(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    VOLTAGE = "voltage"


class Entity(BaseModel):
    unique_id: str = Field(..., description="Unique entity identifier within Home Assistant")
    name: str = Field(..., description="Friendly entity name")
    device_class: DeviceClass
    unit_of_measurement: str
    state: Any = Field(default=None, description="Current entity state")

    def update_state(self, new_state: Any) -> None:
        self.state = new_state