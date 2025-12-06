from fastapi import HTTPException, status
from sqlmodel import Session, select

from ..models import (
    MeasurementIn, 
    MeasurementDb, 
    MeasurementOut, 
    MeasurementOutWithSensor
)

# =================================================================================
#    GET ALL SEGMENTS
# =================================================================================

def get_all_measurements(session: Session):
    measurements_db = session.exec(select(MeasurementDb)).all()

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