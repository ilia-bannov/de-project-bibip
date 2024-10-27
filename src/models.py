from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
MODELS_FILE_NAME = 'models.txt'
CARS_FILE_NAME = 'cars.txt'
SALES_FILE_NAME = 'sales.txt'


class CarStatus(StrEnum):
    available = "available"
    reserve = "reserve"
    sold = "sold"
    delivery = "delivery"


class Car(BaseModel):
    vin: str
    model: int
    price: Decimal
    date_start: datetime
    status: CarStatus
    is_deleted: bool = False

    def index(self) -> str:
        return self.vin

    def get_car_string(self) -> str:
        return (
            f"{self.vin},{self.model},{self.price},"
            f"{self.date_start.strftime(DATE_FORMAT)},"
            f"{self.status.value},{self.is_deleted}"
        )


class Model(BaseModel):
    id: int
    name: str
    brand: str
    is_deleted: bool = False

    def index(self) -> str:
        return str(self.id)

    def get_model_string(self) -> str:
        return f"{self.id},{self.name},{self.brand},{self.is_deleted}"


class Sale(BaseModel):
    sales_number: str
    car_vin: str
    sales_date: datetime
    cost: Decimal
    is_deleted: bool = False

    def index(self) -> str:
        return self.car_vin

    def get_sale_string(self) -> str:
        return (
            f"{self.sales_number},{self.car_vin},"
            f"{self.sales_date.strftime(DATE_FORMAT)},"
            f"{self.cost},{self.is_deleted}"
        )


class CarFullInfo(BaseModel):
    vin: str
    car_model_name: str
    car_model_brand: str
    price: Decimal
    date_start: datetime
    status: CarStatus
    sales_date: datetime | None
    sales_cost: Decimal | None


class ModelSaleStats(BaseModel):
    car_model_name: str
    brand: str
    sales_number: int
