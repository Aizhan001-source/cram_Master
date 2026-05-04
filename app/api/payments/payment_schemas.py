from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class PaymentCreate(BaseModel):
    booking_id: UUID
    amount: Decimal


class PaymentRead(BaseModel):
    id: UUID
    booking_id: UUID
    amount: Decimal
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}