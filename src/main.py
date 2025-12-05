from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database import create_db
from .sensors.router import router as sensors_router
from .measurements.router import router as measurements_router
from .segments.router import router as segments_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(sensors_router)
app.include_router(measurements_router)
app.include_router(segments_router)