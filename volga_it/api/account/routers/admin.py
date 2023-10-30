from typing import Annotated

from fastapi import APIRouter, Depends, Query

from volga_it.api.admin.common import ADMIN_BASE_TAG, ADMIN_PREFIX

from .. import controller as AccountController
from ..dependencies import AccountById, get_admin
from ..schemas import (
    AccountAdminUpdateable,
    AccountList,
    AdminAccountCreate,
    AdminAccountUpdate,
)
from .common import PREFIX, TAG

router = APIRouter(
    prefix=ADMIN_PREFIX + PREFIX,
    tags=[ADMIN_BASE_TAG + TAG],
    dependencies=[Depends(get_admin)],
)


@router.get("", response_model=AccountList)
def list(start: Annotated[int, Query(gt=0)], count: Annotated[int, Query(gt=0)]):
    return AccountController.list(start, count)


@router.get("/{account_id}", response_model=AccountAdminUpdateable)
def read(account: AccountById):
    return AccountController.read(account)


@router.post("", response_model=AccountAdminUpdateable)
def create(data: AdminAccountCreate):
    return AccountController.create(data)


@router.put("/{account_id}", response_model=AccountAdminUpdateable)
def update(account: AccountById, data: AdminAccountUpdate):
    return AccountController.update(account, data)


@router.delete("/{account_id}")
def delete(account: AccountById):
    return AccountController.delete(account)
