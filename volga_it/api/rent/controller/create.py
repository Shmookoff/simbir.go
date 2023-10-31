from datetime import datetime

from fastapi import HTTPException, status

from volga_it.api.account import Account
from volga_it.api.transport import Transport

from ..models import Rent
from ..schema import AdminRentCreate


def check_transport_rentable(transport: Transport):
    if not transport.can_be_rented:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Transport cannot be rented at this time"
        )


def check_balance(account: Account):
    if account.balance < 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Insufficient balance")


def get_price_of_unit(transport: Transport, rent_type: Rent.PriceType):
    if rent_type == "Minutes":
        price_of_unit = transport.minute_price
    elif rent_type == "Days":
        price_of_unit = transport.day_price
    else:
        raise ValueError(f"unexpected {rent_type = }")
    if price_of_unit is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"price_of_unit of transport for rent_type {rent_type} is not defined",
        )
    return price_of_unit


def new(account: Account, transport: Transport, rent_type: Rent.PriceType):
    check_transport_rentable(transport)
    check_balance(account)

    price_of_unit = get_price_of_unit(transport, rent_type)

    transport.update(can_be_rented=False)

    return Rent.create(
        time_start=datetime.now(),
        price_of_unit=price_of_unit,
        price_type=rent_type,
        user=account,
        transport=transport,
    )


def create_as_admin(data: AdminRentCreate):
    return Rent.create(**data.to_model_data())
