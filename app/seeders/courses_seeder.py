from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.course import Course
from data_access.db.models.tutor import Tutor
from data_access.db.models.subject import Subject


async def seed_courses(db: AsyncSession):
    tutors = (await db.execute(select(Tutor))).scalars().all()
    subjects = (await db.execute(select(Subject))).scalars().all()

    if not tutors or not subjects:
        print("No tutors or subjects found!")
        return

    courses_data = [
        {"tutor": tutors[0], "subject": subjects[0]},
        {"tutor": tutors[0], "subject": subjects[1]},
        {"tutor": tutors[1] if len(tutors) > 1 else tutors[0], "subject": subjects[0]},
    ]

    for item in courses_data:
        result = await db.execute(
            select(Course).where(
                Course.tutor_id == item["tutor"].id,
                Course.subject_id == item["subject"].id
            )
        )
        exists = result.scalar_one_or_none()

        if not exists:
            db.add(
                Course(
                    tutor_id=item["tutor"].id,
                    subject_id=item["subject"].id,
                    is_active=True,
                )
            )

    await db.commit()
    print("Courses seeded!")