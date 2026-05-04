from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.booking import Booking
from data_access.db.models.student import Student
from data_access.db.models.schedule import Schedule
from data_access.db.models.booking import BookingStatus


async def seed_bookings(db: AsyncSession):

    students = (await db.execute(select(Student))).scalars().all()
    schedules = (await db.execute(select(Schedule))).scalars().all()

    if not students or not schedules:
        print("No students or schedules found!")
        return

    statuses = [
        BookingStatus.pending.value,
        BookingStatus.confirmed.value,
        BookingStatus.completed.value,
    ]

    for i, student in enumerate(students):
        schedule = schedules[i % len(schedules)]

        # проверка на существование
        result = await db.execute(
            select(Booking).where(
                Booking.student_id == student.id,
                Booking.schedule_id == schedule.id
            )
        )
        exists = result.scalar_one_or_none()

        if not exists:
            db.add(
                Booking(
                    student_id=student.id,
                    schedule_id=schedule.id,
                    status=statuses[i % len(statuses)],
                )
            )

    await db.commit()
    print("Bookings seeded!")