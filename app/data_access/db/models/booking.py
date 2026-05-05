from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, TIMESTAMP, ForeignKey, Enum as SqlEnum, Integer

from data_access.db.base import Base


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)   
    duration_minutes = Column(Integer, nullable=True)

    # FK → users (студент)

    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # FK → tutors (профиль тьютора)

    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutors.id"), nullable=False)
    status = Column(
    SqlEnum(BookingStatus, name="booking_status_enum"),
    default=BookingStatus.pending,
    nullable=False
)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # relationships

    student = relationship(
        "User",
        foreign_keys=[student_id],
        back_populates="bookings"
    )

    tutor = relationship(
        "Tutor",
        foreign_keys=[tutor_id],
        back_populates="bookings"
    )
    payments = relationship("Payment", back_populates="booking", cascade="all, delete-orphan")