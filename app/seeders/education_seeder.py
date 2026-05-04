from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.education import Education


async def seed_educations(db: AsyncSession):
    educations_data = [
        {"name": "Bachelor"},
        {"name": "Master"},
        {"name": "PhD"},
        {"name": "College"},
    ]

    for item in educations_data:
        result = await db.execute(
            select(Education).where(Education.name == item["name"])
        )
        exists = result.scalar_one_or_none()

        if not exists:
            db.add(Education(name=item["name"]))

    await db.commit()
    print("Educations seeded!")