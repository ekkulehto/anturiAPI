from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator

class SensorBase(SQLModel):
    name: str
    status: str

class SensorIn(SensorBase):
    pass

class SensorDb(SensorBase, table=True):
    id: int = Field(default=None, primary_key=True)
    segment_id: int = Field(default=None, foreign_key='segmentdb.id', nullable=False)
    measurements: list['MeasurementDb'] = Relationship(back_populates='sensor')
    segment: 'SegmentDb' | None = Relationship(back_populates='sensors')

class MeasurementBase(SQLModel):
    measurement: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator('measurement')
    @classmethod
    def round_measurement_to_one_decimal(cls, measurement: float) -> float:
        return round(measurement, 1)

class MeasurementIn(MeasurementBase):
    pass

class MeasurementDb(MeasurementBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sensor_id: int = Field(default=None, foreign_key='sensordb.id')
    sensor: SensorDb | None = Relationship(back_populates='measurements')

class SegmentBase(SQLModel):
    name: str

class SegmentIn(SegmentBase):
    pass

class SegmentDb(SegmentBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sensors: list['SensorDb'] = Relationship(back_populates='segment')