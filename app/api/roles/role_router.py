from fastapi import APIRouter
from . import role_router

router = APIRouter(
    prefix="/roles",
)
router.include_router(
    role_router.router,
    tags=["roles"]
)