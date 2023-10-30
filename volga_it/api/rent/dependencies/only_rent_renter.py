from typing import Annotated

from fastapi import Depends

from volga_it.api.account import GetAccount
from volga_it.dependencies import BaseDependency

from ..models import Rent
from .rent_by_id import RentById


class OnlyRentRenter(BaseDependency):
    def __call__(self, rent: RentById, account: GetAccount) -> Rent | None:
        if rent.user == account:
            return rent

        if self.auto_error:
            raise self.FORBIDDEN

        return None


get_rent_renter = OnlyRentRenter()

GetRentRenter = Annotated[Rent, Depends(get_rent_renter)]
