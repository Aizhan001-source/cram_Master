from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from data_access.db.session import get_db
from data_access.educations.education_repository import EducationRepository
from business_logic.educations.education_service import EducationService
from api.educations.education_schemas import EducationRead

router = APIRouter()

@router.get("/", response_model=List[EducationRead])
async def get_all_educations(
    db: AsyncSession = Depends(get_db)
):
    repo = EducationRepository(db)
    service = EducationService(repo)

    return await service.get_all_educations()


@router.get("/{education_id}", response_model=EducationRead)
async def get_education_by_id(
    education_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    repo = EducationRepository(db)
    service = EducationService(repo)

    return await service.get_education_by_id(education_id)