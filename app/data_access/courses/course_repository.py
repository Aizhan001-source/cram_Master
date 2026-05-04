from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data_access.db.models.course import Course
from data_access.db.models.schedule import Schedule


class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_courses(self) -> List[Course]:
        result = await self.db.execute(
            select(Course).options(
                selectinload(Course.tutor),
                selectinload(Course.subject),
                selectinload(Course.schedules),
            )
        )
        return result.scalars().all()

    async def get_course_by_id(self, course_id: UUID) -> Optional[Course]:
        result = await self.db.execute(
            select(Course)
            .where(Course.id == course_id)
            .options(
                selectinload(Course.tutor),
                selectinload(Course.subject),
                selectinload(Course.schedules),
            )
        )
        return result.scalar_one_or_none()

    async def create_course(
        self,
        tutor_id: UUID,
        subject_id: UUID,
        is_active: bool = True,
    ) -> Course:
        course = Course(
            tutor_id=tutor_id,
            subject_id=subject_id,
            is_active=is_active,
        )

        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)

        return course

    async def delete_course(self, course_id: UUID):
        course = await self.get_course_by_id(course_id)

        if not course:
            return False

        await self.db.execute(
            delete(Schedule).where(Schedule.course_id == course_id)
        )

        await self.db.delete(course)
        await self.db.commit()

        return True