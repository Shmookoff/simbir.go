from typing import Annotated

from fastapi import Depends

from volga_it.dependencies import BaseDependency

from ..models import Account
from .only_account import GetAccount


class OnlyAdmin(BaseDependency):
    async def __call__(self, account: GetAccount) -> Account | None:
        if account.is_admin:
            return account

        if self.auto_error:
            raise self.FORBIDDEN

        return None


get_admin = OnlyAdmin()

GetAdmin = Annotated[Account, Depends(get_admin)]
