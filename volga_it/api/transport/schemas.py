from pydantic import RootModel

from volga_it.database.column_types import Point
from volga_it.schemas.api import APISchema

from .models import Transport


class TransportBase(APISchema):
    can_be_rented: bool
    model: str
    color: str
    identifier: str
    description: str | None
    latitude: float
    longitude: float
    minute_price: float | None
    day_price: float | None

    def to_model_data(self):
        return {
            **super().to_model_data(),
            "location": Point(self.latitude, self.longitude),
        }


class TransportCreate(TransportBase):
    transport_type: Transport.TransportType


class TransportAdminUpdateable(TransportBase):
    owner_id: int


class TransportRead(TransportAdminUpdateable):
    id: int


TransportList = RootModel[list[TransportRead]]


class TransportUpdate(TransportCreate):
    pass


class AdminTransportCreate(TransportCreate, TransportAdminUpdateable):
    pass


class AdminTransportUpdate(TransportUpdate, TransportAdminUpdateable):
    pass
