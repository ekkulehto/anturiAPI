from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from pydantic import field_validator

# =================================================================================
#    ENUMERABLES
# =================================================================================

class SensorStatus(str, Enum):
    NORMAL = "NORMAL"
    ERROR = "ERROR"

class MeasurementType(str, Enum):
    TEMPERATURE = 'TEMPERATURE'

class MeasurementUnit(str, Enum):
    CELSIUS = 'CELSIUS'

# =================================================================================
#    SENSORS
# =================================================================================

class SensorBase(SQLModel):
    name: str
    segment_id: int

class SensorIn(SensorBase):
    pass

class SensorOut(SQLModel):
    id: int
    name: str
    status: SensorStatus
    segment: 'SegmentOut'

class SensorOutWithMeasurements(SQLModel):
    id: int
    name: str
    status: SensorStatus
    segment: 'SegmentOut'
    measurements: list['MeasurementOut'] = Field(default_factory=list)

class SensorOutWithLastMeasurement(SQLModel):
    id: int
    name: str
    status: SensorStatus
    last_measurement: Optional['MeasurementOut'] = None

class SensorOutWithStatusHistory(SQLModel):
    id: int
    name: str
    segment: 'SegmentOut'
    status_history: list['SensorStatusOut'] = Field(default_factory=list)

class SensorDb(SensorBase, table=True):
    id: int = Field(default=None, primary_key=True)
    status: SensorStatus = SensorStatus.NORMAL
    segment_id: int = Field(foreign_key='segmentdb.id', nullable=False)
    segment: Optional['SegmentDb'] = Relationship(back_populates='sensors')
    measurements: list['MeasurementDb'] = Relationship(
        back_populates='sensor',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'}
        )
    status_history: list['SensorStatusDb'] = Relationship(
        back_populates='sensor',
        sa_relationship_kwargs={'cascade': 'all, delete-orphan'}
        )

# =================================================================================
#    SENSOR STATUSES
# =================================================================================

class SensorStatusBase(SQLModel):
    status: SensorStatus
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SensorStatusIn(SensorStatusBase):
    sensor_id: int

class SensorStatusOut(SQLModel):
    id: int
    status: SensorStatus
    timestamp: datetime

class SensorStatusDb(SensorStatusBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key='sensordb.id', nullable=False)
    sensor: Optional['SensorDb'] = Relationship(back_populates='status_history')

# =================================================================================
#    MEASUREMENTS
# =================================================================================

class MeasurementBase(SQLModel):
    sensor_id: int

class MeasurementPayload(SQLModel):
    value: float
    unit: MeasurementUnit = Field(default=MeasurementUnit.CELSIUS)
    type: MeasurementType = Field(default=MeasurementType.TEMPERATURE)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator('value')
    @classmethod
    def round_value_to_one_decimal(cls, value: float) -> float:
        return round(value, 1)

class MeasurementIn(MeasurementBase):
    measurement: 'MeasurementPayload'

class MeasurementOut(SQLModel):
    id: int
    value: float
    unit: str
    type: str
    timestamp: datetime

class MeasurementOutWithSensor(MeasurementBase):
    measurement: 'MeasurementOut'

class MeasurementDb(MeasurementBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key='sensordb.id')
    sensor: Optional['SensorDb'] = Relationship(back_populates='measurements')
    value: float
    unit: MeasurementUnit
    type: MeasurementType
    timestamp: datetime

# =================================================================================
#    SEGMENTS
# =================================================================================

class SegmentBase(SQLModel):
    name: str

class SegmentIn(SegmentBase):
    pass

class SegmentOut(SQLModel):
    id: int
    name: str

class SegmentOutWithNumberOfSensors(SQLModel):
    id: int
    name: str
    number_of_sensors: int

class SegmentOutWithSensors(SQLModel):
    id: int
    name: str
    sensors: list['SensorOutWithLastMeasurement'] = Field(default_factory=list)

class SegmentDb(SegmentBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sensors: list['SensorDb'] = Relationship(back_populates='segment')