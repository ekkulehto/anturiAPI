from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from enum import Enum

class SensorStatus(str, Enum):
    NORMAL = "NORMAL"
    ERROR = "ERROR"

# =================================================================================
#    Sensor model
# =================================================================================

class SensorBase(SQLModel):
    name: str

class SensorIn(SensorBase):
    pass

class SensorDb(SensorBase, table=True):
    id: int = Field(default=None, primary_key=True)
    status: SensorStatus = SensorStatus.NORMAL
    segment_id: int = Field(default=None, foreign_key='segmentdb.id', nullable=False)
    measurements: list['MeasurementDb'] = Relationship(back_populates='sensor')
    segment: Optional['SegmentDb'] = Relationship(back_populates='sensors')
    status_history: list['SensorStatusDb'] = Relationship(back_populates='sensor')

# =================================================================================
#    Sensor status model
# =================================================================================

class SensorStatusBase(SQLModel):
    status: SensorStatus
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SensorStatusIn(SensorStatusBase):
    pass

class SensorStatusDb(SensorStatusBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sensor_id: int = Field(default=None, foreign_key='sensordb.id', nullable=False)
    sensor: Optional['SensorDb'] = Relationship(back_populates='status_history')

# =================================================================================
#    Measurement model
# =================================================================================

class MeasurementBase(SQLModel):
    temperature: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator('temperature')
    @classmethod
    def round_temperature_to_one_decimal(cls, temperature: float) -> float:
        return round(temperature, 1)

class MeasurementIn(MeasurementBase):
    pass

class MeasurementDb(MeasurementBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sensor_id: int = Field(default=None, foreign_key='sensordb.id')
    sensor: Optional['SensorDb'] = Relationship(back_populates='measurements')

# =================================================================================
#    Segment model
# =================================================================================

class SegmentBase(SQLModel):
    name: str

class SegmentIn(SegmentBase):
    pass

class SegmentDb(SegmentBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sensors: list['SensorDb'] = Relationship(back_populates='segment')