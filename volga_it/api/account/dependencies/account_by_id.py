from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from ..models import Account


def account_by_id(account_id: int = Path(gt=0)) -> Account:
    account = Account.find(account_id)
    if not account:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account Not Found")
    return account


AccountById = Annotated[Account, Depends(account_by_id)]
