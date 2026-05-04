from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.payment import Payment, PaymentStatus
from data_access.db.models.booking import Booking


async def seed_payments(db: AsyncSession):

    bookings = (await db.execute(select(Booking))).scalars().all()

    if not bookings:
        raise Exception("No bookings found")

    for booking in bookings:

        exists = (await db.execute(
            select(Payment).where(Payment.booking_id == booking.id)
        )).scalar_one_or_none()

        if exists:
            continue

        db.add(Payment(
            booking_id=booking.id,
            amount=5000, 
            status=PaymentStatus.pending
        ))

    await db.commit()