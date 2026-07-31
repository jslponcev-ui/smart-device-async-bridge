from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field


class DeviceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"


class SensorPayload(BaseModel):
    device_id: str = Field(..., description="Unique hardware identifier")
    temperature: float = Field(..., ge=-40.0, le=125.0, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0.0, le=100.0, description="Relative humidity %")
    voltage: float = Field(..., ge=0.0, le=5.0, description="Hardware supply voltage")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: DeviceStatus = DeviceStatus.ONLINE