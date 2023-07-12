from pydantic import BaseModel, condecimal, Extra


class CarDB(BaseModel):
    id: int
    engine_type_id: int
    mark: str
    model: str
    price: condecimal(gt=0)
    person_id: int | None


class CarCreate(BaseModel):
    engineType: str
    mark: str
    model: str
    price: condecimal(gt=0)

    def __init__(self, *args, **kwargs):
        new_kwarg = kwargs.copy()
        for name, value in kwargs.items():
            if name in ('engine type', ):
                new_kwarg['engineType'] = value
        super().__init__(*args, **new_kwarg)

    class Config:
        extra = Extra.ignore


class Car(CarCreate):
    id: int
