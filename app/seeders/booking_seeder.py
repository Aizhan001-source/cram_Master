from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.booking import Booking, BookingStatus
from data_access.db.models.student import Student
from data_access.db.models.tutor import Tutor


async def seed_bookings(db: AsyncSession):

    students = (await db.execute(select(Student))).scalars().all()
    tutors = (await db.execute(select(Tutor))).scalars().all()

    if not students or not tutors:
        return

    base_time = datetime.now(timezone.utc)

    for i, student in enumerate(students):
        tutor = tutors[i % len(tutors)]

        exists = (await db.execute(
            select(Booking).where(
                Booking.student_id == student.id,
                Booking.tutor_id == tutor.id
            )
        )).scalar_one_or_none()

        if exists:
            continue

        start_time = base_time + timedelta(days=i)
        duration = 60

        db.add(Booking(
            student_id=student.id,
            tutor_id=tutor.id,
            start_time=start_time,
            duration_minutes=duration,
            end_time=start_time + timedelta(minutes=duration),
            status=BookingStatus.pending
        ))

    await db.commit()