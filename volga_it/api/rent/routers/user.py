from typing import Annotated

from fastapi import APIRouter, Query

from volga_it.api.account import GetAccount
from volga_it.api.transport import (
    GetNotOwnedTransport,
    GetOwnedTransport,
    TransportTypeFilter,
)
from volga_it.api.transport.schemas import TransportList

from .. import controller as RentController
from ..dependencies import GetRentRenter, GetRentRenterOrOwner
from ..models import Rent
from ..schema import RentList, RentRead
from .common import PREFIX, TAG

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/Transport", response_model=TransportList)
def find_transport(
    lat: Annotated[float, Query()],
    long: Annotated[float, Query()],
    radius: Annotated[float, Query()],
    type: Annotated[TransportTypeFilter, Query()],
):
    return RentController.find_transport(lat, long, radius, type)


@router.get("/{rent_id}", response_model=RentRead)
def read(rent: GetRentRenterOrOwner):
    return RentController.read(rent)


@router.get("/MyHistory", response_model=RentList)
def list_user_history(account: GetAccount):
    return RentController.user_history(account)


@router.get("/TransportHistory/{transport_id}", response_model=RentList)
def list_transport_history(transport: GetOwnedTransport):
    return RentController.transport_history(transport)


@router.post("/New/{transport_id}", response_model=RentRead)
def new(
    account: GetAccount,
    transport: GetNotOwnedTransport,
    rent_type: Annotated[Rent.PriceType, Query()],
):
    return RentController.new(account, transport, rent_type)


@router.post("/End/{rent_id}", response_model=RentRead)
def end(
    rent: GetRentRenter,
    lat: Annotated[float, Query()],
    long: Annotated[float, Query()],
):
    return RentController.end(rent, lat, long)
