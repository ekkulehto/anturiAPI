from typing import Optional
from sqlmodel import Field, SQLModel

class SegmentUpdate(SQLModel):
    name: Optional[str] = Field(default=None, description='New Segment name')