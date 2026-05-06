from fastapi import APIRouter
from . import favorite_router

router = APIRouter()

router = APIRouter(
    prefix="/favorites",
)

router.include_router(
    favorite_router.router,
    tags=["favorites"],
)


