from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt

from volga_it.settings import settings

from ..models import AccessToken
from ..schemas import (
    AccessTokenPayload,
    AccessTokenPayloadCreate,
    AccountAuthorizationCredentials,
    AccountToken,
    EncodedAccessToken,
)
from .authenticate import authenticate_by_credentials


def create_access_token(data: AccessTokenPayloadCreate):
    access_token_record = AccessToken.create()
    payload = AccessTokenPayload(
        sub=data.sub,
        exp=datetime.utcnow() + timedelta(seconds=settings.JWT_ACCESS_TTL_SECONDS),
        jti=str(access_token_record.id),
    )
    return EncodedAccessToken(
        jwt.encode(payload.model_dump(), settings.JWT_ACCESS_SECRET)
    )


def sign_in(data: AccountAuthorizationCredentials):
    account = authenticate_by_credentials(data.username, data.password)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AccountToken(
        access_token=create_access_token(AccessTokenPayloadCreate(sub=str(account.id)))
    )
