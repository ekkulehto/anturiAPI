from fastapi import HTTPException, status
from sqlmodel import Session, select

from .schemas import SensorUpdate
from ..models import (
    SensorIn, 
    SensorDb,
    SensorStatus, 
    SegmentDb,
    SensorStatusDb, 
)

# =================================================================================
#    GET ALL SENSORS
# =================================================================================

def get_all_sensors(session: Session, sensor_status: SensorStatus | None = None):
    query = select(SensorDb)

    if sensor_status is not None:
        query = query.where(SensorDb.status == sensor_status)

    return session.exec(query).all()

# =================================================================================
#    CREATE NEW SENSOR
# =================================================================================

def create_sensor(session: Session, sensor_in: SensorIn):
    segment = session.get(SegmentDb, sensor_in.segment_id)

    if not segment:
        raise HTTPException(
            detail='Segment not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )
    
    new_sensor = SensorDb.model_validate(sensor_in)

    new_sensor.status = SensorStatus.NORMAL

    session.add(new_sensor)
    session.commit()
    session.refresh(new_sensor)

    first_status = SensorStatusDb(
        status=SensorStatus.NORMAL,
        sensor=new_sensor,
    )
    
    session.add(first_status)
    session.commit()
    session.refresh(new_sensor)

    return new_sensor

# =================================================================================
#    GET SENSOR BY ID
# =================================================================================

def get_sensor_by_id(session: Session, sensor_id: int):
    sensor = session.get(SensorDb, sensor_id)

    if not sensor:
        raise HTTPException(
            detail='Sensor not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return SensorDb.model_validate(sensor)

# =================================================================================
#    UPDATE SENSOR BY ID
# =================================================================================

def update_sensor_by_id(session: Session, sensor_id: int, sensor_update: SensorUpdate):
    sensor = session.get(SensorDb, sensor_id)

    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Sensor not found'
        )
    
    name_changed = (
        sensor_update.name is not None
        and sensor_update.name != sensor.name
    )

    segment_changed = (
        sensor_update.segment_id is not None
        and sensor_update.segment_id != sensor.segment_id
    )

    if not name_changed and not segment_changed:
        return sensor
    
    if name_changed:
        sensor.name = sensor_update.name
    
    if segment_changed:
        new_segment = session.get(SegmentDb, sensor_update.segment_id)

        if not new_segment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Segment not found'
            )

        sensor.segment_id = sensor_update.segment_id
    
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor

# =================================================================================
#    DELETE SENSOR BY ID
# =================================================================================

def delete_sensor_by_id(session: Session, sensor_id: int):
    sensor = session.get(SensorDb, sensor_id)

    if not sensor:
        raise HTTPException(
            detail='Sensor not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    session.delete(sensor)
    session.commit()