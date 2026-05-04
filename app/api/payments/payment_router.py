from fastapi import APIRouter
from . import payment_api

router = APIRouter(
    prefix="/payments",
)
router.include_router(
    payment_api.router,
    tags=["payments"]
)