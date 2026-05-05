from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from api.payments.payment_schemas import PaymentRead, PaymentCreate
from business_logic.payments.payment_service import PaymentService
from data_access.payments.payment_repository import PaymentRepository
from data_access.bookings.booking_repository import BookingRepository
from data_access.db.session import get_db
from utils.auth_middleware import get_current_user

router = APIRouter()


def get_payment_service(db: AsyncSession = Depends(get_db)) -> PaymentService:
    return PaymentService(
        PaymentRepository(db),
        BookingRepository(db)
    )


@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
async def create_payment(
    data: PaymentCreate,
    service: PaymentService = Depends(get_payment_service),
    current_user=Depends(get_current_user(required_roles=["student", "admin", "tutor"]))
):
    return await service.create(data, current_user.id)


@router.get("/", response_model=list[PaymentRead])
async def my_payments(
    service: PaymentService = Depends(get_payment_service),
    current_user=Depends(get_current_user(required_roles=["student", "admin", "tutor"]))
):
    return await service.get_my(current_user.id)


@router.get("/{payment_id}", response_model=PaymentRead)
async def get_payment(
    payment_id: UUID,
    service: PaymentService = Depends(get_payment_service),
    current_user=Depends(get_current_user(required_roles=["student", "admin", "tutor"]))
):
    return await service.get_by_id(payment_id, current_user.id)