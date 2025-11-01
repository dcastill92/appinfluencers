"""
Repository for Payment model data access.
"""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment, PaymentStatus


class PaymentRepository:
    """Repository for Payment CRUD operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, payment: Payment) -> Payment:
        """Create a new payment."""
        self.db.add(payment)
        await self.db.flush()
        await self.db.refresh(payment)
        return payment
    
    async def get_by_id(self, payment_id: int) -> Optional[Payment]:
        """Get payment by ID."""
        result = await self.db.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_campaign(self, campaign_id: int) -> list[Payment]:
        """Get all payments for a campaign."""
        result = await self.db.execute(
            select(Payment).where(Payment.campaign_id == campaign_id)
        )
        return list(result.scalars().all())
    
    async def get_by_empresa(
        self,
        empresa_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list[Payment]:
        """Get payments made by an empresa."""
        result = await self.db.execute(
            select(Payment)
            .where(Payment.empresa_id == empresa_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_influencer(
        self,
        influencer_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list[Payment]:
        """Get payments received by an influencer."""
        result = await self.db.execute(
            select(Payment)
            .where(Payment.influencer_id == influencer_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def update(self, payment: Payment) -> Payment:
        """Update payment."""
        await self.db.flush()
        await self.db.refresh(payment)
        return payment
