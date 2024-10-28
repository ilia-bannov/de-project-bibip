from datetime import datetime
from decimal import Decimal
from models import (
    Car, CARS_FILE_NAME,
    Model, MODELS_FILE_NAME,
    Sale, SALES_FILE_NAME,
    CarFullInfo, CarStatus,
    ModelSaleStats, DATE_FORMAT
)
from indexes import (
    CarIndex, CARS_INDEX_FILE_NAME,
    ModelIndex, MODELS_INDEX_FILE_NAME,
    SaleIndex, SALES_INDEX_FILE_NAME
)
from bibip_file_service import FileService


class CarService:

    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        self.file_service = FileService(self.root_directory_path)
        self.model_index: list[ModelIndex] = []
        self.car_index: list[CarIndex] = []
        self.sale_index: list[SaleIndex] = []

    def _get_car_full_info(self,
                           car: Car,
                           model: Model,
                           sale: Sale | None) -> CarFullInfo:
        return CarFullInfo(
            vin=car.vin,
            car_model_name=model.name,
            car_model_brand=model.brand,
            price=car.price,
            date_start=car.date_start,
            status=car.status,
            sales_date=sale.sales_date if sale else None,
            sales_cost=sale.cost if sale else None
        )

    def _get_car(self, car_line: list[str] | None) -> Car | None:
        if car_line and len(car_line) >= 5:
            return Car(
                vin=car_line[0],
                model=int(car_line[1]),
                price=Decimal(car_line[2]),
                date_start=datetime.strptime(car_line[3], DATE_FORMAT),
                status=CarStatus(car_line[4]),
                is_deleted=car_line[5] == 'True'
            )
        return None

    def _get_car_index_by_vin(self, vin: str) -> CarIndex | None:
        for index in self.car_index:
            if index.id == vin:
                return index

        return None

    def _get_model_index_by_id(self, id: int) -> ModelIndex | None:
        for index in self.model_index:
            if index.id == id:
                return index

        return None

    def _get_sale_index_by_car_vin(self, car_vin: str) -> SaleIndex | None:
        for index in self.sale_index:
            if index.id == car_vin:
                return index

        return None

    def _get_car_by_index(self, index: CarIndex | None) -> Car | None:
        if not index:
            return None

        line = self.file_service.get_line_from_file(
            CARS_FILE_NAME,
            index.position_in_data_file
        )
        return self._get_car(line)

    def _get_model_by_index(self, index: ModelIndex | None) -> Model | None:
        if index:
            line = self.file_service.get_line_from_file(
                MODELS_FILE_NAME,
                index.position_in_data_file
            )
            if line and len(line) >= 4:
                return Model(
                    id=int(line[0]),
                    name=line[1],
                    brand=line[2],
                    is_deleted=line[3] == 'True'
                )

        return None

    def _get_sale_by_index(self, index: SaleIndex | None) -> Sale | None:
        if index:
            line = self.file_service.get_line_from_file(
                SALES_FILE_NAME,
                index.position_in_data_file
            )
            if line and len(line) >= 5:
                return Sale(
                    sales_number=line[0],
                    car_vin=line[1],
                    sales_date=datetime.strptime(line[2], DATE_FORMAT),
                    cost=Decimal(line[3]),
                    is_deleted=line[4] == 'True'
                )

        return None

    def _update_car_status_by_vin(self,
                                  vin: str,
                                  car_status: CarStatus) -> Car | None:
        car_index = self._get_car_index_by_vin(vin)
        car = self._get_car_by_index(car_index)
        if car and car_index:
            car.status = car_status
            self.file_service.write_file(
                CARS_FILE_NAME,
                car_index.position_in_data_file,
                car.get_car_string()
            )
            return car
        return None

    def _update_index(self, file_name: str, new_index, index) -> None:
        index.append(new_index)
        index.sort(key=lambda i: i.id)
        lines = [i.get_index_string() for i in index]
        self.file_service.rewrite_file(file_name, lines)

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        self.file_service.append_file(
            model.get_model_string(),
            MODELS_FILE_NAME
        )

        new_index = ModelIndex(model.id, len(self.model_index))
        self._update_index(MODELS_INDEX_FILE_NAME, new_index, self.model_index)

        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        self.file_service.append_file(car.get_car_string(), CARS_FILE_NAME)

        new_index = CarIndex(car.vin, len(self.car_index))
        self._update_index(CARS_INDEX_FILE_NAME, new_index, self.car_index)

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car | None:
        self.file_service.append_file(sale.get_sale_string(), SALES_FILE_NAME)

        new_index = SaleIndex(sale.car_vin, len(self.sale_index))
        self._update_index(SALES_INDEX_FILE_NAME, new_index, self.sale_index)

        return self._update_car_status_by_vin(sale.car_vin, CarStatus.sold)

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        car_list: list[Car] = []
        car_lines = self.file_service.read_file(CARS_FILE_NAME)
        for line in car_lines:
            if line[4] == status.value:
                car = self._get_car(line)
                if car:
                    car_list.append(car)

        # car_list.sort(key=lambda c: c.vin)
        return car_list

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        car_index = self._get_car_index_by_vin(vin)
        car = self._get_car_by_index(car_index)
        if car:
            model_index = self._get_model_index_by_id(car.model)
            model = self._get_model_by_index(model_index)
            if model:
                if car.status == CarStatus.sold:
                    sales_index = self._get_sale_index_by_car_vin(vin)
                    sale = self._get_sale_by_index(sales_index)
                    if sale:
                        return self._get_car_full_info(car, model, sale)
                return self._get_car_full_info(car, model, None)

        return None

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car | None:
        car_index = self._get_car_index_by_vin(vin)
        car = self._get_car_by_index(car_index)
        if car and car_index:
            car.is_deleted = True
            self.file_service.write_file(
                CARS_FILE_NAME,
                car_index.position_in_data_file,
                car.get_car_string()
            )
            car.vin = new_vin
            car.is_deleted = False
            return self.add_car(car)

        return None

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car | None:
        car_vin = sales_number.split('#')[1]
        sales_index = self._get_sale_index_by_car_vin(car_vin)
        sale = self._get_sale_by_index(sales_index)
        if sale and sales_index:
            sale.is_deleted = True
            self.file_service.write_file(
                SALES_FILE_NAME,
                sales_index.position_in_data_file,
                sale.get_sale_string()
            )
            return self._update_car_status_by_vin(car_vin, CarStatus.available)

        return None

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        result: list[ModelSaleStats] = []
        model_sales_count: dict[str, str] = {}
        model_price: dict[str, str] = {}
        top_models: list[dict[str, str]] = []
        car_lines = self.file_service.read_file(CARS_FILE_NAME)
        for line in car_lines:
            if line[4] == CarStatus.sold:
                model_id = line[1]
                sales_count = int(model_sales_count.get(model_id, '0')) + 1
                model_sales_count[model_id] = str(sales_count)
                model_price[model_id] = line[2]

        for model_id, sales_number in model_sales_count.items():
            top_models.append({
                'model_id': model_id,
                'sales_number': sales_number,
                'price': model_price[model_id]
            })

        top_3_models = sorted(top_models,
                              key=lambda item: (
                                  int(item['sales_number']),
                                  Decimal(item['price'])
                              ),
                              reverse=True)[:3]
        for top_model in top_3_models:
            model_index = self._get_model_index_by_id(
                int(top_model["model_id"])
            )
            model = self._get_model_by_index(model_index)
            if model:
                model_sale = ModelSaleStats(
                    car_model_name=model.name,
                    brand=model.brand,
                    sales_number=int(top_model["sales_number"])
                )
                result.append(model_sale)

        return result
