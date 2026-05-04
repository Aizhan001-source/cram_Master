from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal

from data_access.db.models.payment import Payment, PaymentStatus
from data_access.db.models.booking import Booking
from data_access.db.models.course_student import CourseStudent


async def seed_payments(db: AsyncSession):
    bookings = (await db.execute(select(Booking))).scalars().all()
    course_students = (await db.execute(select(CourseStudent))).scalars().all()

    if not bookings or not course_students:
        print("Missing bookings or course_students")
        return

    for i, booking in enumerate(bookings):
        course_student = course_students[i % len(course_students)]

        db.add(
            Payment(
                course_student_id=course_student.id,
                booking_id=booking.id,
                amount=Decimal("100.00"),
                status=PaymentStatus.completed.value if i % 2 == 0 else PaymentStatus.pending.value,
            )
        )

    await db.commit()
    print("Payments seeded!")