from datetime import datetime, timezone
from pydantic import BaseModel, Field

from ..models import MeasurementType

class MeasurementFilterForGetSensorById(BaseModel):
    limit: int = Field(
        10, 
        gt=0, 
        le=100, 
        description="Maximum number of measurements to return (1–100)."
    )
    since: datetime | None = Field(
        default=datetime(1970, 1, 1, tzinfo=timezone.utc), 
        description='Start of the time range.'
    )
    until: datetime | None = Field(
        default=None,
        description='End of the time range. If omitted, the current time is used.'
    )

class MeasurementFilterForGetSegmentById(BaseModel):
    limit: int = Field(
        default=1,
        ge=1,
        le=100,
        description='Maximum number of latest measurements to include per sensor (1–100).',
    )
    measurement_type: MeasurementType | None = Field(
        default=None,
        description='Optional filter for measurement type.',
    )
    since: datetime | None = Field(
        default=None,
        description='Optional start of the time range for measurements.',
    )
    until: datetime | None = Field(
        default=None,
        description='Optional end of the time range for measurements.',
    )