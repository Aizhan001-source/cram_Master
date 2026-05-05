from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from sqlalchemy.orm import selectinload

from data_access.db.models.booking import Booking


class BookingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, student_id, tutor_id, start_time, duration_minutes, end_time):
        booking = Booking(
            student_id=student_id,
            tutor_id=tutor_id,
            start_time=start_time,
            duration_minutes=duration_minutes,
            end_time=end_time,
        )

        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)

        return booking

    async def get_by_student(self, student_id: UUID):
        result = await self.db.execute(
            select(Booking).where(Booking.student_id == student_id)
        )
        return result.scalars().all()

    async def get_by_id(self, booking_id: UUID):
        result = await self.db.execute(
            select(Booking)
            .where(Booking.id == booking_id)
            .options(selectinload(Booking.student))  # optional
        )
        return result.scalar_one_or_none()