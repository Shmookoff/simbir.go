from typing import TYPE_CHECKING, Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from volga_it.api.account import Account
from volga_it.database.column_types import Point
from volga_it.database.models import BaseModel

if TYPE_CHECKING:
    from volga_it.api.rent import Rent


class Transport(BaseModel):
    __tablename__ = "transport"

    TransportType = Literal["Car", "Bike", "Scooter"]

    can_be_rented: Mapped[bool]
    transport_type: Mapped[TransportType]
    model: Mapped[str]
    color: Mapped[str]
    identifier: Mapped[str]
    description: Mapped[str | None]
    location: Mapped[Point]
    minute_price: Mapped[float | None]
    day_price: Mapped[float | None]

    owner_id: Mapped[int] = mapped_column(ForeignKey(Account.id, ondelete="RESTRICT"))
    owner: Mapped[Account] = relationship(back_populates="transport")

    rents: Mapped[list["Rent"]] = relationship(back_populates="transport")


TransportTypeFilter = Transport.TransportType | Literal["All"]
