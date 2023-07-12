from pydantic import BaseModel, condecimal


class HouseDB(BaseModel):
    id: int
    floor_count: int
    price: condecimal(gt=0)
