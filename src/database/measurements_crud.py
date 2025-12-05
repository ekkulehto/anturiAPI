from fastapi import HTTPException, status
from sqlmodel import Session, select

from .models import (
    MeasurementIn, 
    MeasurementDb, 
    MeasurementOut, 
    MeasurementOutWithSensor
)

def get_all_measurements(session: Session):
    measurements_db = session.exec(select(MeasurementDb)).all()

    return [
        MeasurementOutWithSensor(
            sensor_id=measurement.sensor_id,
            measurement=MeasurementOut.model_validate(measurement)
        )
        for measurement in measurements_db
    ]

def create_measurement(session: Session, measurement_in: MeasurementIn):
    measurement = MeasurementDb.model_validate(measurement_in)
    session.add(measurement)
    session.commit()
    session.refresh(measurement)

    return MeasurementOutWithSensor(
        sensor_id=measurement.sensor_id,
        measurement=MeasurementOut.model_validate(measurement)
        )

def get_measurement_by_id(session: Session, measurement_id: int):
    measurement = session.get(MeasurementDb, measurement_id)

    if not measurement:
        raise HTTPException(
            detail='Measurement not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return MeasurementOutWithSensor(
        sensor_id=measurement.sensor_id,
        measurement=MeasurementOut.model_validate(measurement)
        )

def delete_measurement_by_id(session: Session, measurement_id: int):
    measurement = session.get(MeasurementDb, measurement_id)

    if not measurement:
        raise HTTPException(
            detail='Measurement not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    session.delete(measurement)
    session.commit()