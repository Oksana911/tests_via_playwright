from typing import Any


class CarBuilder:
    def __init__(self):
        self.car_data = {
            'engineType': 'Electric',
            'mark': 'Tesla',
            'model': 'Model X',
            'price': 70000,
        }

    def set_engine_type(self, engine_type: Any) -> 'CarBuilder':
        self.car_data['engineType'] = engine_type
        return self

    def set_mark(self, mark: Any) -> 'CarBuilder':
        self.car_data['mark'] = mark
        return self

    def set_model(self, model: Any) -> 'CarBuilder':
        self.car_data['model'] = model
        return self

    def set_price(self, price: Any) -> 'CarBuilder':
        self.car_data['price'] = price
        return self

    def set_id(self, id: int) -> 'CarBuilder':
        self.car_data['id'] = id
        return self

    def build(self) -> dict[str, Any]:
        return self.car_data
