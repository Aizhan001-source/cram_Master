from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    receiver_id: UUID
    content: str


class UserShort(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None
    model_config = {"from_attributes": True}


class MessageRead(BaseModel):
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    content: str
    is_read: bool
    created_at: datetime
    model_config = {"from_attributes": True}


class ChatPreview(BaseModel):
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    content: str
    is_read: bool
    created_at: datetime
    sender: UserShort
    receiver: UserShort
    model_config = {"from_attributes": True}


class UnreadCountResponse(BaseModel):
    unread_count: int

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
