from typing import Annotated

from fastapi import Depends

from volga_it.api.account import GetAccount
from volga_it.dependencies import BaseDependency

from ..models import Rent
from .only_rent_renter import OnlyRentRenter
from .rent_by_id import RentById


class OnlyRentRenterOrOwner(BaseDependency):
    get_rent_renter = OnlyRentRenter(auto_error=False)

    def __call__(
        self,
        account: GetAccount,
        rent_renter: Annotated[Rent, Depends(get_rent_renter)],
        rent: RentById,
    ) -> Rent | None:
        if rent_renter or rent.transport.owner == account:
            return rent

        if self.auto_error:
            raise self.FORBIDDEN

        return None


get_rent_renter_or_owner = OnlyRentRenterOrOwner()

GetRentRenterOrOwner = Annotated[Rent, Depends(get_rent_renter_or_owner)]
