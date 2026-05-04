from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import (Column,  TIMESTAMP,  ForeignKey,  Enum as SqlEnum, String)

from data_access.db.base import Base


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE"), 
        nullable=False
    )
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id"), nullable=False)

    status = Column(String, default="pending")

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="bookings")
    schedule = relationship("Schedule", back_populates="bookings")   
    payments = relationship("Payment", back_populates="booking") 