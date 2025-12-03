from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from ..database.database import get_session

from ..database import measurements_crud as crud
from ..database.models import MeasurementIn, MeasurementDb

router = APIRouter(prefix='/measurements', tags=['measurements'])

@router.get('', response_model=list[MeasurementDb])
def get_all_measurements(*, session: Session = Depends(get_session)):
    return crud.get_all_measurements(session)

@router.get('/{measurement_id}', response_model=MeasurementDb)
def get_measurement_by_id(*, session: Session = Depends(get_session), measurement_id: int):
    return crud.get_measurement_by_id(session, measurement_id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=MeasurementDb)
def create_measurement(*, session: Session = Depends(get_session), measurement_in: MeasurementIn):
    return crud.create_measurement(session, measurement_in)

@router.delete("/{measurement_id}", response_model=MeasurementDb)
def delete_measurement_by_id(*, session: Session = Depends(get_session), measurement_id: int):
    return crud.delete_measurement_by_id(session, measurement_id)