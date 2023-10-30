from fastapi import APIRouter

from volga_it.api.account import GetSelfOrAdmin

from .. import controller as PaymentController

router = APIRouter(prefix="/Payment", tags=["PaymentController"])


@router.post("/Hesoyam/{account_id}")
def hesoyam(account: GetSelfOrAdmin):
    return PaymentController.hesoyam(account)
