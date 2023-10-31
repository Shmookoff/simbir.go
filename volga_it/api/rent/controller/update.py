from datetime import datetime
from math import ceil

from fastapi import HTTPException, status

from volga_it.api.account import Account
from volga_it.api.rent.schema import AdminRentUpdate
from volga_it.api.transport import Transport
from volga_it.database.column_types import Point

from ..models import Rent


def end(rent: Rent, latitude: float, longitude: float):
    if rent.time_end:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Rent already ended")

    now = datetime.now()
    delta = now - rent.time_start

    if rent.price_type == "Minutes":
        units = ceil(delta.total_seconds() / 60)
    elif rent.price_type == "Days":
        units = ceil(delta.total_seconds() / 60 * 60 * 24)
    else:
        raise ValueError(f"unexpected {rent.price_type = }")

    final_price = units * rent.price_of_unit

    Transport.find_or_fail(rent.transport_id).update(
        location=Point(latitude, longitude), can_be_rented=True
    )
    # rent.transport.update(location=Point(latitude, longitude))

    renter = Account.find_or_fail(rent.user_id)
    renter.update(balance=renter.balance - final_price)
    # rent.user.update(balance=rent.user.balance - final_price)

    return rent.update(time_end=now, final_price=final_price)


def update_as_admin(rent: Rent, data: AdminRentUpdate):
    return rent.update(**data.to_model_data())
