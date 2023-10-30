from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from volga_it.dependencies import BaseDependency

from .. import controller as AccountController
from ..schemas import AccessTokenPayload, EncodedAccessToken


class OnlyAccessToken(BaseDependency):
    get_token = HTTPBearer(auto_error=False)

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
        creds: Annotated[HTTPAuthorizationCredentials | None, Depends(get_token)],
    ) -> AccessTokenPayload | None:
        if not creds:
            if self.auto_error:
                raise self.NOT_AUTHENTICATED
            return None

        access_token = EncodedAccessToken(creds.credentials)

        payload = AccountController.authenticate_by_access_token(access_token)

        if not payload:
            if self.auto_error:
                raise self.UNAUTHORIZED
            return None

        return payload


get_access_token = OnlyAccessToken()
