from fastapi import APIRouter

from volga_it.api.account import GetAccount

from .. import controller as TransportController
from ..dependencies import GetOwnedTransport, TransportById
from ..schemas import TransportCreate, TransportRead, TransportUpdate
from .common import PREFIX, TAG

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{transport_id}", response_model=TransportRead)
def read(transport: TransportById):
    TransportController.read(transport)


@router.post("", response_model=TransportRead)
def create(account: GetAccount, data: TransportCreate):
    return TransportController.create(account, data)


@router.put("/{transport_id}", response_model=TransportRead)
def update(transport: GetOwnedTransport, data: TransportUpdate):
    return TransportController.update(transport, data)


@router.delete("/{transport_id}")
def delete(transport: GetOwnedTransport):
    return TransportController.delete(transport)
