from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.schemas.sensors import SensorStatusUpdate, SensorUpdate
from ..schemas.filters import MeasurementFilter
from .models import (
    MeasurementDb, 
    MeasurementOut, 
    SegmentDb, 
    SensorIn, 
    SensorDb,
    SensorOutWithMeasurements, 
    SensorOutWithStatusHistory, 
    SensorStatus, 
    SensorStatusDb, 
    SensorStatusOut
)

def get_all_sensors(session: Session, sensor_status: SensorStatus | None = None):
    query = select(SensorDb)

    if sensor_status is not None:
        query = query.where(SensorDb.status == sensor_status)

    return session.exec(query).all()

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

def get_sensor_by_id(session: Session, sensor_id: int, filters: MeasurementFilter):
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

    if filters.since is None and filters.until is None:
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

def delete_sensor_by_id(session: Session, sensor_id: int):
    sensor = session.get(SensorDb, sensor_id)

    if not sensor:
        raise HTTPException(
            detail='Sensor not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    session.delete(sensor)
    session.commit()

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