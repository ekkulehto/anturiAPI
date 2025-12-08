from fastapi import HTTPException, status
from sqlmodel import Session, select

from .schemas import SensorStatusUpdate
from ..models import (
    SensorDb,
    SensorOutWithStatusHistory, 
    SensorStatus, 
    SensorStatusDb, 
    SensorStatusOut,
)

# =================================================================================
#    GET SENSOR STATUS HISTORY BY ID
# =================================================================================

def get_sensor_status_history_by_id(session: Session, sensor_id: int, sensor_status: SensorStatus | None = None):
    sensor = session.get(SensorDb, sensor_id)

    if not sensor:
        raise HTTPException(
            detail='Sensor not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    query = select(SensorStatusDb).where(SensorStatusDb.sensor_id == sensor_id)
    query = query.order_by(SensorStatusDb.timestamp.desc())
    
    if sensor_status is not None:
        query = query.where(SensorStatusDb.status == sensor_status)

    sensor_status_db = session.exec(query).all()
    sensor_status_out = [SensorStatusOut.model_validate(status) for status in sensor_status_db]

    return SensorOutWithStatusHistory(
        id=sensor_id,
        name=sensor.name,
        segment=sensor.segment,
        status_history=sensor_status_out,
    )

# =================================================================================
#    CHANGE SENSOR STATUS BY ID
# =================================================================================

def change_sensor_status_by_id(session: Session, sensor_id: int, sensor_status_update: SensorStatusUpdate):
    existing_sensor = session.get(SensorDb, sensor_id)

    if not existing_sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Sensor not found'
        )
    
    sensor_status_db = SensorStatusDb(
        status=sensor_status_update.status,
        sensor=existing_sensor
    )

    session.add(sensor_status_db)

    existing_sensor.status = sensor_status_update.status
    session.add(existing_sensor)
    session.commit()
    session.refresh(existing_sensor)

    return existing_sensor