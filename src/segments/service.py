from fastapi import HTTPException, Response, status
from sqlmodel import Session, select

from .schemas import SegmentUpdate
from ..models import (
    SegmentIn, 
    SegmentDb,
    SegmentOutWithNumberOfSensors, 
    SegmentOutWithSensors, 
    MeasurementDb, 
    MeasurementOut,
    SensorOutInSegmentWithLastMeasurement,
    SensorStatus, 
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

def get_segment_by_id(session: Session, segment_id: int, sensor_status: SensorStatus | None = None):
    segment = session.get(SegmentDb, segment_id)

    if not segment:
        raise HTTPException(
            detail="Segment not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    sensors_out: list[SensorOutInSegmentWithLastMeasurement] = []

    for sensor in segment.sensors:
        if sensor_status is not None and sensor.status != sensor_status:
            continue

        query = (
            select(MeasurementDb)
            .where(MeasurementDb.sensor_id == sensor.id)
            .order_by(MeasurementDb.timestamp.desc())
            .limit(1)
        )

        last_measurement_db = session.exec(query).first()

        if last_measurement_db is not None:
            last_measurement = MeasurementOut(
                id=last_measurement_db.id,
                value=last_measurement_db.value,
                unit=last_measurement_db.unit,
                type=last_measurement_db.type,
                timestamp=last_measurement_db.timestamp,
            )
        else:
            last_measurement = None

        sensors_out.append(
            SensorOutInSegmentWithLastMeasurement(
                id=sensor.id,
                name=sensor.name,
                status=sensor.status,
                last_measurement=last_measurement,
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
    
    if segment_update.name is None or segment_update.name == segment.name:
        return segment
    
    segment.name = segment_update.name
    
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