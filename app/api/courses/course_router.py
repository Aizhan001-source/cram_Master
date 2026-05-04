from fastapi import APIRouter
from . import course_router

router = APIRouter(
    prefix="/courses",
)
router.include_router(
    course_router.router,
    tags=["COURSES"]
)