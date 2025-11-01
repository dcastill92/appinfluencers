"""
Payments router for handling campaign payments.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.schemas.payment_schemas import PaymentCreate, PaymentResponse
from app.services.payment_service import PaymentService
from app.api.dependencies import (
    get_current_user,
    get_current_empresa_user,
    get_current_admin_user
)

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_empresa_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a payment for a campaign (Empresa only).
    
    Payment is captured and held until campaign completion.
    Platform commission is calculated automatically.
    """
    payment_service = PaymentService(db)
    payment = await payment_service.create_payment(current_user, payment_data)
    
    return payment


@router.get("/", response_model=list[PaymentResponse])
async def list_my_payments(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List payments for current user.
    
    - EMPRESA: Payments made
    - INFLUENCER: Payments received
    """
    from app.repositories.payment_repository import PaymentRepository
    from app.models.user import UserRole
    
    payment_repo = PaymentRepository(db)
    
    if current_user.role == UserRole.EMPRESA:
        payments = await payment_repo.get_by_empresa(
            current_user.id, skip=skip, limit=limit
        )
    elif current_user.role == UserRole.INFLUENCER:
        payments = await payment_repo.get_by_influencer(
            current_user.id, skip=skip, limit=limit
        )
    else:
        # Admin can see all - implement if needed
        payments = []
    
    return payments


@router.post("/{payment_id}/complete", response_model=PaymentResponse)
async def complete_payment(
    payment_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Release payment to influencer (Admin only).
    
    Can only be done after campaign is marked as completed.
    """
    payment_service = PaymentService(db)
    payment = await payment_service.complete_payment(payment_id, current_user)
    
    return payment
