from typing import Annotated

from fastapi import APIRouter, Depends

from .. import controller as AccountController
from ..dependencies import GetAccount, get_access_token
from ..schemas import (
    AccessTokenPayload,
    AccountAdminUpdateable,
    AccountAuthorizationCredentials,
    AccountCreate,
    AccountToken,
    AccountUpdate,
)
from .common import PREFIX, TAG

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/Me", response_model=AccountAdminUpdateable)
def read_self(account: GetAccount):
    return AccountController.read(account)


@router.post("/SignIn", response_model=AccountToken)
def sign_in(data: AccountAuthorizationCredentials):
    return AccountController.sign_in(data)


@router.post("/SignUp", response_model=AccountAdminUpdateable)
def sign_up(data: AccountCreate):
    return AccountController.create(data)


@router.post("/SignOut")
def sign_out(access_token: Annotated[AccessTokenPayload, Depends(get_access_token)]):
    return AccountController.sign_out(access_token)


@router.put("/Update", response_model=AccountAdminUpdateable)
def update(account: GetAccount, data: AccountUpdate):
    return AccountController.update(account, data)
