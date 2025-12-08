from fastapi import HTTPException, status
from sqlmodel import Session, select

from ..measurements.schemas import MeasurementFilterForGetSensorById

from ..models import (
    MeasurementIn, 
    MeasurementDb, 
    MeasurementOut, 
    MeasurementOutWithSensor,
    SensorDb,
    SensorOutWithMeasurements,
    SensorStatus
)

# =================================================================================
#    GET SENSOR MEASUREMENTS BY ID
# =================================================================================

def get_sensor_measurements_by_id(session: Session, sensor_id: int, filters: MeasurementFilterForGetSensorById):
    sensor = session.get(SensorDb, sensor_id)

    if not sensor:
        raise HTTPException(
            detail='Sensor not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    query = select(MeasurementDb).where(MeasurementDb.sensor_id == sensor_id)

    if filters.measurement_type is not None:
        query = query.where(MeasurementDb.type == filters.measurement_type)
        
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
#    CREATE NEW MEASUREMENT
# =================================================================================

def create_measurement(session: Session, measurement_in: MeasurementIn):
    sensor = session.get(SensorDb, measurement_in.sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail='Sensor not found.',
        )

    if sensor.status == SensorStatus.ERROR:
        raise HTTPException(
            status_code=400,
            detail='Sensor is in ERROR state and must not send measurements.'
        )
    
    payload = measurement_in.measurement

    measurement = MeasurementDb(
        sensor_id=measurement_in.sensor_id,
        timestamp=payload.timestamp,
        type=payload.type,
        unit=payload.unit,
        value=payload.value,
    )

    session.add(measurement)
    session.commit()
    session.refresh(measurement)

    return MeasurementOutWithSensor(
        sensor_id=measurement_in.sensor_id,
        measurement=MeasurementOut(
            id=measurement.id,
            type=payload.type,
            unit=payload.unit,
            value=payload.value,
            timestamp=payload.timestamp,
        ),
    )

# =================================================================================
#    GET MEASUREMENT BY ID
# =================================================================================

def get_measurement_by_id(session: Session, measurement_id: int):
    measurement = session.get(MeasurementDb, measurement_id)

    if not measurement:
        raise HTTPException(
            detail='Measurement not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return MeasurementOutWithSensor(
            sensor_id=measurement.sensor_id,
            measurement=MeasurementOut(
                id=measurement.id,
                type=measurement.type,
                unit=measurement.unit,
                value=measurement.value,
                timestamp=measurement.timestamp,
            )
        )

# =================================================================================
#    DELETE MEASUREMENT BY ID
# =================================================================================

def delete_measurement_by_id(session: Session, measurement_id: int):
    measurement = session.get(MeasurementDb, measurement_id)

    if not measurement:
        raise HTTPException(
            detail='Measurement not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    session.delete(measurement)
    session.commit()