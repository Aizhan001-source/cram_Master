from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy import (Column, ForeignKey, Integer, TIMESTAMP)
from sqlalchemy.sql import func
from data_access.db.base import Base


class TutorAvailability(Base):
    __tablename__ = "tutor_availability"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutors.id"), primary_key=True)

    weekday = Column(Integer)

    start_time = Column(TIMESTAMP(timezone=True), server_default=func.now())
    end_time = Column(TIMESTAMP(timezone=True), server_default=func.now())