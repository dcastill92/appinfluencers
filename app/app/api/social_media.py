"""
Social Media API endpoints for syncing insights.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.services.social_media_service import SocialMediaService


router = APIRouter(prefix="/social-media", tags=["Social Media"])


class InstagramSyncRequest(BaseModel):
    """Request model for Instagram sync."""
    instagram_user_id: str
    access_token: str


class TikTokSyncRequest(BaseModel):
    """Request model for TikTok sync."""
    access_token: str


@router.post("/instagram/sync")
async def sync_instagram(
    request: InstagramSyncRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Sync Instagram insights for the current user's profile.
    
    Requires:
    - User must be an INFLUENCER
    - Must have an influencer profile
    - Valid Instagram Business Account ID
    - Valid Instagram access token
    """
    if current_user.role != "INFLUENCER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only influencers can sync Instagram insights"
        )
    
    if not current_user.influencer_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influencer profile not found"
        )
    
    service = SocialMediaService(db)
    
    try:
        insights = await service.sync_instagram_insights(
            profile_id=current_user.influencer_profile.id,
            instagram_user_id=request.instagram_user_id,
            access_token=request.access_token
        )
        
        return {
            "message": "Instagram insights synced successfully",
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/tiktok/sync")
async def sync_tiktok(
    request: TikTokSyncRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Sync TikTok insights for the current user's profile.
    
    Requires:
    - User must be an INFLUENCER
    - Must have an influencer profile
    - Valid TikTok access token
    """
    if current_user.role != "INFLUENCER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only influencers can sync TikTok insights"
        )
    
    if not current_user.influencer_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influencer profile not found"
        )
    
    service = SocialMediaService(db)
    
    try:
        insights = await service.sync_tiktok_insights(
            profile_id=current_user.influencer_profile.id,
            access_token=request.access_token
        )
        
        return {
            "message": "TikTok insights synced successfully",
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/config")
async def get_social_media_config():
    """
    Get public configuration for social media integrations.
    Returns App IDs but not secrets.
    """
    from app.core.config import settings
    
    return {
        "facebook_app_id": settings.FACEBOOK_APP_ID,
        "tiktok_client_key": settings.TIKTOK_CLIENT_KEY,
        "instagram_configured": bool(settings.INSTAGRAM_ACCESS_TOKEN or settings.FACEBOOK_APP_ID),
        "tiktok_configured": bool(settings.TIKTOK_CLIENT_KEY)
    }
