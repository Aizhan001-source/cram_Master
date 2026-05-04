from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from business_logic.courses.course_service import CourseService
from api.courses.course_schemas import (
    CourseRead,
    CourseCreate,
    CourseResponse,
    CourseListResponse,
    DeleteCourseResponse,
)
from data_access.db.session import get_db
from utils.auth_middleware import get_current_user

router = APIRouter()


def get_course_service(db: AsyncSession = Depends(get_db)) -> CourseService:
    return CourseService(db)


@router.get("/all", response_model=list[CourseRead])
async def get_all_courses(
    service: CourseService = Depends(get_course_service),
):
    return await service.get_all_courses()


@router.get("/by_id/{course_id}", response_model=CourseRead)
async def get_course_by_id(
    course_id: UUID,
    service: CourseService = Depends(get_course_service),
    user=Depends(get_current_user(required_roles=["student", "tutor", "admin"])),
):
    return await service.get_course_by_id(course_id)


@router.post("/create", response_model=CourseRead)
async def create_course(
    data: CourseCreate,
    service: CourseService = Depends(get_course_service),
    user=Depends(get_current_user(required_roles=["tutor", "admin"])),
):
    return await service.create_course(data)


@router.delete("/delete/{course_id}", response_model=DeleteCourseResponse)
async def delete_course(
    course_id: UUID,
    service: CourseService = Depends(get_course_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.delete_course(course_id)