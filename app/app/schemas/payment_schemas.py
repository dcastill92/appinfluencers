"""
Pydantic schemas for payments.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from app.models.payment import PaymentStatus


class PaymentCreate(BaseModel):
    """Schema for creating a payment."""
    campaign_id: int
    amount: float = Field(..., gt=0)
    stripe_payment_method_id: Optional[str] = None


class PaymentResponse(BaseModel):
    """Schema for payment response."""
    id: int
    campaign_id: int
    empresa_id: int
    influencer_id: int
    amount: float
    platform_commission: float
    influencer_payout: float
    stripe_payment_intent_id: Optional[str] = None
    stripe_charge_id: Optional[str] = None
    status: PaymentStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
