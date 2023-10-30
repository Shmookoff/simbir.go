from typing import Annotated

from fastapi import APIRouter, Depends, Query

from volga_it.api.account import AccountById
from volga_it.api.account.dependencies import get_admin
from volga_it.api.admin.common import ADMIN_BASE_TAG, ADMIN_PREFIX
from volga_it.api.transport import TransportById

from .. import controller as RentController
from ..dependencies import RentById
from ..schema import AdminRentCreate, AdminRentUpdate, RentList, RentRead
from .common import PREFIX, TAG

router = APIRouter(
    prefix=ADMIN_PREFIX + PREFIX,
    tags=[ADMIN_BASE_TAG + TAG],
    dependencies=[Depends(get_admin)],
)


@router.get("/{rent_id}", response_model=RentRead)
def read(rent: RentById):
    return RentController.read(rent)


@router.get("/UserHistory/{account_id}", response_model=RentList)
def list_user_history(account: AccountById):
    return RentController.user_history(account)


@router.get("/UserHistory/{transport_id}", response_model=RentList)
def list_transport_history(transport: TransportById):
    return RentController.transport_history(transport)


@router.post("", response_model=RentRead)
def create(data: AdminRentCreate):
    return RentController.create_as_admin(data)


@router.post("/End/{rent_id}", response_model=RentRead)
def end(
    rent: RentById,
    lat: Annotated[float, Query()],
    long: Annotated[float, Query()],
):
    return RentController.end(rent, lat, long)


@router.put("/{rent_id}", response_model=RentRead)
def update(rent: RentById, data: AdminRentUpdate):
    return RentController.update_as_admin(rent, data)


@router.delete("/{rent_id}")
def delete(rent: RentById):
    return RentController.delete(rent)
