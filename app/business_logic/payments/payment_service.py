from uuid import UUID
from fastapi import HTTPException

from data_access.payments.payment_repository import PaymentRepository
from data_access.bookings.booking_repository import BookingRepository

class PaymentService:
    def __init__(self, payment_repo: PaymentRepository, booking_repo: BookingRepository):
        self.payment_repo = payment_repo
        self.booking_repo = booking_repo


    async def create(self, data, user_id: UUID):
        booking = await self.booking_repo.get_by_id(data.booking_id)

        if not booking or booking.student_id != user_id:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        return await self.payment_repo.create(
            booking_id=data.booking_id,
            amount=data.amount,
        )
    
    async def get_my(self, user_id: UUID):
        return await self.payment_repo.get_by_student(user_id)
    
    async def get_by_id(self, payment_id: UUID, user_id: UUID):
        payment = await self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Not found")
        
        if payment.booking.student_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        return payment