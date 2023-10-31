from pydantic import ConfigDict, Field, RootModel, computed_field

from volga_it.database.column_types import Point
from volga_it.schemas.api import APISchema

from .models import Transport


class TransportBase(APISchema):
    can_be_rented: bool
    model: str
    color: str
    identifier: str
    description: str | None = None
    minute_price: float | None = None
    day_price: float | None = None


class TransportTraitLocation(APISchema):
    latitude: float
    longitude: float

    def to_model_data(self):
        return {
            **super().to_model_data(exclude={"latitude", "longitude"}),
            "location": Point(self.latitude, self.longitude),
        }


class TransportTraitTransportType(APISchema):
    transport_type: Transport.TransportType


class TransportTraitOwnerId(APISchema):
    owner_id: int


class TransportCreate(
    TransportBase, TransportTraitTransportType, TransportTraitLocation
):
    pass


class TransportRead(TransportBase, TransportTraitTransportType, TransportTraitOwnerId):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int
    location: Point = Field(exclude=True)

    @computed_field
    @property
    def latitude(self) -> float:
        return self.location.x

    @computed_field
    @property
    def longitude(self) -> float:
        return self.location.y


TransportList = RootModel[list[TransportRead]]


class TransportUpdate(TransportBase, TransportTraitLocation):
    pass


class TransportAdminUpdateable(
    TransportBase,
    TransportTraitTransportType,
    TransportTraitLocation,
    TransportTraitOwnerId,
):
    pass


class AdminTransportCreate(TransportCreate, TransportAdminUpdateable):
    pass


class AdminTransportUpdate(TransportUpdate, TransportAdminUpdateable):
    pass
