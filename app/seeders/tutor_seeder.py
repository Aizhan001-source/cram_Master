from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
import random

from data_access.db.models.tutor import Tutor
from data_access.db.models.user import User
from data_access.db.models.education import Education


async def seed_tutors(db: AsyncSession):
    users = (await db.execute(
        select(User).join(User.role).where(User.role.has(name="tutor"))
    )).scalars().all()

    educations = (await db.execute(select(Education))).scalars().all()

    if not educations:
        print("No educations found")
        return

    for user in users:
        result = await db.execute(
            select(Tutor).where(Tutor.user_id == user.id)
        )
        exists = result.scalar_one_or_none()

        if not exists:
            db.add(
                Tutor(
                    user_id=user.id,
                    education_id=random.choice(educations).id,
                    bio="Experienced tutor",
                    experience_years=random.randint(1, 10),
                    price_per_hour=Decimal("5000.00"),
                    currency="KZT",
                )
            )

    await db.commit()
    print("Tutors seeded!")