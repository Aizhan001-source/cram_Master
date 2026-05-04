from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.favorite import Favorite
from data_access.db.models.student import Student
from data_access.db.models.course import Course


async def seed_favorites(db: AsyncSession):

    students = (await db.execute(select(Student))).scalars().all()
    courses = (await db.execute(select(Course))).scalars().all()

    if not students or not courses:
        return

    for i, student in enumerate(students):
        course = courses[i % len(courses)]

        exists = (await db.execute(
            select(Favorite).where(
                and_(
                    Favorite.student_id == student.id,
                    Favorite.course_id == course.id
                )
            )
        )).scalar_one_or_none()

        if exists:
            continue

        db.add(Favorite(
            student_id=student.id,
            course_id=course.id
        ))

    await db.commit()