from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator

from ..sensors.models import SensorDb

class MeasurementBase(SQLModel):
    sensor_id: int
    temperature: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator('temperature')
    @classmethod
    def round_temperature_to_one_decimal(cls, temperature: float) -> float:
        return round(temperature, 1)

class MeasurementIn(MeasurementBase):
    pass

class MeasurementOut(SQLModel):
    id: int
    temperature: float
    timestamp: datetime

class MeasurementOutWithSensor(SQLModel):
    sensor_id: int
    measurement: 'MeasurementOut'

class MeasurementDb(MeasurementBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key='sensordb.id')
    sensor: Optional['SensorDb'] = Relationship(back_populates='measurements')
