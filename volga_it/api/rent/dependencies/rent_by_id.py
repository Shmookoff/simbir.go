from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from ..models import Rent


def rent_by_id(rent_id: int = Path(gt=0)):
    rent = Rent.find(rent_id)
    if not rent:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Rent Not Found")
    return rent


RentById = Annotated[Rent, Depends(rent_by_id)]
