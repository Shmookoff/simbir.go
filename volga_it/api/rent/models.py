from datetime import datetime
from typing import Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from volga_it.api.account import Account
from volga_it.api.transport import Transport
from volga_it.database.models import BaseModel


class Rent(BaseModel):
    __tablename__ = "rents"

    PriceType = Literal["Minutes", "Days"]

    time_start: Mapped[datetime]
    time_end: Mapped[datetime | None]
    price_of_unit: Mapped[float]
    price_type: Mapped[PriceType]
    final_price: Mapped[float | None]

    user_id: Mapped[int] = mapped_column(ForeignKey(Account.id, ondelete="RESTRICT"))
    user: Mapped[Account] = relationship(back_populates="rents")

    transport_id: Mapped[int] = mapped_column(
        ForeignKey(Transport.id, ondelete="RESTRICT")
    )
    transport: Mapped[Transport] = relationship(back_populates="rents")
