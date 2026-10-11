from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Car, FuelType
from app.schemas import CarCreate, CarUpdate


def create_car(session: Session, payload: CarCreate):
    car = Car(**payload.model_dump())
    session.add(car)
    session.commit()
    session.refresh(car)
    return car

def get_cars(session: Session, car_make_model: str | None = None, fuel_type: FuelType | None = None, year: int | None = None, limit: int = 20, offset: int = 0):
    stmt = select(Car)
    if car_make_model is not None:
        stmt = stmt.where(Car.car_make_model == car_make_model)
    if fuel_type is not None:
        stmt = stmt.where(Car.fuel_type == fuel_type)
    if year is not None:
        stmt = stmt.where(Car.year == year)
    stmt = stmt.order_by(Car.id).offset(offset).limit(limit)
    return list(session.scalars(stmt).all())

def get_car(session: Session, car_id: int) -> Car | None:
    return session.get(Car, car_id)

def update_car(session: Session, payload: CarUpdate, car: Car) -> Car:
    changes_dict = payload.model_dump(exclude_unset=True)
    for key, value in changes_dict.items():
        setattr(car, key, value)
    session.commit()
    session.refresh(car)
    return car

def delete_car(session: Session, car: Car) -> None:
    session.delete(car)
    session.commit()