from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.api.tutors.tutor_schemas import TutorRead

class FavoriteCreate(BaseModel):
    tutor_id: UUID

class FavoriteRead(BaseModel):
    id: UUID
    tutor_id: UUID
    student_id: UUID
    tutor: TutorRead
    created_at: datetime

    model_config = {"from_attributes": True}