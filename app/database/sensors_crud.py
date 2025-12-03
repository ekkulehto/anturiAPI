from fastapi import HTTPException, Response, status
from sqlmodel import Session, select
from .models import SensorIn, SensorDb

def create_sensor(session: Session, sensor_in: SensorIn):
    sensor = SensorDb.model_validate(sensor_in)
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor

def get_all_sensors(session: Session):
    return session.exec(select(SensorDb)).all()

def get_sensor_by_id(session: Session, sensor_id: int):
    sensor = session.get(SensorDb, sensor_id)

    if not sensor:
        raise HTTPException(
            detail='Sensor not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return sensor

def delete_sensor_by_id(session: Session, sensor_id: int):
    sensor = session.get(SensorDb, sensor_id)

    if not sensor:
        raise HTTPException(
            detail='Sensor not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    session.delete(sensor)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)