from datetime import datetime
from typing import NewType

from pydantic import BaseModel, RootModel

from volga_it.schemas.api import APISchema


class AccountBase(APISchema):
    username: str


class AccountCreate(AccountBase):
    password: str


class AccountAdminUpdateable(AccountBase):
    is_admin: bool
    balance: float


class AccountRead(AccountAdminUpdateable):
    id: int


AccountList = RootModel[list[AccountRead]]


class AccountUpdate(AccountCreate):
    pass


class AdminAccountCreate(AccountCreate, AccountAdminUpdateable):
    pass


class AdminAccountUpdate(AccountUpdate, AccountAdminUpdateable):
    pass


AccountUsername = NewType("AccountUsername", str)
AccountPassword = NewType("AccountPassword", str)


class AccountAuthorizationCredentials(APISchema):
    username: AccountUsername
    password: AccountPassword


EncodedAccessToken = NewType("EncodedAccessToken", str)


class AccountToken(APISchema):
    access_token: EncodedAccessToken


class AccessTokenPayloadCreate(BaseModel):
    sub: str


class AccessTokenPayload(BaseModel):
    sub: str
    exp: datetime
    jti: str
