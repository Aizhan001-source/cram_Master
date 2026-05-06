from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from utils.auth_middleware import get_current_user
from data_access.db.session import get_db
from api.users.user_schemas import CurrentUser

from data_access.favorites.favorite_repository import FavoriteRepository
from data_access.tutors.tutor_repository import TutorRepository
from business_logic.favorites.favorite_service import FavoriteService

from api.tutors.tutor_schemas import TutorRead

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> FavoriteService:
    return FavoriteService(
        FavoriteRepository(db),
        TutorRepository(db)
    )


@router.post("/{tutor_id}")
async def add_favorite(
    tutor_id: UUID,
    service: FavoriteService = Depends(get_service),
    user: CurrentUser = Depends(get_current_user(required_roles=["student"]))
):
    return await service.add_favorite(user.id, tutor_id)


@router.delete("/{tutor_id}")
async def remove_favorite(
    tutor_id: UUID,
    service: FavoriteService = Depends(get_service),
    user: CurrentUser = Depends(get_current_user(required_roles=["student"]))
):
    return await service.remove_favorite(user.id, tutor_id)


@router.get("/", response_model=list[TutorRead])
async def get_my_favorites(
    service: FavoriteService = Depends(get_service),
    user: CurrentUser = Depends(get_current_user(required_roles=["student"]))
):
    return await service.get_my(user.id)