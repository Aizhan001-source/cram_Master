from fastapi import APIRouter
from . import education_router

router = APIRouter(
    prefix="/educations",
)
router.include_router(
    education_router.router,
    tags=["EDUCATIONS"]
)