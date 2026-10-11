import datetime
import enum

from sqlalchemy import String, Numeric, Text, Integer, JSON
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass

class Body(str, enum.Enum):
    sedan = 'sedan'
    hatchback = 'hatchback'
    station_wagon = 'station_wagon'
    coupe = 'coupe'
    cabriolet = 'cabriolet'
    crossover ='crossover'
    SUV ='SUV'
    minivan ='minivan'
    pickup_truck = 'pickup_truck'

class FuelType(str, enum.Enum):
    gas = 'gas'
    gasoline = 'gasoline'
    diesel = 'diesel'
    electric = 'electric'


class Car(Base):
    __tablename__ = 'cars'

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(8), unique=True)
    car_make_model: Mapped[str] = mapped_column(String(200))
    automaker: Mapped[str] = mapped_column(String(200))
    vin: Mapped[str] = mapped_column(String(16), unique=True)
    body: Mapped[Body] = mapped_column(SqlEnum(Body), nullable=False)
    fuel_type: Mapped[FuelType] = mapped_column(SqlEnum(FuelType), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    rating: Mapped[float | None] = mapped_column(default=None)
    is_available: Mapped[bool] = mapped_column(default=True)
    summary: Mapped[str | None] = mapped_column(Text, default=None)
    year: Mapped[int] = mapped_column(Integer)
    added_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    additional_options: Mapped[list[str | None]] = mapped_column(JSON, default=None)