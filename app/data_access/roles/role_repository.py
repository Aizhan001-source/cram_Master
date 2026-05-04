from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from data_access.db.models.role import Role


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Role]:
        stmt = select(Role)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, role_id: UUID) -> Role | None:
        stmt = select(Role).where(Role.id == role_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()