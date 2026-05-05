from uuid import UUID
from datetime import datetime, timedelta
from fastapi import HTTPException

from data_access.bookings.booking_repository import BookingRepository
from data_access.tutors.tutor_repository import TutorRepository
from data_access.users.user_repository import UserRepository


class BookingService:
    def __init__(
        self,
        booking_repo: BookingRepository,
        tutor_repo: TutorRepository,
        user_repo: UserRepository
    ):
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
        # 1. Tutor check
        tutor = await self.tutor_repo.get_tutor_by_id(tutor_id)
        if not tutor:
            raise HTTPException(status_code=404, detail="Tutor not found")

        # 2. Student check
        student = await self.user_repo.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # 3. Validation (қатаң)
        if duration_minutes is None:
            raise HTTPException(status_code=400, detail="duration is required")

        if not (15 <= duration_minutes <= 180):
            raise HTTPException(status_code=400, detail="duration must be 15-180 minutes")

        if start_time is None:
            raise HTTPException(status_code=400, detail="start_time is required")

        # 4. Time calc
        end_time = start_time + timedelta(minutes=duration_minutes)

        # 5. Create booking (commit repo ішінде болуы керек)
        booking = await self.booking_repo.create(
            student_id=student_id,
            tutor_id=tutor_id,
            start_time=start_time,
            duration_minutes=duration_minutes,
            end_time=end_time,
        )

        return booking

    async def get_my(self, student_id: UUID):
        return await self.booking_repo.get_by_student(student_id)

    async def get_by_id(self, booking_id: UUID):
        booking = await self.booking_repo.get_by_id(booking_id)

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        return booking