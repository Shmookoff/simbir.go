from fastapi import APIRouter, status

from volga_it.api.account import GetSelfOrAdmin

from .. import controller as PaymentController

router = APIRouter(prefix="/Payment", tags=["PaymentController"])


@router.post("/Hesoyam/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def hesoyam(account: GetSelfOrAdmin):
    return PaymentController.hesoyam(account)
