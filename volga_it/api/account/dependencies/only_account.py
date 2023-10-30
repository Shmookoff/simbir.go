from typing import Annotated

from fastapi import Depends, HTTPException, status

from volga_it.dependencies import BaseDependency

from ..models import Account
from ..schemas import AccessTokenPayload
from .only_access_token import OnlyAccessToken


class OnlyAccount(BaseDependency):
    get_access_token = OnlyAccessToken()

    NOT_AUTHENTICATED = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Not authenticated",
        {"WWW-Authenticate": "Bearer"},
    )

    UNAUTHORIZED = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    async def __call__(
        self,
        access_token: Annotated[AccessTokenPayload, Depends(get_access_token)],
    ) -> Account | None:
        account = Account.find(int(access_token.sub))

        if account:
            return account

        if self.auto_error:
            raise self.UNAUTHORIZED
        return None


get_account = OnlyAccount()

GetAccount = Annotated[Account, Depends(get_account)]
