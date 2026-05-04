from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data_access.db.models.review import Review


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # 🔥 НОВЫЙ МЕТОД (БЫЛ ОТСУТСТВУЮЩИЙ)
    async def get_all_reviews(self):
        result = await self.db.execute(
            select(Review).options(
                selectinload(Review.student),
                selectinload(Review.course),
            )
        )
        return result.scalars().all()

    async def get_course_rating(self, course_id: UUID):
        result = await self.db.execute(
            select(
                func.avg(Review.rating).label("average_rating"),
                func.count(Review.id).label("total_reviews"),
            ).where(Review.course_id == course_id)
        )

        row = result.first()

        return {
            "average_rating": float(row.average_rating) if row.average_rating else 0.0,
            "total_reviews": row.total_reviews or 0,
        }

    async def get_review_by_id(self, review_id: UUID) -> Optional[Review]:
        result = await self.db.execute(
            select(Review)
            .where(Review.id == review_id)
            .options(
                selectinload(Review.student),
                selectinload(Review.course),
            )
        )
        return result.scalar_one_or_none()

    async def create_review(
        self,
        student_id: UUID,
        course_id: UUID,
        rating: int,
        comment: str | None = None,
    ) -> Review:
        review = Review(
            student_id=student_id,
            course_id=course_id,
            rating=rating,
            comment=comment,
        )

        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)

        return review

    async def delete_review(self, review_id: UUID):
        review = await self.get_review_by_id(review_id)

        if not review:
            return False, None

        course_id = review.course_id

        await self.db.delete(review)
        await self.db.commit()

        rating_data = await self.get_course_rating(course_id)

        return True, rating_data

    async def exists(self, student_id: UUID, course_id: UUID) -> bool:
        result = await self.db.execute(
            select(Review).where(
                Review.student_id == student_id,
                Review.course_id == course_id,
            )
        )
        return result.scalar_one_or_none() is not None