from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from volga_it.database import BaseModel

if TYPE_CHECKING:
    from volga_it.api.rent import Rent
    from volga_it.api.transport import Transport


class Account(BaseModel):
    __tablename__ = "accounts"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    balance: Mapped[float] = mapped_column(default=0)

    transport: Mapped[list["Transport"]] = relationship(back_populates="owner")
    rents: Mapped[list["Rent"]] = relationship(back_populates="user")


class AccessToken(BaseModel):
    __tablename__ = "access_tokens"
