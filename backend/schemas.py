from typing import Optional
from pydantic import BaseModel

class DeviceLog(BaseModel):
    id: int
    user_id: int
    name: str
    watering_status: str
    battery_voltage: Optional[float] = None
    issues: Optional[str] = None

    class Config:
        # pydantic v2 uses 'from_attributes' instead of 'orm_mode'
        from_attributes = True
