from fastapi import HTTPException, Response, status
from sqlmodel import Session, select
from .models import SegmentIn, SegmentDb

def create_segment(session: Session, segment_in: SegmentIn):
    segment = SegmentDb.model_validate(segment_in)
    session.add(segment)
    session.commit()
    session.refresh(segment)
    return segment

def get_all_segments(session: Session):
    return session.exec(select(SegmentDb)).all()

def get_segment_by_id(session: Session, segment_id: int):
    segment = session.get(SegmentDb, segment_id)

    if not segment:
        raise HTTPException(
            detail='Segment not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return segment

def delete_segment_by_id(session: Session, segment_id: int):
    segment = session.get(SegmentDb, segment_id)

    if not segment:
        raise HTTPException(
            detail='Segment not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    session.delete(segment)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)