from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.booking import Booking, BookingStatus
from data_access.db.models.student import Student
from data_access.db.models.tutor import Tutor
from data_access.db.models.schedule import Schedule


async def seed_bookings(db: AsyncSession):

    students = (await db.execute(select(Student))).scalars().all()
    schedules = (await db.execute(select(Schedule))).scalars().all()

    if not students or not schedules:
        return

    for i, student in enumerate(students):
        schedule = schedules[i % len(schedules)]

        exists = (await db.execute(
            select(Booking).where(
                Booking.student_id == student.id,
                Booking.schedule_id == schedule.id
            )
        )).scalar_one_or_none()

        if exists:
            continue

        db.add(Booking(
            student_id=student.id,
            schedule_id=schedule.id,
            status=BookingStatus.pending
        ))

    await db.commit()