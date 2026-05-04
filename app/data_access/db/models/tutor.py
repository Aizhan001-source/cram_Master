from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from sqlalchemy import (Column, ForeignKey, String,Integer, CheckConstraint, Numeric, Text, TIMESTAMP, Table)

from data_access.db.base import Base

tutor_subjects = Table(
    "tutor_subjects",
    Base.metadata,
    Column("tutor_id", ForeignKey("tutors.id"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
)


class Tutor(Base):
    __tablename__ = "tutors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    bio = Column(String)
    experience_years = Column(Integer, default=0)

    price_per_hour = Column(Numeric(10, 2))
    currency = Column(String(10), default="KZT")

    average_rating = Column(Numeric(3, 2), default=0)
    total_reviews = Column(Integer, default=0)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="tutor")
    courses = relationship(
    "Course",
    back_populates="tutor",
    cascade="all, delete-orphan",
    passive_deletes=True
)
    education = relationship("Education", back_populates="tutors")

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    education_id = Column(UUID(as_uuid=True), ForeignKey("educations.id"), nullable=False, unique=True)

    
    __table_args__ = (
        CheckConstraint("experience_years >= 0", name="check_experience"),
    )

    subjects = relationship(
        "Subject",
        secondary="tutor_subjects",
        back_populates="tutors"
    )
