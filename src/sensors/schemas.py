from typing import Optional
from sqlmodel import Field, SQLModel

from .models import SensorStatus

class SensorUpdate(SQLModel):
    name: Optional[str] = Field(default=None, description='New sensor name')
    segment_id: Optional[int] = Field(default=None, description='New segment ID the sensor belongs to')

class SensorStatusUpdate(SQLModel):
    status: SensorStatus