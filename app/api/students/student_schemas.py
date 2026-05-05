from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

from api.users.user_schemas import UserRead


class StudentCreate(BaseModel):
    user_id: UUID


class UserShort(BaseModel):
    id: UUID
    first_name: Optional[str]
    last_name: Optional[str]
    avatar_url: Optional[str]

    model_config = {"from_attributes": True}

class StudentRead(BaseModel):
    id: UUID
    user: UserRead | None

    model_config = {"from_attributes": True}
class StudentList(BaseModel):
    students: list[StudentRead]


class StudentUpdate(BaseModel):
    user_id: Optional[UUID] = None


class StudentDetail(BaseModel):
    id: UUID
    user_id: UUID
    user: Optional[UserShort] = None

    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class StudentListResponse(BaseModel):
    count: int

    model_config = {"from_attributes": True}