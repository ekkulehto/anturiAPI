from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import create_db
from .segments.router import router as segments_router
from .sensors.router import router as sensors_router
from .sensor_status.router import router as sensor_status_router
from .sensor_measurements.router import router as measurements_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(segments_router)
app.include_router(sensors_router)
app.include_router(sensor_status_router)
app.include_router(measurements_router)