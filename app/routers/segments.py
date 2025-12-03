from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from ..database.database import get_session

from ..database import segments_crud as crud
from ..database.models import SegmentIn, SegmentDb

router = APIRouter(prefix='/segments', tags=['segments'])

@router.get('', response_model=list[SegmentDb])
def get_all_segments(*, session: Session = Depends(get_session)):
    return crud.get_all_segments(session)

@router.get('/{sensor_id}', response_model=SegmentDb)
def get_segment_by_id(*, session: Session = Depends(get_session), segment_id: int):
    return crud.get_segment_by_id(session, segment_id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=SegmentDb)
def create_segment(*, session: Session = Depends(get_session), segment_in: SegmentIn):
    return crud.create_segment(session, segment_in)

@router.delete("/{pub_id}", response_model=SegmentDb)
def delete_segment_by_id(*, session: Session = Depends(get_session), segment_id: int):
    return crud.delete_segment_by_id(session, segment_id)