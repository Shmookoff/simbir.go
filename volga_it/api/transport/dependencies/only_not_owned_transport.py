from typing import Annotated, Any

from fastapi import Depends, HTTPException, status

from volga_it.api.transport.models import Transport
from volga_it.dependencies import BaseDependency

from .only_owned_transport import OnlyOwnedTransport
from .transport_by_id import TransportById


class OnlyNotOwnedTransport(BaseDependency):
    get_owned_transport = OnlyOwnedTransport(auto_error=False)

    def __call__(
        self,
        transport: TransportById,
        owned_transport: Annotated[Transport | None, Depends(get_owned_transport)],
    ) -> Any:
        if not owned_transport:
            return transport

        if self.auto_error:
            raise self.FORBIDDEN

        return None


get_not_owned_transport = OnlyNotOwnedTransport()

GetNotOwnedTransport = Annotated[Transport, Depends(get_not_owned_transport)]
