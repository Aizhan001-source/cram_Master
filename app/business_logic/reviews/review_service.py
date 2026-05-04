from fastapi import HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.reviews.review_schemas import ReviewRead, ReviewCreate
from data_access.reviews.review_repository import ReviewRepository
from data_access.db.models.student import Student
from data_access.db.models.course import Course


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.repo = ReviewRepository(db)
        self.db = db

    async def get_all_reviews(self):
        reviews = await self.repo.get_all_reviews()

        return [
            ReviewRead(
                id=r.id,
                student_id=r.student_id,
                course_id=r.course_id,
                rating=r.rating,
                comment=r.comment,
                average_rating=0.0,  # нет avg в этом запросе
            )
            for r in reviews
        ]

    async def get_review_by_id(self, review_id: UUID):
        review = await self.repo.get_review_by_id(review_id)

        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        # отдельный запрос для avg
        rating_data = await self.repo.get_course_rating(review.course_id)

        return ReviewRead(
            id=review.id,
            student_id=review.student_id,
            course_id=review.course_id,
            rating=review.rating,
            comment=review.comment,
            average_rating=rating_data["average_rating"],
        )

    async def create_review(self, data: ReviewCreate):
        if not (1 <= data.rating <= 5):
            raise HTTPException(
                status_code=400,
                detail="Rating must be between 1 and 5",
            )

        student = await self.db.execute(
            select(Student).where(Student.id == data.student_id)
        )
        if not student.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Student not found")

        course = await self.db.execute(
            select(Course).where(Course.id == data.course_id)
        )
        if not course.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Course not found")

        if await self.repo.exists(data.student_id, data.course_id):
            raise HTTPException(
                status_code=400,
                detail="Review already exists for this student and course",
            )

        review = await self.repo.create_review(
            student_id=data.student_id,
            course_id=data.course_id,
            rating=data.rating,
            comment=data.comment,
        )

        rating_data = await self.repo.get_course_rating(data.course_id)

        return {
            "review": ReviewRead(
                id=review.id,
                student_id=review.student_id,
                course_id=review.course_id,
                rating=review.rating,
                comment=review.comment,
                average_rating=rating_data["average_rating"],
            ),
            "average_rating": rating_data["average_rating"],
            "total_reviews": rating_data["total_reviews"],
        }

    async def delete_review(self, review_id: UUID):
        success, rating_data = await self.repo.delete_review(review_id)

        if not success:
            raise HTTPException(status_code=404, detail="Review not found")

        return {
            "message": "Review deleted successfully",
            "average_rating": rating_data["average_rating"],
            "total_reviews": rating_data["total_reviews"],
        }