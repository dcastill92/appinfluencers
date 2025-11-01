"""
Payment model for tracking financial transactions.
Integrates with Stripe and manages platform commissions.
"""
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class PaymentStatus(str, enum.Enum):
    """Payment status enumeration."""
    PENDIENTE = "PENDIENTE"  # Payment initiated but not captured
    RETENIDO = "RETENIDO"  # Payment captured, held until campaign completion
    COMPLETADO = "COMPLETADO"  # Payment released to influencer
    REEMBOLSADO = "REEMBOLSADO"  # Payment refunded to empresa
    FALLIDO = "FALLIDO"  # Payment failed


class Payment(Base):
    """
    Payment model for tracking campaign payments.
    Handles Stripe integration and commission calculation.
    """
    __tablename__ = "payments"
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    campaign_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    empresa_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    influencer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Payment Details
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    platform_commission: Mapped[float] = mapped_column(Float, nullable=False)
    influencer_payout: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Stripe Integration
    stripe_payment_intent_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stripe_charge_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Status
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDIENTE,
        nullable=False,
        index=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Relationships
    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="payments")
    
    empresa: Mapped["User"] = relationship(
        "User",
        back_populates="payments_made",
        foreign_keys=[empresa_id]
    )
    
    influencer: Mapped["User"] = relationship(
        "User",
        back_populates="payments_received",
        foreign_keys=[influencer_id]
    )
    
    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, amount={self.amount}, status={self.status})>"
