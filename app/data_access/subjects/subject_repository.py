from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from data_access.db.models.subject import Subject


class SubjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_subjects(self) -> List[Subject]:
        result = await self.db.execute(
            select(Subject).options(
                selectinload(Subject.courses),
                selectinload(Subject.tutors),
            )
        )
        return result.scalars().all()

    async def get_subject_by_id(self, subject_id: UUID) -> Optional[Subject]:
        result = await self.db.execute(
            select(Subject)
            .where(Subject.id == subject_id)
            .options(
                selectinload(Subject.courses),
                selectinload(Subject.tutors),
            )
        )
        return result.scalar_one_or_none()

    async def create_subject(self, name: str) -> Subject:
        subject = Subject(name=name)

        self.db.add(subject)
        await self.db.commit()
        await self.db.refresh(subject)

        return subject