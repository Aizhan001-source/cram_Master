from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.session import get_db
from utils.auth_middleware import get_current_user

from data_access.payments.payment_repository import PaymentRepository
from data_access.bookings.booking_repository import BookingRepository
from business_logic.payments.payment_service import PaymentService

from api.payments.payment_schemas import PaymentRead, PaymentCreate

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> PaymentService:
    return PaymentService(
        PaymentRepository(db),
        BookingRepository(db)
    )


@router.post("/", response_model=PaymentRead)
async def create_payment(
    data: PaymentCreate,
    service: PaymentService = Depends(get_service),
    user: dict = Depends(get_current_user()),
):
    return await service.create(data, user["user_id"])


@router.get("/", response_model=list[PaymentRead])
async def my_payments(
    service: PaymentService = Depends(get_service),
    user: dict = Depends(get_current_user()),
):
    return await service.get_my(user["user_id"])


@router.get("/{payment_id}", response_model=PaymentRead)
async def get_payment(
    payment_id: UUID,
    service: PaymentService = Depends(get_service),
    user: dict = Depends(get_current_user()),
):
    return await service.get_by_id(payment_id, user["user_id"])