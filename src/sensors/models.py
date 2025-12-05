from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

from ..segments.models import SegmentOut, SegmentDb
from ..measurements.models import MeasurementOut, MeasurementDb

# =================================================================================
#    Enumerables
# =================================================================================

class SensorStatus(str, Enum):
    NORMAL = "NORMAL"
    ERROR = "ERROR"

# =================================================================================
#    Sensor model
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
#    Sensor status model
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