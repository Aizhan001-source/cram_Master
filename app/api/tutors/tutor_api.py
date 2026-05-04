from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.session import get_db
from data_access.tutors.tutor_repository import TutorRepository
from business_logic.tutors.tutor_service import TutorService

from api.tutors.tutor_schemas import TutorRead, TutorUpdate


router = APIRouter()


def get_tutor_service(db: AsyncSession = Depends(get_db)) -> TutorService:
    repo = TutorRepository(db)
    return TutorService(repo)


@router.get("/", response_model=list[TutorRead])
async def get_all_tutors(service: TutorService = Depends(get_tutor_service)):
    return await service.get_all_tutors()


@router.get("/{tutor_id}", response_model=TutorRead)
async def get_tutor_by_id(
    tutor_id: UUID,
    service: TutorService = Depends(get_tutor_service),
):
    try:
        return await service.get_tutor_by_id(tutor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user/{user_id}", response_model=TutorRead)
async def get_by_user_id(
    user_id: UUID,
    service: TutorService = Depends(get_tutor_service),
):
    tutor = await service.get_by_user_id(user_id)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")
    return tutor


@router.get("/count/")
async def get_tutors_count(service: TutorService = Depends(get_tutor_service)):
    return {"count": await service.get_tutors_count()}


@router.patch("/{tutor_id}", response_model=TutorRead)
async def update_tutor(
    tutor_id: UUID,
    data: TutorUpdate,
    service: TutorService = Depends(get_tutor_service),
):
    try:
        return await service.update_tutor(tutor_id, data.dict(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{tutor_id}")
async def delete_tutor(
    tutor_id: UUID,
    service: TutorService = Depends(get_tutor_service),
):
    try:
        await service.delete_tutor(tutor_id)
        return {"message": "Tutor deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))