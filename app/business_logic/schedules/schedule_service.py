from uuid import UUID
from fastapi import HTTPException

from data_access.schedules.schedule_repository import ScheduleRepository
from api.schedules.schedule_schemas import ScheduleCreate, ScheduleUpdate


class ScheduleService:
    def __init__(self, repo: ScheduleRepository):
        self.repo = repo

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, schedule_id: UUID):
        schedule = await self.repo.get_by_id(schedule_id)
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return schedule

    async def get_by_tutor(self, tutor_id: UUID):
        return await self.repo.get_by_tutor(tutor_id)

    async def get_by_course(self, course_id: UUID):
        return await self.repo.get_by_course(course_id)

    async def create(self, data: ScheduleCreate):
        if data.end_time <= data.start_time:
            raise HTTPException(
                status_code=400,
                detail="end_time must be after start_time"
            )
        return await self.repo.create(
            course_id=data.course_id,
            start_time=data.start_time,
            end_time=data.end_time,
        )

    async def update(self, schedule_id: UUID, data: ScheduleUpdate):
        schedule = await self.repo.get_by_id(schedule_id)
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return await self.repo.update(schedule_id, data.model_dump(exclude_none=True))

    async def delete(self, schedule_id: UUID):
        deleted = await self.repo.delete(schedule_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return {"message": "Schedule deleted successfully"}