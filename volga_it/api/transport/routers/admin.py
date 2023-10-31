from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from volga_it.api.account.dependencies import get_admin
from volga_it.api.admin.common import ADMIN_BASE_TAG, ADMIN_PREFIX
from volga_it.api.transport.controller.list import TransportTypeFilter

from .. import controller as TransportController
from ..dependencies import TransportById
from ..schemas import (
    AdminTransportCreate,
    AdminTransportUpdate,
    TransportList,
    TransportRead,
)
from .common import PREFIX, TAG

router = APIRouter(
    prefix=ADMIN_PREFIX + PREFIX,
    tags=[ADMIN_BASE_TAG + TAG],
    dependencies=[Depends(get_admin)],
)


@router.get("", response_model=TransportList)
def list(
    start: Annotated[int, Query(gt=0)],
    count: Annotated[int, Query(gt=0)],
    transport_type: Annotated[TransportTypeFilter, Query(alias="transportType")],
):
    return TransportController.list(start, count, transport_type)


@router.get("/{transport_id}", response_model=TransportRead)
def read(transport: TransportById):
    return TransportController.read(transport)


@router.post("", status_code=status.HTTP_201_CREATED)
def create(data: AdminTransportCreate):
    return TransportController.create_as_admin(data)


@router.put("/{transport_id}")
def update(transport: TransportById, data: AdminTransportUpdate):
    return TransportController.update(transport, data)


@router.delete("/{transport_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(transport: TransportById):
    return TransportController.delete(transport)
