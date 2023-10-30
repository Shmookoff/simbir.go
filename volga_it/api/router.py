from fastapi import APIRouter

from .account.routers import router as account_router
from .payment.routers import router as payment_router
from .rent.routers import router as rent_router
from .transport.routers import router as transport_router

api_router = APIRouter(prefix="/api")
api_router.include_router(account_router)
api_router.include_router(transport_router)
api_router.include_router(rent_router)
api_router.include_router(payment_router)
