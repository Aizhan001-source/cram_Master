from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class UserShort(BaseModel):
    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class StudentShort(BaseModel):
    id: UUID
    user: Optional[UserShort] = None

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    rating: int
    comment: str | None = None


class ReviewCreate(ReviewBase):
    student_id: UUID
    course_id: UUID


class ReviewRead(ReviewBase):
    id: UUID
    student_id: UUID
    course_id: UUID
    average_rating: float | None = None
    created_at: Optional[datetime] = None
    student: Optional[StudentShort] = None

    class Config:
        from_attributes = True


class ReviewWithRatingResponse(BaseModel):
    review: ReviewRead
    average_rating: float
    total_reviews: int


class DeleteReviewResponse(BaseModel):
    message: str
    average_rating: float
    total_reviews: int