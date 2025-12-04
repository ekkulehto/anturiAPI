from fastapi import HTTPException, Response, status
from sqlmodel import Session, select
from .models import SensorDb, SensorStatusIn, SensorStatusDb

def create_sensor_status(session: Session, sensor_status_in: SensorStatusIn):
    sensor = session.get(SensorDb, sensor_status_in.sensor_id)

    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Sensor not found',
        )

    sensor_status = SensorStatusDb.model_validate(sensor_status_in)
    session.add(sensor_status)
    sensor.status = sensor_status_in.status
    session.commit()
    session.refresh(sensor_status)
    return sensor_status

def get_all_sensor_statuses(session: Session):
    return session.exec(select(SensorStatusDb)).all()

def get_sensor_status_by_id(session: Session, sensor_status_id: int):
    sensor_status = session.get(SensorStatusDb, sensor_status_id)

    if not sensor_status:
        raise HTTPException(
            detail='Sensor not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return sensor_status

def delete_sensor_status_by_id(session: Session, sensor_status_id: int):
    sensor_status = session.get(SensorStatusDb, sensor_status_id)

    if not sensor_status:
        raise HTTPException(
            detail='Sensor status not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    session.delete(sensor_status)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)