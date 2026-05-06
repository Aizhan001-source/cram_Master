from uuid import UUID
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data_access.db.models.schedule import Schedule
from data_access.db.models.booking import Booking
from data_access.db.models.student import Student
from data_access.db.models.course import Course


def _load_options():
    return [
        selectinload(Schedule.course).selectinload(Course.subject),
        selectinload(Schedule.bookings).selectinload(Booking.student).selectinload(Student.user),
    ]


class ScheduleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Schedule]:
        result = await self.db.execute(
            select(Schedule).options(*_load_options())
        )
        return result.scalars().all()

    async def get_by_id(self, schedule_id: UUID) -> Optional[Schedule]:
        result = await self.db.execute(
            select(Schedule)
            .where(Schedule.id == schedule_id)
            .options(*_load_options())
        )
        return result.scalar_one_or_none()

    async def get_by_tutor(self, tutor_id: UUID) -> list[Schedule]:
        result = await self.db.execute(
            select(Schedule)
            .join(Course, Schedule.course_id == Course.id)
            .where(Course.tutor_id == tutor_id)
            .options(*_load_options())
        )
        return result.scalars().all()

    async def get_by_course(self, course_id: UUID) -> list[Schedule]:
        result = await self.db.execute(
            select(Schedule)
            .where(Schedule.course_id == course_id)
            .options(*_load_options())
        )
        return result.scalars().all()

    async def create(self, course_id: UUID, start_time, end_time) -> Schedule:
        schedule = Schedule(
            course_id=course_id,
            start_time=start_time,
            end_time=end_time,
            is_available=True,
        )
        self.db.add(schedule)
        await self.db.commit()
        await self.db.refresh(schedule)
        return await self.get_by_id(schedule.id)

    async def update(self, schedule_id: UUID, data: dict) -> Optional[Schedule]:
        schedule = await self.get_by_id(schedule_id)
        if not schedule:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(schedule, key, value)
        await self.db.commit()
        await self.db.refresh(schedule)
        return await self.get_by_id(schedule_id)

    async def delete(self, schedule_id: UUID) -> bool:
        schedule = await self.get_by_id(schedule_id)
        if not schedule:
            return False
        await self.db.delete(schedule)
        await self.db.commit()
        return True