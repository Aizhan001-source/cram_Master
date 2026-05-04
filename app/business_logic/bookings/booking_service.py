from uuid import UUID
from datetime import datetime, timedelta
from fastapi import HTTPException

from data_access.bookings.booking_repository import BookingRepository
from data_access.tutors.tutor_repository import TutorRepository
from data_access.users.user_repository import UserRepository


class BookingService:
    def __init__(self, booking_repo: BookingRepository, tutor_repo: TutorRepository, user_repo: UserRepository):
        self.booking_repo = booking_repo
        self.tutor_repo = tutor_repo
        self.user_repo = user_repo

    async def create(
        self,
        student_id: UUID,
        tutor_id: UUID,
        start_time: datetime,
        duration_minutes: int
    ):
        tutor = await self.tutor_repo.get_tutor_by_id(tutor_id)
        if not tutor:
            raise HTTPException(status_code=404, detail="Tutor not found")

        student = await self.user_repo.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        if duration_minutes < 15 or duration_minutes > 180:
            raise HTTPException(status_code=400, detail="Invalid duration")

        if not start_time:
            raise HTTPException(status_code=400, detail="start_time is required")

        end_time = start_time + timedelta(minutes=duration_minutes)

        booking = await self.booking_repo.create(
            student_id=student_id,
            tutor_id=tutor_id,
            start_time=start_time,
            duration_minutes=duration_minutes,
            end_time=end_time,
        )

        await self.booking_repo.db.commit()
        await self.booking_repo.db.refresh(booking)

        return booking

    async def get_my(self, student_id: UUID):
        return await self.booking_repo.get_by_student(student_id)

    async def get_by_id(self, booking_id: UUID):
        booking = await self.booking_repo.get_by_id(booking_id)

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        return booking