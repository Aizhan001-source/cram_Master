from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from business_logic.reviews.review_service import ReviewService
from api.reviews.review_schemas import (
    ReviewRead,
    ReviewCreate,
    ReviewWithRatingResponse,
    DeleteReviewResponse,
)
from data_access.db.session import get_db
from utils.auth_middleware import get_current_user

router = APIRouter()


def get_review_service(db: AsyncSession = Depends(get_db)) -> ReviewService:
    return ReviewService(db)


@router.get("/", response_model=list[ReviewRead])
async def get_all_reviews(
    service: ReviewService = Depends(get_review_service),
):
    return await service.get_all_reviews()


@router.get("/{review_id}", response_model=ReviewRead)
async def get_review_by_id(
    review_id: UUID,
    service: ReviewService = Depends(get_review_service),
    user=Depends(get_current_user(required_roles=["student", "tutor", "admin"])),
):
    return await service.get_review_by_id(review_id)


@router.post("/", response_model=ReviewWithRatingResponse)
async def create_review(
    data: ReviewCreate,
    service: ReviewService = Depends(get_review_service),
    user=Depends(get_current_user(required_roles=["student"])),
):
    return await service.create_review(data)


@router.delete("/{review_id}", response_model=DeleteReviewResponse)
async def delete_review(
    review_id: UUID,
    service: ReviewService = Depends(get_review_service),
    user=Depends(get_current_user(required_roles=["student"])),
):
    return await service.delete_review(review_id)

@router.get("/tutor/{tutor_id}", response_model=list[ReviewRead])
async def get_reviews_by_tutor(
    tutor_id: UUID,
    service: ReviewService = Depends(get_review_service),
):
    return await service.get_by_tutor_id(tutor_id)