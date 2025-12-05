from datetime import datetime
from pydantic import BaseModel, Field

class MeasurementFilter(BaseModel):
    limit: int = Field(10, gt=0, le=100, description="Number of measurements")
    since: datetime | None = Field(default='1970-01-01T00:00:00Z', description='Beginning of timespan (e.g 1970-01-01T00:00:00Z)')
    until: datetime | None = Field(None, description='Ending of timespan (e.g 1970-01-01T00:00:00Z)')
