import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.models import Body, FuelType


class CarBase(BaseModel):
    number: str = Field(pattern=r'^[ABCEHIKMOPTX]{2}\d{4}[ABCEHIKMOPTX]{2}$')
    car_make_model: str = Field(min_length=2, max_length=200)
    automaker: str = Field(min_length=2, max_length=200)
    vin: str = Field(pattern=r'^[A-HJ-NPR-Z0-9]{17}$')
    body: Body
    fuel_type: FuelType
    price: float = Field(ge=0.0)
    rating: float = Field(ge=0.0)
    summary: str | None = Field(default=None, max_length=2000000)
    year: int = Field(gt=1900, lt=2027)
    additional_options: list[str] | None = Field(default=None, max_length=20)

class CarCreate(CarBase):
    pass

class CarUpdate(CarBase):
    number: str | None = Field(default=None, pattern=r'^[ABCEHIKMOPTX]{2}\d{4}[ABCEHIKMOPTX]{2}$')
    car_make_model: str | None = Field(default=None, min_length=2, max_length=200)
    automaker: str | None = Field(default=None, min_length=2, max_length=200)
    body: Body | None = None
    fuel_type: FuelType | None = None
    price: float | None = Field(default=None, ge=0.0)
    rating: float | None = Field(default=None, ge=0.0)
    is_available: bool | None = None
    summary: str | None = Field(default=None, max_length=2000000)
    year: int | None = Field(default=None, gt=1900, lt=2027)
    additional_options: list[str] | None = Field(default=None, max_length=20)

class CarResponse(BaseModel):
    id: int
    is_available: bool
    added_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)