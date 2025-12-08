from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import create_db
from .sensors.router import router as sensors_router
from .sensor_status.router import router as sensor_status_router
from .measurements.router import router as measurements_router
from .segments.router import router as segments_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(segments_router)
app.include_router(sensors_router)
app.include_router(sensor_status_router)
app.include_router(measurements_router)