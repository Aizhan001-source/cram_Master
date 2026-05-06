from fastapi import APIRouter
from . import booking_api

router = APIRouter()

router = APIRouter(
    prefix="/bookings",
)

router.include_router(
    booking_api.router,
    tags=["bookings"],
)



