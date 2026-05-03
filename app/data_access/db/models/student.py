from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from sqlalchemy import (Column, ForeignKey)

from data_access.db.base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)

    bookings = relationship("Booking", back_populates="student")    
    user = relationship("User", back_populates="student")
