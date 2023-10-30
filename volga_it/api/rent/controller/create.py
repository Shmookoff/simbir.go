from datetime import datetime

from fastapi import HTTPException, status

from volga_it.api.account import Account
from volga_it.api.transport import Transport

from ..models import Rent
from ..schema import AdminRentCreate


def new(account: Account, transport: Transport, rent_type: Rent.PriceType):
    if rent_type == "Minutes":
        price_of_unit = transport.minute_price
    elif rent_type == "Days":
        price_of_unit = transport.day_price
    else:
        raise ValueError(f"unexpected {rent_type = }")

    if account.balance < 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Insufficient balance")

    return Rent.create(
        time_start=datetime.now(),
        price_of_unit=price_of_unit,
        price_type=rent_type,
        user=account,
        transport=transport,
    )


def create_as_admin(data: AdminRentCreate):
    return Rent.create(**data.to_model_data())
