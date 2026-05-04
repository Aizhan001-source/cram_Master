from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.subject import Subject


async def seed_subjects(db: AsyncSession):
    subjects = ["Math", "Physics", "English", "Programming"]

    for name in subjects:
        result = await db.execute(
            select(Subject).where(Subject.name == name)
        )
        exists = result.scalar_one_or_none()

        if not exists:
            db.add(Subject(name=name))

    await db.commit()
    print("Subjects seeded!")