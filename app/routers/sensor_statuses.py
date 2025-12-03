from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from ..database.database import get_session

from ..database import sensor_statuses_crud as crud
from ..database.models import SensorStatusIn, SensorStatusDb

router = APIRouter(prefix='/segments', tags=['segments'])

@router.get('', response_model=list[SensorStatusDb])
def get_all_sensor_statuses(*, session: Session = Depends(get_session)):
    return crud.get_all_sensor_statuses(session)

@router.get('/{sensor_id}', response_model=SensorStatusDb)
def get_sensor_status_by_id(*, session: Session = Depends(get_session), sensor_status_id: int):
    return crud.get_sensor_status_by_id(session, sensor_status_id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=SensorStatusDb)
def create_sensor_status(*, session: Session = Depends(get_session), sensor_status_in: SensorStatusIn):
    return crud.create_sensor_status(session, sensor_status_in)

@router.delete("/{pub_id}", response_model=SensorStatusDb)
def delete_sensor_status_by_id(*, session: Session = Depends(get_session), sensor_status_id: int):
    return crud.delete_sensor_status_by_id(session, sensor_status_id)