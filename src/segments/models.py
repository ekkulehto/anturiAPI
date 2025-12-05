from sqlmodel import SQLModel, Field, Relationship
from ..sensors.models import SensorDb, SensorOutWithLastMeasurement

class SegmentBase(SQLModel):
    name: str

class SegmentIn(SegmentBase):
    pass

class SegmentOut(SQLModel):
    id: int
    name: str

class SegmentOutWithSensors(SQLModel):
    id: int
    name: str
    sensors: list['SensorOutWithLastMeasurement'] = Field(default_factory=list)

class SegmentDb(SegmentBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sensors: list['SensorDb'] = Relationship(back_populates='segment')