from typing import Annotated

from fastapi import Depends, HTTPException, status

from volga_it.api.account import GetAccount
from volga_it.dependencies import BaseDependency

from ..models import Transport
from .transport_by_id import TransportById


class OnlyOwnedTransport(BaseDependency):
    def __call__(
        self, account: GetAccount, transport: TransportById
    ) -> Transport | None:
        if account.id == transport.owner_id:
            return transport

        if self.auto_error:
            raise self.FORBIDDEN

        return None


get_owned_transport = OnlyOwnedTransport()

GetOwnedTransport = Annotated[Transport, Depends(get_owned_transport)]
