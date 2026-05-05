from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from data_access.db.models.role import Role


async def seed_roles(db: AsyncSession):
    roles = ["admin", "student", "tutor"]

    for name in roles:
        exists = await db.execute(select(Role).where(Role.name == name))
        if not exists.scalar_one_or_none():
            db.add(Role(name=name))

    await db.commit()