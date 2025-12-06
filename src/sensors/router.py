from typing import Annotated
from fastapi import APIRouter, Query, status, Depends
from sqlmodel import Session

from ..database import get_session
from .schemas import SensorStatusUpdate, SensorUpdate
from ..measurements.schemas import MeasurementFilterForGetSensorById
from ..sensors import service as crud
from ..models import (
    SensorIn, 
    SensorOut, 
    SensorOutWithMeasurements, 
    SensorOutWithStatusHistory, 
    SensorStatus
)

from .docs import (
    GET_ALL_SENSORS_SUMMARY,
    GET_ALL_SENSORS_DESCRIPTION,
    GET_ALL_SENSORS_STATUS_FILTER_DESCRIPTION,
    CREATE_SENSOR_SUMMARY,
    CREATE_SENSOR_DESCRIPTION,
    GET_SENSOR_BY_ID_SUMMARY,
    GET_SENSOR_BY_ID_DESCRIPTION,
    UPDATE_SENSOR_BY_ID_SUMMARY,
    UPDATE_SENSOR_BY_ID_DESCRIPTION,
    DELETE_SENSOR_BY_ID_SUMMARY,
    DELETE_SENSOR_BY_ID_DESCRIPTION,
    GET_SENSOR_STATUS_HISTORY_BY_ID_SUMMARY,
    GET_SENSOR_STATUS_HISTORY_BY_ID_DESCRIPTION,
    GET_SENSOR_STATUS_HISTORY_BY_ID_FILTER_DESCRIPTION,
    CHANGE_SENSOR_STATUS_BY_ID_SUMMARY,
    CHANGE_SENSOR_STATUS_BY_ID_DESCRIPTION,
)

router = APIRouter(prefix='/sensors', tags=['Sensors'])

# =================================================================================
#    GET ALL SENSORS
# =================================================================================

@router.get(
        '', 
        response_model=list[SensorOut],
        summary=GET_ALL_SENSORS_SUMMARY,
        description=GET_ALL_SENSORS_DESCRIPTION
)
def get_all_sensors(
    *, 
    session: Session = Depends(get_session), 
    sensor_status: SensorStatus | None = Query(
    default=None,
    description=GET_ALL_SENSORS_STATUS_FILTER_DESCRIPTION
)):
    return crud.get_all_sensors(session, sensor_status)

# =================================================================================
#    CREATE NEW SENSOR
# =================================================================================

@router.post(
        '', 
        status_code=status.HTTP_201_CREATED, 
        response_model=SensorOut,
        summary=CREATE_SENSOR_SUMMARY,
        description=CREATE_SENSOR_DESCRIPTION
)
def create_sensor(
    *, 
    session: Session = Depends(get_session), 
    sensor_in: SensorIn
):
    return crud.create_sensor(session, sensor_in)

# =================================================================================
#    GET SENSOR BY ID
# =================================================================================

@router.get(
        '/{sensor_id}', 
        response_model=SensorOutWithMeasurements,
        summary=GET_SENSOR_BY_ID_SUMMARY,
        description=GET_SENSOR_BY_ID_DESCRIPTION
)
def get_sensor_by_id(
    *, session: Session = Depends(get_session), 
    sensor_id: int, 
    filters: Annotated[MeasurementFilterForGetSensorById, Query()]
):
    return crud.get_sensor_by_id(session, sensor_id, filters)

# =================================================================================
#    UPDATE SENSOR BY ID
# =================================================================================

@router.patch(
        '/{sensor_id}', 
        response_model=SensorOut,
        summary=UPDATE_SENSOR_BY_ID_SUMMARY,
        description=UPDATE_SENSOR_BY_ID_DESCRIPTION
)
def update_sensor_by_id(
    *, 
    session: Session = Depends(get_session), 
    sensor_id: int, 
    sensor_update: SensorUpdate
):
    return crud.update_sensor_by_id(session, sensor_id, sensor_update)

# =================================================================================
#    DELETE SENSOR BY ID
# =================================================================================

@router.delete(
        '/{sensor_id}', 
        status_code=status.HTTP_204_NO_CONTENT,
        summary=DELETE_SENSOR_BY_ID_SUMMARY,
        description=DELETE_SENSOR_BY_ID_DESCRIPTION
)
def delete_sensor_by_id(
    *, 
    session: Session = Depends(get_session), 
    sensor_id: int
):
    return crud.delete_sensor_by_id(session, sensor_id)

# =================================================================================
#    GET SENSOR STATUS HISTORY BY ID
# =================================================================================

@router.get(
        '/{sensor_id}/status_history', 
        response_model=SensorOutWithStatusHistory,
        summary=GET_SENSOR_STATUS_HISTORY_BY_ID_SUMMARY,
        description=GET_SENSOR_STATUS_HISTORY_BY_ID_DESCRIPTION
)
def get_sensor_status_history_by_id(
    *, 
    session: Session = Depends(get_session), 
    sensor_id: int, 
    sensor_status: SensorStatus | None = Query(
    default=None,
    description=GET_SENSOR_STATUS_HISTORY_BY_ID_FILTER_DESCRIPTION
)):
    return crud.get_sensor_status_history_by_id(session, sensor_id, sensor_status)

# =================================================================================
#    CHANGE SENSOR STATUS BY ID
# =================================================================================

@router.post(
        '/{sensor_id}/status', 
        response_model=SensorOut, 
        status_code=status.HTTP_202_ACCEPTED,
        summary=CHANGE_SENSOR_STATUS_BY_ID_SUMMARY,
        description=CHANGE_SENSOR_STATUS_BY_ID_DESCRIPTION
)
def change_sensor_status_by_id(
    *, 
    session: Session = Depends(get_session), 
    sensor_id: int, 
    sensor_status_update: SensorStatusUpdate
):
    return crud.change_sensor_status_by_id(session, sensor_id, sensor_status_update)

