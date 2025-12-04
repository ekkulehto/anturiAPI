from fastapi import APIRouter, status, Depends
from sqlmodel import Session

from app.schemas.segments import SegmentUpdate
from ..database.database import get_session

from ..database import segments_crud as crud
from ..database.models import SegmentIn, SegmentDb, SegmentOutWithSensors

router = APIRouter(prefix='/segments', tags=['segments'])

@router.get('', response_model=list[SegmentDb])
def get_all_segments(*, session: Session = Depends(get_session)):
    return crud.get_all_segments(session)

@router.get('/{segment_id}', response_model=SegmentOutWithSensors)
def get_segment_by_id(*, session: Session = Depends(get_session), segment_id: int):
    return crud.get_segment_by_id(session, segment_id)

@router.post('', status_code=status.HTTP_201_CREATED, response_model=SegmentDb)
def create_segment(*, session: Session = Depends(get_session), segment_in: SegmentIn):
    return crud.create_segment(session, segment_in)

@router.patch('/{segment_id}', response_model=SegmentDb)
def update_segment_by_id(*, session: Session = Depends(get_session), segment_id:int, segment_update: SegmentUpdate):
    return crud.update_segment_by_id(session, segment_id, segment_update)

@router.delete('/{segment_id}', response_model=SegmentDb)
def delete_segment_by_id(*, session: Session = Depends(get_session), segment_id: int):
    return crud.delete_segment_by_id(session, segment_id)