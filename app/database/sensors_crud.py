from datetime import datetime, timezone
from fastapi import HTTPException, Response, status
from sqlmodel import Session, select

from ..schemas.filters import MeasurementFilter
from .models import MeasurementDb, MeasurementOut, SegmentDb, SensorIn, SensorDb, SensorOutWithMeasurements, SensorStatus, SensorStatusDb

def create_sensor(session: Session, sensor_in: SensorIn):
    segment = session.get(SegmentDb, sensor_in.segment_id)

    if not segment:
        raise HTTPException(
            detail='Segment not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    new_sensor = SensorDb.model_validate(sensor_in)

    sensor_status = SensorStatusDb(status=SensorStatus.NORMAL ,sensor=new_sensor)
    
    session.add(new_sensor)
    session.add(sensor_status)
    session.commit()
    session.refresh(new_sensor)

    return new_sensor

def get_all_sensors(session: Session):
    return session.exec(select(SensorDb)).all()

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
        measurements=measurements_out
    )

def delete_sensor_by_id(session: Session, sensor_id: int):
    sensor = session.get(SensorDb, sensor_id)

    if not sensor:
        raise HTTPException(
            detail='Sensor not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    session.delete(sensor)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)