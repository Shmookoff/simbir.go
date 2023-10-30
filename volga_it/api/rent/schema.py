from datetime import datetime

from pydantic import RootModel

from volga_it.schemas.api import APISchema

from .models import Rent


class RentBase(APISchema):
    transport_id: int
    user_id: int
    time_start: datetime
    time_end: datetime | None
    price_of_unit: float
    price_type: Rent.PriceType
    final_price: float | None


class RentListItem(APISchema):
    id: int


RentList = RootModel[list[RentListItem]]


class RentRead(RentBase, RentListItem):
    pass


class AdminRentCreate(RentBase):
    pass


class AdminRentUpdate(RentBase):
    pass
