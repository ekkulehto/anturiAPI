from sqlmodel import SQLModel

from ..models import SensorStatus

class SensorStatusUpdate(SQLModel):
    status: SensorStatus