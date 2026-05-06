from pydantic import BaseModel
from uuid import UUID

class EducationRead(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True  # для SQLAlchemy (Pydantic v2)