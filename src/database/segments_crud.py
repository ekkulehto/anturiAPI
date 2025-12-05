from fastapi import HTTPException, Response, status
from sqlmodel import Session, select

from app.schemas.segments import SegmentUpdate
from .models import (
    MeasurementDb, 
    MeasurementOut, 
    SegmentIn, 
    SegmentDb, 
    SegmentOutWithSensors, 
    SensorOutWithLastMeasurement
)

def get_all_segments(session: Session):
    return session.exec(select(SegmentDb)).all()

def create_segment(session: Session, segment_in: SegmentIn):
    segment = SegmentDb.model_validate(segment_in)
    session.add(segment)
    session.commit()
    session.refresh(segment)
    return segment

def get_segment_by_id(session: Session, segment_id: int):
    segment = session.get(SegmentDb, segment_id)

    if not segment:
        raise HTTPException(
            detail='Segment not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    sensors_out: list[SensorOutWithLastMeasurement] = []

    for sensor in segment.sensors:
        query = (
            select(MeasurementDb)
            .where(MeasurementDb.sensor_id == sensor.id)
            .order_by(MeasurementDb.timestamp.desc())
            .limit(1)
        )

        last_measurement_db = session.exec(query).first()

        if last_measurement_db is not None:
            last_measurement_out = MeasurementOut.model_validate(last_measurement_db)
        else:
            last_measurement_out = None
        
        sensors_out.append(SensorOutWithLastMeasurement(
            id=sensor.id,
            name=sensor.name,
            status=sensor.status,
            last_measurement=last_measurement_out
        ))
    
    return SegmentOutWithSensors(
        id=segment.id,
        name=segment.name,
        sensors=sensors_out
    )

def update_segment_by_id(session: Session, segment_id: int, segment_update: SegmentUpdate):
    segment = session.get(SegmentDb, segment_id)

    if not segment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Segment not found'
        )
    
    if segment_update.name is not None:
        segment.name = segment_update.name
    
    session.add(segment)
    session.commit()
    session.refresh(segment)
    return segment

def delete_segment_by_id(session: Session, segment_id: int):
    segment = session.get(SegmentDb, segment_id)

    if not segment:
        raise HTTPException(
            detail='Segment not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    if segment.sensors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Segment cannot be deleted while it still has sensors'
        )
    
    session.delete(segment)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)