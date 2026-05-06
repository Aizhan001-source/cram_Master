from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.favorite import Favorite
from data_access.db.models.student import Student
from data_access.db.models.tutor import Tutor


async def seed_favorites(db: AsyncSession):

    students = (await db.execute(select(Student))).scalars().all()
    tutors = (await db.execute(select(Tutor))).scalars().all()

    if not students or not tutors:
        return

    for i, student in enumerate(students):
        tutor = tutors[i % len(tutors)]

        exists = (await db.execute(
            select(Favorite).where(
                and_(
                    Favorite.student_id == student.id,
                    Favorite.tutor_id == tutor.id
                )
            )
        )).scalar_one_or_none()

        if exists:
            continue

        db.add(Favorite(
            student_id=student.id,
            tutor_id=tutor.id
        ))

    await db.commit()