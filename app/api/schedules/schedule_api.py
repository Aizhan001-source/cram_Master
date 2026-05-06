from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.session import get_db
from data_access.schedules.schedule_repository import ScheduleRepository
from business_logic.schedules.schedule_service import ScheduleService
from api.schedules.schedule_schemas import ScheduleCreate, ScheduleUpdate, ScheduleRead

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> ScheduleService:
    return ScheduleService(ScheduleRepository(db))


@router.get("/", response_model=list[ScheduleRead])
async def get_all_schedules(service: ScheduleService = Depends(get_service)):
    return await service.get_all()


@router.get("/tutor/{tutor_id}", response_model=list[ScheduleRead])
async def get_schedules_by_tutor(tutor_id: UUID, service: ScheduleService = Depends(get_service)):
    return await service.get_by_tutor(tutor_id)


@router.get("/course/{course_id}", response_model=list[ScheduleRead])
async def get_schedules_by_course(course_id: UUID, service: ScheduleService = Depends(get_service)):
    return await service.get_by_course(course_id)


@router.get("/{schedule_id}", response_model=ScheduleRead)
async def get_schedule(schedule_id: UUID, service: ScheduleService = Depends(get_service)):
    return await service.get_by_id(schedule_id)


@router.post("/", response_model=ScheduleRead)
async def create_schedule(data: ScheduleCreate, service: ScheduleService = Depends(get_service)):
    return await service.create(data)


@router.patch("/{schedule_id}", response_model=ScheduleRead)
async def update_schedule(
    schedule_id: UUID,
    data: ScheduleUpdate,
    service: ScheduleService = Depends(get_service)
):
    return await service.update(schedule_id, data)


@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: UUID, service: ScheduleService = Depends(get_service)):
    return await service.delete(schedule_id)