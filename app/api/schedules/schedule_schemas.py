from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class ScheduleCreate(BaseModel):
    course_id: UUID
    start_time: datetime
    end_time: datetime


class ScheduleUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_available: Optional[bool] = None


class UserShort(BaseModel):
    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class StudentShort(BaseModel):
    id: UUID
    user: Optional[UserShort] = None

    class Config:
        from_attributes = True


class BookingShort(BaseModel):
    id: UUID
    status: str
    student: Optional[StudentShort] = None

    class Config:
        from_attributes = True


class SubjectShort(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


class CourseShort(BaseModel):
    id: UUID
    subject: Optional[SubjectShort] = None

    class Config:
        from_attributes = True


class ScheduleRead(BaseModel):
    id: UUID
    course_id: UUID
    start_time: datetime
    end_time: datetime
    is_available: bool
    course: Optional[CourseShort] = None
    bookings: list[BookingShort] = []

    class Config:
        from_attributes = True


StudentShort.model_rebuild()