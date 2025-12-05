from typing import Annotated
from fastapi import APIRouter, Query, status, Depends
from sqlmodel import Session

from app.schemas.sensors import SensorStatusUpdate, SensorUpdate

from ..schemas.filters import MeasurementFilter
from ..database.database import get_session

from ..database import sensors_crud as crud
from ..database.models import SensorIn, SensorDb, SensorOut, SensorOutWithMeasurements, SensorOutWithStatusHistory, SensorStatus, SensorStatusOut

router = APIRouter(prefix='/sensors', tags=['Sensors'])

@router.get('', response_model=list[SensorOut])
def get_all_sensors(*, session: Session = Depends(get_session), sensor_status: SensorStatus | None = Query(
    default=None,
    description='Filter sensors by current status'
)):
    return crud.get_all_sensors(session, sensor_status)

@router.get('/{sensor_id}', response_model=SensorOutWithMeasurements)
def get_sensor_by_id(*, session: Session = Depends(get_session), sensor_id: int, filters: Annotated[MeasurementFilter, Query()]):
    return crud.get_sensor_by_id(session, sensor_id, filters)

@router.get('/{sensor_id}/status_history', response_model=SensorOutWithStatusHistory)
def get_sensor_status_history_by_id(*, session: Session = Depends(get_session), sensor_id: int, sensor_status: SensorStatus | None = Query(
    default=None,
    description='Filter sensor status history by status'
)):
    return crud.get_sensor_status_history_by_id(session, sensor_id, sensor_status)

@router.post('/{sensor_id}/status', response_model=SensorOut, status_code=status.HTTP_202_ACCEPTED)
def change_sensor_status(*, session: Session = Depends(get_session), sensor_id: int, sensor_status_update: SensorStatusUpdate):
    return crud.change_sensor_status(session, sensor_id, sensor_status_update)

@router.post('', status_code=status.HTTP_201_CREATED, response_model=SensorOut)
def create_sensor(*, session: Session = Depends(get_session), sensor_in: SensorIn):
    return crud.create_sensor(session, sensor_in)

@router.patch('/{sensor_id}', response_model=SensorOut)
def update_sensor_by_id(*, session: Session = Depends(get_session), sensor_id: int, sensor_update: SensorUpdate):
    return crud.update_sensor_by_id(session, sensor_id, sensor_update)

@router.delete('/{sensor_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor_by_id(*, session: Session = Depends(get_session), sensor_id: int):
    return crud.delete_sensor_by_id(session, sensor_id)