from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.review import Review
from data_access.db.models.student import Student
from data_access.db.models.course import Course


async def seed_reviews(db: AsyncSession):
    students = (await db.execute(select(Student))).scalars().all()
    courses = (await db.execute(select(Course))).scalars().all()

    for student in students:
        for course in courses[:1]:
            exists = await db.execute(
                select(Review).where(
                    Review.student_id == student.id,
                    Review.course_id == course.id
                )
            )

            if exists.scalar_one_or_none():
                continue

            db.add(Review(
                student_id=student.id,
                course_id=course.id,
                rating=5,
                comment="Excellent course!"
            ))

    await db.commit()