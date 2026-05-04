from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.student import Student
from data_access.db.models.user import User


async def seed_students(db: AsyncSession):
    users = (await db.execute(
        select(User).join(User.role).where(User.role.has(name="student"))
    )).scalars().all()

    for user in users:
        result = await db.execute(
            select(Student).where(Student.user_id == user.id)
        )
        exists = result.scalar_one_or_none()

        if not exists:
            db.add(Student(user_id=user.id))

    await db.commit()
    print("Students seeded!")