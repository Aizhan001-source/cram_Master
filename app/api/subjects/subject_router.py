from fastapi import APIRouter
from . import subject_router

router = APIRouter(
    prefix="/subjects",
)
router.include_router(
    subject_router.router,
    tags=["SUBJECTS"]
)