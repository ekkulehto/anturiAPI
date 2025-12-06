from fastapi import HTTPException, Response, status
from sqlmodel import Session, select

from ..measurements.schemas import MeasurementFilterForGetSegmentById

from .schemas import SegmentUpdate
from ..models import (
    SegmentIn, 
    SegmentDb,
    SegmentOutWithNumberOfSensors, 
    SegmentOutWithSensors, 
    MeasurementDb, 
    MeasurementOut,
    SensorOutInSegmentWithMeasurements,
    SensorOutWithMeasurements, 
)

# =================================================================================
#    GET ALL SEGMENTS
# =================================================================================

def get_all_segments(session: Session):
    segments_db = session.exec(select(SegmentDb)).all()

    return [
        SegmentOutWithNumberOfSensors(
            id=segment.id,
            name= segment.name,
            number_of_sensors=len(segment.sensors)
        )
        for segment in segments_db
    ]

# =================================================================================
#    CREATE NEW SEGMENT
# =================================================================================

def create_segment(session: Session, segment_in: SegmentIn):
    segment = SegmentDb.model_validate(segment_in)
    session.add(segment)
    session.commit()
    session.refresh(segment)
    return segment

# =================================================================================
#    GET SEGMENT BY ID
# =================================================================================

def get_segment_by_id(session: Session, segment_id: int, filters: MeasurementFilterForGetSegmentById):
    segment = session.get(SegmentDb, segment_id)

    if not segment:
        raise HTTPException(
            detail='Segment not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )

    sensors_out: list[SensorOutWithMeasurements] = []

    for sensor in segment.sensors:
        query = select(MeasurementDb).where(MeasurementDb.sensor_id == sensor.id)

        if filters.measurement_type is not None:
            query = query.where(MeasurementDb.type == filters.measurement_type)

        if filters.since is not None:
            query = query.where(MeasurementDb.timestamp >= filters.since)

        if filters.until is not None:
            query = query.where(MeasurementDb.timestamp <= filters.until)

        query = (
            query
            .order_by(MeasurementDb.timestamp.desc())
            .limit(filters.limit)
        )

        measurements_db = session.exec(query).all()

        measurements_out = [
            MeasurementOut(
                id=measurement.id,
                value=measurement.value,
                unit=measurement.unit,
                type=measurement.type,
                timestamp=measurement.timestamp,
            )
            for measurement in measurements_db
        ]

        sensors_out.append(
            SensorOutInSegmentWithMeasurements(
                id=sensor.id,
                name=sensor.name,
                status=sensor.status,
                measurements=measurements_out,
            )
        )

    return SegmentOutWithSensors(
        id=segment.id,
        name=segment.name,
        sensors=sensors_out,
    )

# =================================================================================
#    UPDATE SEGMENT BY ID
# =================================================================================

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

# =================================================================================
#    DELETE SEGMENT BY ID
# =================================================================================

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