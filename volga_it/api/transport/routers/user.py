from fastapi import APIRouter, status

from volga_it.api.account import GetAccount

from .. import controller as TransportController
from ..dependencies import GetOwnedTransport, TransportById
from ..schemas import TransportCreate, TransportRead, TransportUpdate
from .common import PREFIX, TAG

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{transport_id}", response_model=TransportRead)
def read(transport: TransportById):
    return TransportController.read(transport)


@router.post("", response_model=TransportRead, status_code=status.HTTP_201_CREATED)
def create(account: GetAccount, data: TransportCreate):
    return TransportController.create(account, data)


@router.put("/{transport_id}", response_model=TransportRead)
def update(transport: GetOwnedTransport, data: TransportUpdate):
    return TransportController.update(transport, data)


@router.delete("/{transport_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(transport: GetOwnedTransport):
    return TransportController.delete(transport)
