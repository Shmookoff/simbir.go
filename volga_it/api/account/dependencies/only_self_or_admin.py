from typing import Annotated, Any

from fastapi import Depends

from volga_it.dependencies import BaseDependency

from ..models import Account
from .account_by_id import AccountById
from .only_account import GetAccount


class OnlySelfOrAdmin(BaseDependency):
    def __call__(self, account: GetAccount, requested_account: AccountById) -> Any:
        if account.is_admin or account.id == requested_account.id:
            return requested_account

        if self.auto_error:
            raise self.FORBIDDEN

        return None


get_self_or_admin = OnlySelfOrAdmin()

GetSelfOrAdmin = Annotated[Account, Depends(get_self_or_admin)]
