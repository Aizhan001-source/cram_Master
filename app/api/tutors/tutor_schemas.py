from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class SubjectRead(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


# ---- Tutor ----
class TutorBase(BaseModel):
    bio: Optional[str] = None
    experience_years: int = 0
    price_per_hour: Optional[Decimal] = None
    currency: str = "KZT"


class TutorCreate(TutorBase):
    user_id: UUID
    education_id: UUID
    subject_ids: Optional[List[UUID]] = []


class TutorUpdate(BaseModel):
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    price_per_hour: Optional[Decimal] = None
    currency: Optional[str] = None
    education_id: Optional[UUID] = None
    subject_ids: Optional[List[UUID]] = None


class TutorRead(TutorBase):
    id: UUID
    user_id: UUID
    education_id: UUID

    price_per_hour: Optional[Decimal] = None
    average_rating: Optional[Decimal] = 0

    created_at: datetime
    updated_at: datetime

    subjects: List[SubjectRead] = []

    class Config:
        from_attributes = True