from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.course import Course
from data_access.db.models.tutor import Tutor
from data_access.db.models.subject import Subject


async def seed_courses(db: AsyncSession):
    courses_data = [
        {"tutor_email": "alice@example.com", "subject": "Math"},
        {"tutor_email": "bob@example.com", "subject": "Physics"},
    ]

    for c in courses_data:
        tutor = await db.execute(
            select(Tutor).join(Tutor.user).where(
                Tutor.user.has(email=c["tutor_email"])
            )
        )
        tutor = tutor.scalar_one_or_none()

        subject = await db.execute(
            select(Subject).where(Subject.name == c["subject"])
        )
        subject = subject.scalar_one_or_none()

        if not tutor or not subject:
            continue

        exists = await db.execute(
            select(Course).where(
                Course.tutor_id == tutor.id,
                Course.subject_id == subject.id
            )
        )

        if exists.scalar_one_or_none():
            continue

        db.add(Course(
            tutor_id=tutor.id,
            subject_id=subject.id,
            is_active=True
        ))

    await db.commit()