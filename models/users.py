from decimal import Decimal

from pydantic import BaseModel, condecimal
from models.cars import Car


class UserDB(BaseModel):
    id: int
    first_name: str
    second_name: str
    age: int
    sex: str
    money: condecimal(decimal_places=2)
    house_id: int | None


class UserCreate(BaseModel):
    firstName: str
    secondName: str
    age: int
    sex: str
    money: condecimal()


class User(UserCreate):
    id: int

    def __init__(self, *args, **kwargs):
        new_kwargs = kwargs.copy()
        for name, value in kwargs.items():
            if name in ('first name', 'first_name'):
                new_kwargs['firstName'] = kwargs.get(name)
            elif name in ('last name', 'second_name'):
                new_kwargs['secondName'] = kwargs.get(name)
            elif name == 'sex':
                if value is True:
                    new_kwargs[name] = 'MALE'
                if value is False:
                    new_kwargs[name] = 'FEMALE'
        super().__init__(*args, **new_kwargs)


class UserInfo(User):
    cars: list[Car | None]
