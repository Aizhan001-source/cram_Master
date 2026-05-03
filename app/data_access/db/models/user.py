from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, Boolean, TIMESTAMP, ForeignKey)

from data_access.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    first_name = Column(String(100))
    last_name = Column(String(100))

    phone = Column(String(20))
    avatar_url = Column(String(255))

    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    last_seen_at = Column(TIMESTAMP, server_default=func.now())

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    role = relationship("Role", back_populates="users")
    
    role_id = Column(UUID(as_uuid=True),  ForeignKey("roles.id"), nullable=False)
    
    tutor = relationship("Tutor", back_populates="user", uselist=False)
    student = relationship("Student", back_populates="user", uselist=False)

    sent_messages =  relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages =  relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")