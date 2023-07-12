from decimal import Decimal
from typing import Any


class UserBuilder:
    """Класс получения payload для различных запросов"""

    def __init__(self):
        self.user_data = {
            'firstName': 'Vasiliy',
            'secondName': 'Rubenstein',
            'age': 42,
            'sex': 'MALE',
            'money': 1000000,
        }

    def set_first_name(self, first_name: Any) -> 'UserBuilder':
        self.user_data['firstName'] = first_name
        return self

    def set_second_name(self, second_name: Any) -> 'UserBuilder':
        self.user_data['secondName'] = second_name
        return self

    def set_age(self, age: int) -> 'UserBuilder':
        self.user_data['age'] = age
        return self

    def set_sex(self, sex: str) -> 'UserBuilder':
        self.user_data['sex'] = sex
        return self

    def set_money(self, money: Decimal) -> 'UserBuilder':
        self.user_data['money'] = money
        return self

    def set_id(self, id: int) -> 'UserBuilder':
        self.user_data['id'] = id
        return self

    def build(self) -> dict[str, Any]:
        return self.user_data
