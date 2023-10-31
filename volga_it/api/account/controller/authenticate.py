import secrets
from typing import NewType, Type, TypeVar

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from volga_it.settings import settings

from ..models import AccessToken, Account
from ..schemas import (
    AccessTokenPayload,
    AccountCreate,
    AccountPassword,
    AccountUpdate,
    AccountUsername,
    EncodedAccessToken,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_by_credentials(username: AccountUsername, password: AccountPassword):
    account = Account.first(Account.username == username)

    account_password = account.password if account else secrets.token_urlsafe()

    if pwd_context.verify(password, account_password):
        is_password_correct = True
    else:
        is_password_correct = False

    if account and is_password_correct:
        return account


def authenticate_by_access_token(access_token: EncodedAccessToken):
    try:
        decoded = jwt.decode(access_token, settings.JWT_ACCESS_SECRET)
        payload = AccessTokenPayload.model_validate(decoded)
    except (JWTError, ValidationError):
        return

    access_token_record = AccessToken.find(int(payload.jti))
    if not access_token_record:
        return

    return payload


DataT = TypeVar("DataT", bound=AccountCreate | AccountUpdate)


def process_new_data(data: DataT) -> DataT:
    data.password = pwd_context.hash(data.password)
    return data
