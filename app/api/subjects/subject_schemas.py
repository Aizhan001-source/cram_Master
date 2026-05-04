from pydantic import BaseModel
from uuid import UUID


class SubjectBase(BaseModel):
    name: str

class SubjectCreate(SubjectBase):
    pass

class SubjectRead(SubjectBase):
    id: UUID

    class Config:
        from_attributes = True

from typing import List


class CourseShort(BaseModel):
    id: UUID

    class Config:
        from_attributes = True


class TutorShort(BaseModel):
    id: UUID

    class Config:
        from_attributes = True


class SubjectWithRelations(SubjectRead):
    courses: List[CourseShort] = []
    tutors: List[TutorShort] = []