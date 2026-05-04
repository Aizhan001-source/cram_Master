from fastapi import HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.courses.course_schemas import (
    CourseRead,
    CourseCreate,
)
from data_access.courses.course_repository import CourseRepository
from data_access.db.models.tutor import Tutor
from data_access.db.models.subject import Subject


class CourseService:
    def __init__(self, db: AsyncSession):
        self.repo = CourseRepository(db)
        self.db = db

    async def get_all_courses(self):
        courses = await self.repo.get_all_courses()

        return [
            CourseRead(
                id=course.id,
                tutor_id=course.tutor_id,
                subject_id=course.subject_id,
                is_active=course.is_active,
                created_at=course.created_at,
            )
            for course in courses
        ]

    async def get_course_by_id(self, course_id: UUID):
        course = await self.repo.get_course_by_id(course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        return CourseRead(
            id=course.id,
            tutor_id=course.tutor_id,
            subject_id=course.subject_id,
            is_active=course.is_active,
            created_at=course.created_at,
        )

    async def create_course(self, data: CourseCreate):
        tutor = await self.db.execute(
            select(Tutor).where(Tutor.id == data.tutor_id)
        )
        if not tutor.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Tutor not found")

        subject = await self.db.execute(
            select(Subject).where(Subject.id == data.subject_id)
        )
        if not subject.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Subject not found")

        if await self.repo.exists(data.tutor_id, data.subject_id):
            raise HTTPException(
                status_code=400,
                detail="Course already exists for this tutor and subject",
            )

        course = await self.repo.create_course(
            tutor_id=data.tutor_id,
            subject_id=data.subject_id,
            is_active=data.is_active,
        )

        return CourseRead(
            id=course.id,
            tutor_id=course.tutor_id,
            subject_id=course.subject_id,
            is_active=course.is_active,
            created_at=course.created_at,
        )

    async def delete_course(self, course_id: UUID):
        success = await self.repo.delete_course(course_id)

        if not success:
            raise HTTPException(status_code=404, detail="Course not found")

        return {
            "message": "Course deleted successfully"
        }