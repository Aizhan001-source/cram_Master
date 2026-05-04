from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from business_logic.subjects.subject_service import SubjectService
from api.subjects.subject_schemas import (
    SubjectRead,
    SubjectCreate,
)
from data_access.db.session import get_db
from utils.auth_middleware import get_current_user

router = APIRouter()


def get_subject_service(db: AsyncSession = Depends(get_db)) -> SubjectService:
    return SubjectService(db)


@router.get("/all", response_model=list[SubjectRead])
async def get_all_subjects(
    service: SubjectService = Depends(get_subject_service),
):
    return await service.get_all_subjects()


@router.get("/by_id/{subject_id}", response_model=SubjectRead)
async def get_subject_by_id(
    subject_id: UUID,
    service: SubjectService = Depends(get_subject_service),
    user=Depends(get_current_user(required_roles=["student", "tutor", "admin"])),
):
    return await service.get_subject_by_id(subject_id)


@router.post("/create", response_model=SubjectRead)
async def create_subject(
    data: SubjectCreate,
    service: SubjectService = Depends(get_subject_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    return await service.create_subject(data)