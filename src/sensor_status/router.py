from fastapi import APIRouter, Path, Query, status, Depends
from sqlmodel import Session

from ..database import get_session
from .schemas import SensorStatusUpdate
from ..sensor_status import service as crud
from ..models import (
    SensorOut, 
    SensorOutWithStatusHistory, 
    SensorStatus
)

from .docs import (
    GET_SENSOR_STATUS_HISTORY_BY_ID_SUMMARY,
    GET_SENSOR_STATUS_HISTORY_BY_ID_DESCRIPTION,
    GET_SENSOR_STATUS_HISTORY_BY_ID_FILTER_DESCRIPTION,
    CHANGE_SENSOR_STATUS_BY_ID_SUMMARY,
    CHANGE_SENSOR_STATUS_BY_ID_DESCRIPTION,
)

router = APIRouter(prefix='/sensors', tags=['Sensor Status'])

# =================================================================================
#    GET SENSOR STATUS HISTORY BY ID
# =================================================================================

@router.get(
        '/{sensor_id}/status/history', 
        response_model=SensorOutWithStatusHistory,
        summary=GET_SENSOR_STATUS_HISTORY_BY_ID_SUMMARY,
        description=GET_SENSOR_STATUS_HISTORY_BY_ID_DESCRIPTION
)
def get_sensor_status_history_by_id(
    *, 
    session: Session = Depends(get_session), 
    sensor_id: int = Path(..., description='Unique identifier of the sensor whose status history to retrieve'),
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
    sensor_id: int = Path(..., description='Unique identifier of the sensor whose status to update'), 
    sensor_status_update: SensorStatusUpdate
):
    return crud.change_sensor_status_by_id(session, sensor_id, sensor_status_update)

