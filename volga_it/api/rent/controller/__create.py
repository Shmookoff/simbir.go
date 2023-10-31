"""
Groundworks for checking data integrity in admin logic
"""

from datetime import datetime
from typing import Callable, Literal

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


def get_user(account_id: int):
    user = Account.find(account_id)
    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User not found")
    return user


def get_transport(transport_id: int):
    transport = Transport.find(transport_id)
    if not transport:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Transport not found")
    return transport


RentState = Literal["started", "ended"]


def get_rent_state(data: AdminRentCreate) -> RentState:
    if data.time_end and data.final_price:
        return "started"
    if not data.time_end and not data.final_price:
        return "ended"
    raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid rent state")


rent_state_to_transport_status_actions: dict[
    RentState, dict[bool, Callable[[Transport], Transport]]
] = {
    "started": {
        True: lambda transport: transport.update(can_be_rented=False),
    },
    "ended": {
        False: lambda transport: transport.update(can_be_rented=True),
    },
}


def get_transport_action(transport: Transport, rent_state: RentState):
    action = rent_state_to_transport_status_actions[rent_state].get(
        transport.can_be_rented
    )
    if not action:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Rent state ({rent_state}) does not correspond with "
            f"current transport status ({transport.can_be_rented})",
        )
    return action


def create_as_admin(data: AdminRentCreate):
    account = get_user(data.user_id)
    transport = get_transport(data.transport_id)

    state = get_rent_state(data)

    transport_action = get_transport_action(transport, state)

    return Rent.create(**data.to_model_data())
