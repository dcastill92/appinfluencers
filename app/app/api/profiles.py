"""
Influencer profiles router with trial access control.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.profile_schemas import (
    InfluencerProfileCreate,
    InfluencerProfileUpdate,
    InfluencerProfileResponse
)
from app.repositories.profile_repository import ProfileRepository
from app.models.profile import InfluencerProfile
from app.api.dependencies import (
    get_current_user,
    get_current_influencer_user,
    check_trial_access
)

router = APIRouter(prefix="/profiles", tags=["Influencer Profiles"])


@router.post("/", response_model=InfluencerProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: InfluencerProfileCreate,
    current_user: User = Depends(get_current_influencer_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create influencer profile (Influencer only).
    
    Each influencer can only have one profile.
    """
    profile_repo = ProfileRepository(db)
    
    # Check if profile already exists
    existing_profile = await profile_repo.get_by_user_id(current_user.id)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user"
        )
    
    # Create profile
    profile = InfluencerProfile(
        user_id=current_user.id,
        **profile_data.model_dump()
    )
    
    profile = await profile_repo.create(profile)
    
    return profile


@router.get("/", response_model=list[InfluencerProfileResponse])
async def list_profiles(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all influencer profiles (Explorer/Search).
    
    For EMPRESA users in trial: Shows list but blocks detailed view.
    """
    profile_repo = ProfileRepository(db)
    profiles = await profile_repo.get_all(skip=skip, limit=limit)
    
    return profiles


@router.get("/test")
async def test_endpoint():
    """Test endpoint without dependencies"""
    return {"message": "Test successful", "status": "ok"}


@router.get("/me")
async def get_my_profile(
    access_token: str = Cookie(None)
):
    """
    Get own influencer profile (Influencer only).
    """
    from app.core.database import get_db
    from app.core.security import decode_access_token
    from app.services.auth_service import AuthService
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Decode token
    payload = decode_access_token(access_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    
    # Get DB session manually
    async for db in get_db():
        # Get user
        auth_service = AuthService(db)
        current_user = await auth_service.get_current_user(user_id)
        
        # Verificar que sea influencer
        if current_user.role != UserRole.INFLUENCER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only influencers can access this endpoint"
            )
        
        profile_repo = ProfileRepository(db)
        profile = await profile_repo.get_by_user_id(current_user.id)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found. Create one first."
            )
        
        # Convertir a dict manualmente
        return {
            "id": profile.id,
            "user_id": profile.user_id,
            "bio": profile.bio,
            "profile_picture_url": profile.profile_picture_url,
            "instagram_handle": profile.instagram_handle,
            "instagram_followers": profile.instagram_followers,
            "tiktok_handle": profile.tiktok_handle,
            "tiktok_followers": profile.tiktok_followers,
            "youtube_handle": profile.youtube_handle,
            "youtube_subscribers": profile.youtube_subscribers,
            "average_engagement_rate": profile.average_engagement_rate,
            "suggested_rate_per_post": profile.suggested_rate_per_post,
            "suggested_rate_per_story": profile.suggested_rate_per_story,
            "suggested_rate_per_video": profile.suggested_rate_per_video,
            "categories": profile.categories,
            "portfolio_items": profile.portfolio_items,
            "total_campaigns_completed": profile.total_campaigns_completed,
            "average_rating": profile.average_rating,
            "created_at": profile.created_at.isoformat() if profile.created_at else None,
            "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
        }


@router.get("/{profile_id}", response_model=InfluencerProfileResponse)
async def get_profile(
    profile_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(check_trial_access)
):
    """
    Get detailed influencer profile.
    
    **CRITICAL ENDPOINT**: Enforces 24-hour trial logic for EMPRESA users.
    
    Trial Rules:
    - First profile view during trial: ALLOWED
    - Second profile view during trial: BLOCKED (403)
    - After trial expiration: BLOCKED (402)
    - With subscription: ALLOWED
    """
    profile_repo = ProfileRepository(db)
    profile = await profile_repo.get_by_id(profile_id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile


@router.get("/user/{user_id}", response_model=InfluencerProfileResponse)
async def get_profile_by_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get influencer profile by user ID.
    """
    profile_repo = ProfileRepository(db)
    profile = await profile_repo.get_by_user_id(user_id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found for this user"
        )
    
    return profile


@router.put("/me", response_model=InfluencerProfileResponse)
async def update_my_profile(
    profile_data: InfluencerProfileUpdate,
    current_user: User = Depends(get_current_influencer_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update own influencer profile (Influencer only).
    """
    profile_repo = ProfileRepository(db)
    profile = await profile_repo.get_by_user_id(current_user.id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Create one first."
        )
    
    # Update fields
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    profile = await profile_repo.update(profile)
    
    return profile
