"""
Payment service for handling Stripe payments and platform commissions.
"""
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import stripe

from app.core.config import settings
from app.models.user import User, UserRole
from app.models.campaign import Campaign, CampaignStatus
from app.models.payment import Payment, PaymentStatus
from app.repositories.payment_repository import PaymentRepository
from app.repositories.campaign_repository import CampaignRepository
from app.schemas.payment_schemas import PaymentCreate

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    """Service for payment processing."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.payment_repo = PaymentRepository(db)
        self.campaign_repo = CampaignRepository(db)
    
    def calculate_commission(self, amount: float) -> tuple[float, float]:
        """
        Calculate platform commission and influencer payout.
        
        Args:
            amount: Total payment amount
            
        Returns:
            tuple: (commission, influencer_payout)
        """
        commission = amount * settings.PLATFORM_COMMISSION_RATE
        influencer_payout = amount - commission
        return commission, influencer_payout
    
    async def create_payment(
        self,
        empresa_user: User,
        payment_data: PaymentCreate
    ) -> Payment:
        """
        Create a payment for a campaign.
        
        Business Rules:
        - Only EMPRESA users can make payments
        - Campaign must exist and be ACTIVA
        - Payment is captured and held (RETENIDO) until campaign completion
        - Integrates with Stripe
        """
        # Verify empresa role
        if empresa_user.role != UserRole.EMPRESA:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only EMPRESA users can make payments"
            )
        
        # Get campaign
        campaign = await self.campaign_repo.get_by_id(payment_data.campaign_id)
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign not found"
            )
        
        # Verify authorization
        if campaign.empresa_id != empresa_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to pay for this campaign"
            )
        
        # Verify campaign status
        if campaign.status != CampaignStatus.ACTIVA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only pay for active campaigns"
            )
        
        # Calculate commission
        commission, influencer_payout = self.calculate_commission(payment_data.amount)
        
        # Create Stripe Payment Intent (for MVP, we'll use a mock)
        try:
            # In production, integrate with real Stripe
            payment_intent = await self._create_stripe_payment_intent(
                amount=payment_data.amount,
                payment_method_id=payment_data.stripe_payment_method_id
            )
            
            stripe_payment_intent_id = payment_intent.get("id")
            stripe_charge_id = payment_intent.get("charge_id")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment processing failed: {str(e)}"
            )
        
        # Create payment record
        payment = Payment(
            campaign_id=campaign.id,
            empresa_id=empresa_user.id,
            influencer_id=campaign.influencer_id,
            amount=payment_data.amount,
            platform_commission=commission,
            influencer_payout=influencer_payout,
            stripe_payment_intent_id=stripe_payment_intent_id,
            stripe_charge_id=stripe_charge_id,
            status=PaymentStatus.RETENIDO,  # Held until campaign completion
        )
        
        payment = await self.payment_repo.create(payment)
        
        return payment
    
    async def complete_payment(
        self,
        payment_id: int,
        admin_user: User
    ) -> Payment:
        """
        Release payment to influencer (after campaign completion).
        
        Business Rules:
        - Only ADMIN can release payments
        - Campaign must be FINALIZADA
        - Payment status changes to COMPLETADO
        """
        # Verify admin role
        if admin_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only ADMIN can release payments"
            )
        
        # Get payment
        payment = await self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        
        # Verify payment status
        if payment.status != PaymentStatus.RETENIDO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment not in held status"
            )
        
        # Get campaign
        campaign = await self.campaign_repo.get_by_id(payment.campaign_id)
        if campaign.status != CampaignStatus.FINALIZADA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campaign must be completed before releasing payment"
            )
        
        # Update payment status
        from datetime import datetime
        payment.status = PaymentStatus.COMPLETADO
        payment.completed_at = datetime.utcnow()
        payment = await self.payment_repo.update(payment)
        
        # In production, transfer funds to influencer via Stripe Connect
        
        return payment
    
    async def _create_stripe_payment_intent(
        self,
        amount: float,
        payment_method_id: Optional[str] = None
    ) -> dict:
        """
        Create a Stripe Payment Intent.
        
        For MVP, this is a mock implementation.
        In production, integrate with real Stripe API.
        """
        # Mock implementation for MVP
        # In production, use:
        # payment_intent = stripe.PaymentIntent.create(
        #     amount=int(amount * 100),  # Convert to cents
        #     currency="usd",
        #     payment_method=payment_method_id,
        #     confirm=True,
        # )
        
        return {
            "id": f"pi_mock_{int(amount * 100)}",
            "charge_id": f"ch_mock_{int(amount * 100)}",
            "status": "succeeded",
        }
