from typing import Annotated
from fastapi import APIRouter, Path, Query, status, Depends
from sqlmodel import Session

from ..sensor_measurements.schemas import MeasurementFilterForGetSensorById

from ..database import get_session
from ..sensor_measurements import service as crud
from ..models import MeasurementIn, MeasurementOutWithSensor, SensorOutWithMeasurements

from .docs import (
    GET_SENSOR_MEASUREMENTS_BY_ID_SUMMARY, 
    GET_SENSOR_MEASUREMENTS_BY_ID_DESCRIPTION,
    CREATE_MEASUREMENT_SUMMARY,
    CREATE_MEASUREMENT_DESCRIPTION,
    GET_MEASUREMENT_BY_ID_SUMMARY,
    GET_MEASUREMENT_BY_ID_DESCRIPTION,
    DELETE_MEASUREMENT_BY_ID_SUMMARY,
    DELETE_MEASUREMENT_BY_ID_DESCRIPTION
)

router = APIRouter(prefix='/sensors', tags=['Sensor Measurements'])

# =================================================================================
#    GET SENSOR'S MEASUREMENTS BY ID
# =================================================================================

@router.get(
        '/{sensor_id}/measurements', 
        response_model=SensorOutWithMeasurements,
        summary=GET_SENSOR_MEASUREMENTS_BY_ID_SUMMARY,
        description=GET_SENSOR_MEASUREMENTS_BY_ID_DESCRIPTION
)
def get_sensor_by_id(
    *, session: Session = Depends(get_session), 
    sensor_id: int = Path(..., description='Unique identifier of the sensor whose measurements to retrieve'), 
    filters: Annotated[MeasurementFilterForGetSensorById, Query()]
):
    return crud.get_sensor_measurements_by_id(session, sensor_id, filters)

# =================================================================================
#    CREATE NEW MEASUREMENT
# =================================================================================

@router.post(
        '/{sensor_id}/measurements', 
        status_code=status.HTTP_201_CREATED, 
        response_model=MeasurementOutWithSensor,
        summary=CREATE_MEASUREMENT_SUMMARY,
        description=CREATE_MEASUREMENT_DESCRIPTION
)
def create_measurement(
    *, 
    session: Session = Depends(get_session),
    sensor_id: int = Path(..., description='Unique identifier of the sensor whose measurements to create'),  
    measurement_in: MeasurementIn
):
    return crud.create_measurement(session, sensor_id, measurement_in)

# =================================================================================
#    GET MEASUREMENT BY ID
# =================================================================================

@router.get(
        '/{sensor_id}/measurements/{measurement_id}', 
        response_model=MeasurementOutWithSensor,
        summary=GET_MEASUREMENT_BY_ID_SUMMARY,
        description=GET_MEASUREMENT_BY_ID_DESCRIPTION
)
def get_measurement_by_id(
    *, 
    session: Session = Depends(get_session), 
    sensor_id: int = Path(..., description='Unique identifier of the sensor whose measurement to retrieve'),
    measurement_id: int = Path(..., description='Unique identifier of the measurement to retrieve'),
):
    return crud.get_measurement_by_id(session, sensor_id, measurement_id)

# =================================================================================
#    DELETE MEASUREMENT BY ID
# =================================================================================

@router.delete(
        '/{sensor_id}/measurements/{measurement_id}', 
        status_code=status.HTTP_204_NO_CONTENT,
        summary=DELETE_MEASUREMENT_BY_ID_SUMMARY,
        description=DELETE_MEASUREMENT_BY_ID_DESCRIPTION
)
def delete_measurement_by_id(
    *, 
    session: Session = Depends(get_session), 
    sensor_id: int = Path(..., description='Unique identifier of the sensor whose measurement to delete'),
    measurement_id: int = Path(..., description='Unique identifier of the measurement to delete'),
):
    return crud.delete_measurement_by_id(session, sensor_id, measurement_id)