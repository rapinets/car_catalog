from fastapi import APIRouter, status, HTTPException
from sqlalchemy.exc import IntegrityError

from app import schemas
from ..dependencies import SessionDep
from ..models import FuelType
from ..services import car_service

router = APIRouter(prefix="/cars", tags=["cars"])

@router.get("/", response_model=list[schemas.CarResponse])
def get_cars(db: SessionDep, car_make_model: str | None = None, fuel_type: FuelType | None = None, year: int | None = None, limit: int = 20, offset: int = 0):
    return car_service.get_cars(db, car_make_model, fuel_type, year, limit, offset)

@router.post("/", response_model=schemas.CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(payload: schemas.CarCreate, db: SessionDep):
    try:
        return car_service.create_car(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This car already exists.")

@router.get("/{car_id}", response_model=schemas.CarResponse)
def get_car(car_id: int, db: SessionDep):
    car = car_service.get_car(db, car_id)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This car does not exist.")
    return car

@router.patch("/{car_id}", response_model=schemas.CarResponse)
def update_car(car_id: int, payload: schemas.CarUpdate, db: SessionDep):
    car = car_service.get_car(db, car_id)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This car does not exist.")
    try:
        return car_service.update_car(db, car, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This car already exists.")

@router.delete("/{car_id}", response_model=schemas.CarResponse)
def delete_car(car_id: int, db: SessionDep):
    car = car_service.get_car(db, car_id)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This car does not exist.")
    car_service.delete_car(db, car)
