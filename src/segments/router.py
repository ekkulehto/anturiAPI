from typing import Annotated
from fastapi import APIRouter, Path, Query, status, Depends
from sqlmodel import Session

from ..measurements.schemas import MeasurementFilterForGetSegmentById
from ..database import get_session
from .schemas import SegmentUpdate
from ..segments import service as crud
from ..models import SegmentIn, SegmentOut, SegmentOutWithNumberOfSensors, SegmentOutWithSensors, SensorStatus

from .docs import (
        GET_ALL_SEGMENTS_SUMMARY,
        GET_ALL_SEGMENTS_DESCRIPTION,
        CREATE_SEGMENT_SUMMARY,
        CREATE_SEGMENT_DESCRIPTION,
        GET_SEGMENT_BY_ID_SUMMARY,
        GET_SEGMENT_BY_ID_DESCRIPTION,
        UPDATE_SEGMENT_BY_ID_SUMMARY,
        UPDATE_SEGMENT_BY_ID_DESCRIPTION,
        DELETE_SEGMENT_BY_ID_SUMMARY,
        DELETE_SEGMENT_BY_ID_DESCRIPTION,
)

router = APIRouter(prefix='/segments', tags=['Segments'])

# =================================================================================
#    GET ALL SEGMENTS
# =================================================================================

@router.get(
        '', 
        response_model=list[SegmentOutWithNumberOfSensors],
        summary=GET_ALL_SEGMENTS_SUMMARY,
        description=GET_ALL_SEGMENTS_DESCRIPTION
)
def get_all_segments(
    *, 
    session: Session = Depends(get_session)
):
    return crud.get_all_segments(session)

# =================================================================================
#    CREATE NEW SEGMENT
# =================================================================================

@router.post(
        '', 
        status_code=status.HTTP_201_CREATED, 
        response_model=SegmentOut,
        summary=CREATE_SEGMENT_SUMMARY,
        description=CREATE_SEGMENT_DESCRIPTION
)
def create_segment(
    *, 
    session: Session = Depends(get_session), 
    segment_in: SegmentIn
):
    return crud.create_segment(session, segment_in)

# =================================================================================
#    GET SEGMENT BY ID
# =================================================================================

@router.get(
    '/{segment_id}',
    response_model=SegmentOutWithSensors,
    summary=GET_SEGMENT_BY_ID_SUMMARY,
    description=GET_SEGMENT_BY_ID_DESCRIPTION,
)
def get_segment_by_id(
    *,
    session: Session = Depends(get_session),
    segment_id: int = Path(..., description='Unique identifier of the segment to retrieve'),
    sensor_status: SensorStatus | None = Query(
        default=None,
        description="Optional filter for current sensor status.",
    ),
):
    return crud.get_segment_by_id(session, segment_id, sensor_status)

# =================================================================================
#    UPDATE SEGMENT BY ID
# =================================================================================

@router.patch(
        '/{segment_id}', 
        response_model=SegmentOut,
        summary=UPDATE_SEGMENT_BY_ID_SUMMARY,
        description=UPDATE_SEGMENT_BY_ID_DESCRIPTION
)
def update_segment_by_id(
    *, 
    session: Session = Depends(get_session), 
    segment_id: int = Path(..., description='Unique identifier of the segment to update'), 
    segment_update: SegmentUpdate
):
    return crud.update_segment_by_id(session, segment_id, segment_update)

# =================================================================================
#    DELETE SEGMENT BY ID
# =================================================================================

@router.delete(
        '/{segment_id}', 
        response_model=SegmentOut,
        summary=DELETE_SEGMENT_BY_ID_SUMMARY,
        description=DELETE_SEGMENT_BY_ID_DESCRIPTION
)
def delete_segment_by_id(
    *, 
    session: Session = Depends(get_session), 
    segment_id: int = Path(..., description='Unique identifier of the segment to delete'), 
):
    return crud.delete_segment_by_id(session, segment_id)