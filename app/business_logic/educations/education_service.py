from uuid import UUID
from fastapi import HTTPException
from data_access.educations.education_repository import EducationRepository


class EducationService:
    def __init__(self, repo: EducationRepository):
        self.repo = repo

    async def get_all_educations(self):
        return await self.repo.get_all()

    async def get_education_by_id(self, education_id: UUID):
        education = await self.repo.get_by_id(education_id)

        if not education:
            raise HTTPException(
                status_code=404,
                detail="Education not found"
            )

        return education