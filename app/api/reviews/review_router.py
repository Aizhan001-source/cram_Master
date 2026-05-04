from fastapi import APIRouter
from . import review_router

router = APIRouter(
    prefix="/reviews",
)
router.include_router(
    review_router.router,
    tags=["REVIEWS"]
)