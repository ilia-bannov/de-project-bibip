CARS_INDEX_FILE_NAME = 'cars_index.txt'
MODELS_INDEX_FILE_NAME = 'models_index.txt'
SALES_INDEX_FILE_NAME = 'sales_index.txt'


class ModelIndex:
    def __init__(self, model_id: int, position_in_data_file: int):
        self.id = model_id
        self.position_in_data_file = position_in_data_file

    def get_index_string(self):
        return f"{self.id},{self.position_in_data_file}"


class CarIndex:
    def __init__(self, vin: str, position_in_data_file: int):
        self.id = vin
        self.position_in_data_file = position_in_data_file

    def get_index_string(self):
        return f"{self.id},{self.position_in_data_file}"


class SaleIndex:
    def __init__(self, car_vin: str, position_in_data_file: int):
        self.id = car_vin
        self.position_in_data_file = position_in_data_file

    def get_index_string(self):
        return f"{self.id},{self.position_in_data_file}"
