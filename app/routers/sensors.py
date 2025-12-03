from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from ..database.database import get_session

from ..database import sensors_crud as crud
from ..database.models import SensorIn, SensorDb

router = APIRouter(prefix='/sensors', tags=['sensors'])

@router.get('', response_model=list[SensorDb])
def get_all_sensors(*, session: Session = Depends(get_session)):
    return crud.get_all_sensors(session)

@router.get('/{sensor_id}', response_model=SensorDb)
def get_sensor_by_id(*, session: Session = Depends(get_session), sensor_id: int):
    return crud.get_sensor_by_id(session, sensor_id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=SensorDb)
def create_sensor(*, session: Session = Depends(get_session), sensor_in: SensorIn):
    return crud.create_sensor(session, sensor_in)

@router.delete("/{pub_id}", response_model=SensorDb)
def delete_sensor_by_id(*, session: Session = Depends(get_session), sensor_id: int):
    return crud.delete_sensor_by_id(session, sensor_id)