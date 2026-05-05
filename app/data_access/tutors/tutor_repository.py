from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from data_access.db.models.tutor import Tutor
from data_access.db.models.subject import Subject


class TutorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_tutor(self, user_id, education_id):
        tutor = Tutor(
            user_id=user_id,
            education_id=education_id
        )

        self.db.add(tutor)

        # важно для получения id сразу
        await self.db.flush()

        return tutor

    async def get_all_tutors(self):
        result = await self.db.execute(
            select(Tutor).options(selectinload(Tutor.subjects))
        )
        return result.scalars().all()

    async def get_tutor_by_id(self, tutor_id):
        result = await self.db.execute(
            select(Tutor)
            .where(Tutor.id == tutor_id)
            .options(selectinload(Tutor.subjects))
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id):
        result = await self.db.execute(
            select(Tutor)
            .where(Tutor.user_id == user_id)
            .options(selectinload(Tutor.subjects))
        )
        return result.scalar_one_or_none()

    async def get_tutors_count(self):
        result = await self.db.execute(select(func.count(Tutor.id)))
        return result.scalar()

    async def update_tutor(self, tutor: Tutor, data: dict):
        for key, value in data.items():
            if hasattr(tutor, key) and value is not None:
                setattr(tutor, key, value)

        self.db.add(tutor)
        await self.db.commit()
        await self.db.refresh(tutor)
        return tutor

    async def delete_tutor(self, tutor: Tutor):
        await self.db.delete(tutor)
        await self.db.commit()

    async def update_tutor_subjects(self, tutor: Tutor, subject_ids: list):
        result = await self.db.execute(
            select(Subject).where(Subject.id.in_(subject_ids))
        )
        subjects = result.scalars().all()

        tutor.subjects = subjects

        self.db.add(tutor)
        await self.db.commit()
        await self.db.refresh(tutor)
        return tutor