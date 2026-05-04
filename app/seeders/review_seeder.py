from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import random

from data_access.db.models.review import Review
from data_access.db.models.student import Student
from data_access.db.models.course import Course


async def seed_reviews(db: AsyncSession):
    students = (await db.execute(select(Student))).scalars().all()
    courses = (await db.execute(select(Course))).scalars().all()

    if not students or not courses:
        print("No students or courses found")
        return

    comments = [
        "Great course!",
        "Very useful",
        "Amazing tutor",
        "Could be better",
        "Excellent explanation",
    ]

    for i, student in enumerate(students):
        course = courses[i % len(courses)]

        result = await db.execute(
            select(Review).where(
                Review.student_id == student.id,
                Review.course_id == course.id,
            )
        )
        exists = result.scalar_one_or_none()

        if not exists:
            db.add(
                Review(
                    student_id=student.id,
                    course_id=course.id,
                    rating=random.randint(3, 5),
                    comment=random.choice(comments),
                )
            )

    await db.commit()
    print("Reviews seeded!")