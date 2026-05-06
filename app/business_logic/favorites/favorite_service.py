from uuid import UUID
from fastapi import HTTPException


class FavoriteService:
    def __init__(self, repo, tutor_repo):
        self.repo = repo
        self.tutor_repo = tutor_repo

    async def add(self, student_id: UUID, tutor_id: UUID):
        tutor = await self.tutor_repo.get_tutor_by_id(tutor_id)

        if not tutor:
            raise HTTPException(404, "Tutor not found")

        exists = await self.repo.exists(student_id, tutor_id)

        if exists:
            return {"message": "already exists"}

        fav = await self.repo.add(student_id, tutor_id)

        await self.repo.db.commit()

        return fav

    async def remove(self, student_id: UUID, tutor_id: UUID):
        await self.repo.remove(student_id, tutor_id)

        await self.repo.db.commit()

        return {"message": "deleted"}

    async def get_my(self, student_id: UUID):
        return await self.repo.get_by_student(student_id)