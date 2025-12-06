from fastapi import HTTPException, status
from sqlmodel import Session, select

from ..models import (
    MeasurementIn, 
    MeasurementDb, 
    MeasurementOut, 
    MeasurementOutWithSensor,
    MeasurementType,
    SensorDb,
    SensorStatus
)

# =================================================================================
#    GET ALL SEGMENTS
# =================================================================================

def get_all_measurements(session: Session, measurement_type: MeasurementType | None = None):
    query = select(MeasurementDb)

    if measurement_type is not None:
        query = query.where(MeasurementDb.type == measurement_type)

    measurements_db = session.exec(query).all()

    return [
        MeasurementOutWithSensor(
            sensor_id=measurement.sensor_id,
            measurement=MeasurementOut(
                id=measurement.id,
                type=measurement.type,
                unit=measurement.unit,
                value=measurement.value,
                timestamp=measurement.timestamp
            )
        )
        for measurement in measurements_db
    ]

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