from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


# 🔹 Создание студента
class StudentCreate(BaseModel):
    user_id: UUID


# 🔹 Короткий пользователь (для вложенности)
class UserShort(BaseModel):
    id: UUID
    first_name: Optional[str]
    last_name: Optional[str]
    avatar_url: Optional[str]

    model_config = {"from_attributes": True}


# 🔹 Основная схема студента
class StudentRead(BaseModel):
    id: UUID
    user_id: UUID

    # вложенный user (очень удобно для фронта)
    user: Optional[UserShort] = None

    model_config = {"from_attributes": True}


# 🔹 Список студентов (если хочешь отдельно)
class StudentList(BaseModel):
    students: list[StudentRead]


# 🔹 Для обновления (если понадобится)
class StudentUpdate(BaseModel):
    user_id: Optional[UUID] = None


# 🔹 Расширенная (например с датами, если добавишь потом)
class StudentDetail(BaseModel):
    id: UUID
    user_id: UUID
    user: Optional[UserShort] = None

    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}