from fastapi import HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from api.subjects.subject_schemas import SubjectCreate, SubjectRead
from data_access.subjects.subject_repository import SubjectRepository


class SubjectService:
    def __init__(self, db: AsyncSession):
        self.repo = SubjectRepository(db)

    async def get_all_subjects(self):
        subjects = await self.repo.get_all_subjects()

        return [
            SubjectRead(
                id=subject.id,
                name=subject.name,
            )
            for subject in subjects
        ]

    async def get_subject_by_id(self, subject_id: UUID):
        subject = await self.repo.get_subject_by_id(subject_id)

        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")

        return SubjectRead(
            id=subject.id,
            name=subject.name,
        )

    # 🔹 Создать subject
    async def create_subject(self, data: SubjectCreate):
        # проверка на уникальность имени (если хочешь строгость)
        existing = await self.repo.get_all_subjects()
        if any(s.name.lower() == data.name.lower() for s in existing):
            raise HTTPException(
                status_code=400,
                detail="Subject with this name already exists",
            )

        subject = await self.repo.create_subject(name=data.name)

        return SubjectRead(
            id=subject.id,
            name=subject.name,
        )