from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from data_access.db.models.booking import BookingStatus

class BookingCreate(BaseModel):
    tutor_id: UUID
    start_time: datetime
    duration_minutes: int


class BookingRead(BaseModel):
    id: UUID
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    student_id: UUID
    tutor_id: UUID
    status: BookingStatus

    class Config:
        from_attributes = True