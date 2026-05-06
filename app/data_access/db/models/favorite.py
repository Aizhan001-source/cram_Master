from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from sqlalchemy import (Column,  TIMESTAMP, ForeignKey, UniqueConstraint)

from data_access.db.base import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutors.id"), nullable=False)
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # 🔥 FIX

    __table_args__ = (
        UniqueConstraint("student_id", "tutor_id", name="unique_favorite"),
    )

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    student = relationship("User") 
    tutor = relationship("Tutor")