from datetime import datetime, timezone
from pydantic import BaseModel, Field

class MeasurementFilter(BaseModel):
    limit: int = Field(10, gt=0, le=100, description="Maximum number of measurements to return (1–100).")
    since: datetime | None = Field(default=datetime(1970, 1, 1, tzinfo=timezone.utc), description='Start of the time range.')
    until: datetime | None = Field(None, description='End of the time range. If omitted, the current time is used.')
