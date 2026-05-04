from uuid import UUID
from typing import Optional

from sqlalchemy import select, delete

from data_access.tutors.tutor_repository import TutorRepository
from data_access.db.models.tutor import Tutor
from data_access.db.models.course import Course
from data_access.db.models.favorite import Favorite


class TutorService:
    def __init__(self, repo: TutorRepository):
        self.repo = repo

    async def get_all_tutors(self):
        return await self.repo.get_all_tutors()

    async def get_tutor_by_id(self, tutor_id: UUID) -> Tutor:
        tutor = await self.repo.get_tutor_by_id(tutor_id)
        if not tutor:
            raise ValueError("Tutor not found")
        return tutor

    async def get_by_user_id(self, user_id: UUID) -> Optional[Tutor]:
        return await self.repo.get_by_user_id(user_id)

    async def get_tutors_count(self) -> int:
        return await self.repo.get_tutors_count()

    async def update_tutor(self, tutor_id: UUID, data: dict) -> Tutor:
        tutor = await self.repo.get_tutor_by_id(tutor_id)
        if not tutor:
            raise ValueError("Tutor not found")

        subject_ids = data.pop("subject_ids", None)

        updated_tutor = await self.repo.update_tutor(tutor, data)

        if subject_ids is not None:
            updated_tutor = await self.repo.update_tutor_subjects(
                updated_tutor,
                subject_ids
            )

        return updated_tutor

    async def delete_tutor(self, tutor_id: UUID):
        tutor = await self.repo.get_tutor_by_id(tutor_id)
        if not tutor:
            raise ValueError("Tutor not found")

        session = self.repo.db

        # 1. delete favorites
        course_ids = await session.execute(
            select(Course.id).where(Course.tutor_id == tutor_id)
        )
        course_ids = course_ids.scalars().all()

        if course_ids:
            await session.execute(
                delete(Favorite).where(Favorite.course_id.in_(course_ids))
            )

        # 2. delete courses
        await session.execute(
            delete(Course).where(Course.tutor_id == tutor_id)
        )

        # 3. delete tutor
        await self.repo.delete_tutor(tutor)

        await session.commit()