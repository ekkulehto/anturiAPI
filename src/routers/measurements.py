from fastapi import APIRouter, status, Depends
from sqlmodel import Session

from ..database.database import get_session
from ..database import measurements_crud as crud
from ..database.models import MeasurementIn, MeasurementOutWithSensor

router = APIRouter(prefix='/measurements', tags=['Measurements'])

@router.get('', response_model=list[MeasurementOutWithSensor])
def get_all_measurements(*, session: Session = Depends(get_session)):
    return crud.get_all_measurements(session)

@router.post('', status_code=status.HTTP_201_CREATED, response_model=MeasurementOutWithSensor)
def create_measurement(*, session: Session = Depends(get_session), measurement_in: MeasurementIn):
    return crud.create_measurement(session, measurement_in)

@router.get('/{measurement_id}', response_model=MeasurementOutWithSensor)
def get_measurement_by_id(*, session: Session = Depends(get_session), measurement_id: int):
    return crud.get_measurement_by_id(session, measurement_id)

@router.delete('/{measurement_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement_by_id(*, session: Session = Depends(get_session), measurement_id: int):
    return crud.delete_measurement_by_id(session, measurement_id)