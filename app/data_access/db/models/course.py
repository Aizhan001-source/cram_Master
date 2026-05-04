from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Boolean, TIMESTAMP, ForeignKey)

from data_access.db.base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tutor_id = Column(
    UUID(as_uuid=True),
    ForeignKey("tutors.id", ondelete="CASCADE"),
    nullable=False
)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    tutor = relationship("Tutor", back_populates="courses")
    subject = relationship("Subject", back_populates="courses")
    schedules = relationship(
    "Schedule",
    back_populates="course",
    cascade="all, delete-orphan",
    passive_deletes=True
)    
