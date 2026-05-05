from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from data_access.db.models.payment import Payment
from data_access.db.models.booking import Booking


class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, booking_id: UUID, amount: float):
        payment = Payment(
            booking_id=booking_id,
            amount=amount
        )
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def get_by_id(self, payment_id: UUID):
        result = await self.db.execute(
            select(Payment)
            .options(selectinload(Payment.booking))
            .where(Payment.id == payment_id)
        )
        return result.scalar_one_or_none()

    # 🔥 ГЛАВНЫЙ ФИКС — правильное имя метода
    async def get_by_student(self, student_id: UUID):
        result = await self.db.execute(
            select(Payment)
            .options(selectinload(Payment.booking))
            .join(Booking, Payment.booking_id == Booking.id)
            .where(Booking.student_id == student_id)
        )
        return result.scalars().all()

    async def get_by_booking(self, booking_id: UUID):
        result = await self.db.execute(
            select(Payment)
            .where(Payment.booking_id == booking_id)
            .order_by(Payment.created_at.desc())
        )
        return result.scalars().all()