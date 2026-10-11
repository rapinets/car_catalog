from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp

from app.database import engine
from app.models import Base
from app.routers import car


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Car API", lifespan=lifespan)
app.include_router(car.router)

def cors_middleware(app: ASGIApp) -> ASGIApp:
    return CORSMiddleware(
        app,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.add_middleware(cors_middleware)
