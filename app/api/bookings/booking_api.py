from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from utils.auth_middleware import get_current_user
from data_access.db.session import get_db
from api.users.user_schemas import CurrentUser

from data_access.bookings.booking_repository import BookingRepository
from data_access.tutors.tutor_repository import TutorRepository
from data_access.users.user_repository import UserRepository  
from business_logic.bookings.booking_service import BookingService

from api.bookings.booking_schemas import BookingRead, BookingCreate

router = APIRouter()



def get_service(db: AsyncSession = Depends(get_db)) -> BookingService:
    return BookingService(
        BookingRepository(db),
        TutorRepository(db),
        UserRepository(db)   
    )

@router.post("/", response_model=BookingRead, status_code=201)
async def create_booking(
    data: BookingCreate,
    service: BookingService = Depends(get_service),
    user: CurrentUser = Depends(get_current_user)
):
    return await service.create(
        user.id,
        data.tutor_id,
        data.start_time,
        data.duration_minutes
    )

@router.get("/", response_model=list[BookingRead])
async def get_my_bookings(
    service: BookingService = Depends(get_service),
    user: CurrentUser = Depends(get_current_user)
):
    return await service.get_my(user.id)