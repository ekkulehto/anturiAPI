from datetime import datetime, timezone
from pydantic import BaseModel, Field

from ..models import MeasurementType

class MeasurementFilterForGetSensorById(BaseModel):
    measurement_type: MeasurementType | None = Field(
        default=None, 
        description='Optional measurement type filter.'
    )
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