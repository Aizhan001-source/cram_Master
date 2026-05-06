from fastapi import APIRouter
from . import student_api

router = APIRouter(prefix="/schedule")
router.include_router(student_api.router, tags=["SCHEDULE"])