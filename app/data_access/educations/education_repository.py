from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from data_access.db.models.education import Education
from typing import List


class EducationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Education]:
        result = await self.db.execute(select(Education))
        return result.scalars().all()
    
    async def get_by_id(self, education_id: UUID) -> Education | None:
        result = await self.db.execute(
            select(Education).where(Education.id == education_id)
        )
        return result.scalar_one_or_none()