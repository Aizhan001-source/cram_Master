from pydantic import BaseModel
from uuid import UUID


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