from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.sensor_status.router import change_sensor_status_by_id
from src.sensor_status.schemas import SensorStatusUpdate

from .schemas import SensorUpdate
from ..measurements.schemas import MeasurementFilterForGetSensorById
from ..models import (
    SensorIn, 
    SensorDb,
    SensorOutWithMeasurements, 
    SensorStatus, 
    MeasurementDb, 
    MeasurementOut, 
    SegmentDb, 
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
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    new_sensor = SensorDb.model_validate(sensor_in)
    session.add(new_sensor)
    session.commit()
    session.refresh(new_sensor)

    change_sensor_status_by_id(
        session=session,
        sensor_id=new_sensor.id,
        sensor_status_update=SensorStatusUpdate(status=SensorStatus.NORMAL)
    )

    session.refresh(new_sensor)

    return new_sensor

# =================================================================================
#    GET SENSOR BY ID
# =================================================================================

def get_sensor_by_id(session: Session, sensor_id: int, filters: MeasurementFilterForGetSensorById):
    sensor = session.get(SensorDb, sensor_id)

    if not sensor:
        raise HTTPException(
            detail='Sensor not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    query = select(MeasurementDb).where(MeasurementDb.sensor_id == sensor_id)

    if filters.since is not None:
        query = query.where(MeasurementDb.timestamp >= filters.since)
    
    if filters.until is not None:
        query = query.where(MeasurementDb.timestamp <= filters.until)
    
    query = query.order_by(MeasurementDb.timestamp.desc())

    query = query.limit(filters.limit)
    
    measurements_db = session.exec(query).all()
    measurements_out = [MeasurementOut.model_validate(measurement) for measurement in measurements_db]

    return SensorOutWithMeasurements(
        id=sensor_id,
        name=sensor.name,
        status=sensor.status,
        segment=sensor.segment,
        measurements=measurements_out
    )

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
    
    if sensor_update.name is not None:
        sensor.name = sensor_update.name
    
    if sensor_update.segment_id is not None:
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