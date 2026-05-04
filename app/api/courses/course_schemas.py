from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CourseBase(BaseModel):
    tutor_id: UUID
    subject_id: UUID
    is_active: bool = True


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class CourseResponse(BaseModel):
    course: CourseRead


class CourseListResponse(BaseModel):
    courses: list[CourseRead]


class DeleteCourseResponse(BaseModel):
    message: str