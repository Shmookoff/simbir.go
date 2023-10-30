from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from ..models import Transport


def transport_by_id(transport_id: int = Path(gt=0)) -> Transport:
    transport = Transport.find(transport_id)
    if not transport:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Transport Not Found")
    return transport


TransportById = Annotated[Transport, Depends(transport_by_id)]
