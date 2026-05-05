from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, TIMESTAMP,  ForeignKey,  Enum as SqlEnum, Numeric)

from sqlalchemy.orm import relationship
from data_access.db.base import Base


class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)

    status = Column(
        SqlEnum(PaymentStatus, name="payment_status_enum"),
        default=PaymentStatus.pending,
        nullable=False
    )
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    booking = relationship("Booking", back_populates="payments")