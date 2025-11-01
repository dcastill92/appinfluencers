"""
Service for syncing social media insights from Instagram and TikTok APIs.
"""
import requests
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.profile import InfluencerProfile
from app.repositories.profile_repository import ProfileRepository


class SocialMediaService:
    """Service for managing social media integrations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.profile_repo = ProfileRepository(db)
    
    async def sync_instagram_insights(
        self,
        profile_id: int,
        instagram_user_id: str,
        access_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sync Instagram insights for a profile.
        
        Args:
            profile_id: ID of the influencer profile
            instagram_user_id: Instagram Business Account ID
            access_token: User's Instagram access token (optional, uses app token if not provided)
        
        Returns:
            Dictionary with synced insights
        """
        # Use provided token or fall back to app token
        token = access_token or settings.INSTAGRAM_ACCESS_TOKEN
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Instagram access token not configured"
            )
        
        try:
            # Get profile from database
            profile = await self.profile_repo.get_by_id(profile_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            # Fetch user info
            user_response = requests.get(
                f"https://graph.facebook.com/v18.0/{instagram_user_id}",
                params={
                    "fields": "followers_count,follows_count,media_count",
                    "access_token": token
                },
                timeout=10
            )
            
            if user_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Instagram API error: {user_response.text}"
                )
            
            user_data = user_response.json()
            
            # Fetch insights
            insights_response = requests.get(
                f"https://graph.facebook.com/v18.0/{instagram_user_id}/insights",
                params={
                    "metric": "impressions,reach,profile_views,website_clicks",
                    "period": "day",
                    "access_token": token
                },
                timeout=10
            )
            
            insights_data = {}
            if insights_response.status_code == 200:
                insights_raw = insights_response.json()
                for metric in insights_raw.get("data", []):
                    metric_name = metric.get("name")
                    values = metric.get("values", [])
                    if values:
                        # Get the most recent value
                        insights_data[metric_name] = values[-1].get("value", 0)
            
            # Fetch recent media
            media_response = requests.get(
                f"https://graph.facebook.com/v18.0/{instagram_user_id}/media",
                params={
                    "fields": "id,like_count,comments_count,media_url,media_type,timestamp",
                    "limit": 25,
                    "access_token": token
                },
                timeout=10
            )
            
            media_data = []
            avg_likes = 0
            avg_comments = 0
            
            if media_response.status_code == 200:
                media_raw = media_response.json()
                media_items = media_raw.get("data", [])
                
                if media_items:
                    total_likes = sum(item.get("like_count", 0) for item in media_items)
                    total_comments = sum(item.get("comments_count", 0) for item in media_items)
                    avg_likes = total_likes // len(media_items)
                    avg_comments = total_comments // len(media_items)
                    
                    # Get top 3 posts by engagement
                    sorted_media = sorted(
                        media_items,
                        key=lambda x: x.get("like_count", 0) + x.get("comments_count", 0),
                        reverse=True
                    )[:3]
                    
                    media_data = [
                        {
                            "id": item.get("id"),
                            "likes": item.get("like_count", 0),
                            "comments": item.get("comments_count", 0),
                            "image_url": item.get("media_url", "")
                        }
                        for item in sorted_media
                        if item.get("media_type") in ["IMAGE", "CAROUSEL_ALBUM"]
                    ]
            
            # Calculate engagement rate
            followers = user_data.get("followers_count", 0)
            engagement_rate = 0
            if followers > 0:
                engagement_rate = ((avg_likes + avg_comments) / followers) * 100
            
            # Build insights object
            instagram_insights = {
                "followers": followers,
                "following": user_data.get("follows_count", 0),
                "posts_count": user_data.get("media_count", 0),
                "engagement_rate": round(engagement_rate, 2),
                "avg_likes": avg_likes,
                "avg_comments": avg_comments,
                "reach": insights_data.get("reach", 0),
                "impressions": insights_data.get("impressions", 0),
                "profile_views": insights_data.get("profile_views", 0),
                "website_clicks": insights_data.get("website_clicks", 0),
                "top_posts": media_data
            }
            
            # Update profile
            profile.instagram_insights = instagram_insights
            profile.instagram_followers = followers
            profile.average_engagement_rate = engagement_rate
            
            await self.db.commit()
            await self.db.refresh(profile)
            
            return instagram_insights
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Error connecting to Instagram API: {str(e)}"
            )
    
    async def sync_tiktok_insights(
        self,
        profile_id: int,
        access_token: str
    ) -> Dict[str, Any]:
        """
        Sync TikTok insights for a profile.
        
        Args:
            profile_id: ID of the influencer profile
            access_token: User's TikTok access token
        
        Returns:
            Dictionary with synced insights
        """
        if not settings.TIKTOK_CLIENT_KEY:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="TikTok API not configured"
            )
        
        try:
            # Get profile from database
            profile = await self.profile_repo.get_by_id(profile_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            # Fetch user info
            user_response = requests.get(
                "https://open.tiktokapis.com/v2/user/info/",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                params={
                    "fields": "follower_count,following_count,likes_count,video_count"
                },
                timeout=10
            )
            
            if user_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"TikTok API error: {user_response.text}"
                )
            
            user_data = user_response.json().get("data", {}).get("user", {})
            
            # Fetch videos
            videos_response = requests.post(
                "https://open.tiktokapis.com/v2/video/list/",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "max_count": 20
                },
                timeout=10
            )
            
            videos_data = []
            avg_views = 0
            avg_likes = 0
            avg_comments = 0
            avg_shares = 0
            total_views = 0
            
            if videos_response.status_code == 200:
                videos_raw = videos_response.json().get("data", {}).get("videos", [])
                
                if videos_raw:
                    total_views = sum(v.get("view_count", 0) for v in videos_raw)
                    total_likes = sum(v.get("like_count", 0) for v in videos_raw)
                    total_comments = sum(v.get("comment_count", 0) for v in videos_raw)
                    total_shares = sum(v.get("share_count", 0) for v in videos_raw)
                    
                    count = len(videos_raw)
                    avg_views = total_views // count
                    avg_likes = total_likes // count
                    avg_comments = total_comments // count
                    avg_shares = total_shares // count
                    
                    # Get top 3 videos
                    sorted_videos = sorted(
                        videos_raw,
                        key=lambda x: x.get("view_count", 0),
                        reverse=True
                    )[:3]
                    
                    videos_data = [
                        {
                            "id": video.get("id"),
                            "views": video.get("view_count", 0),
                            "likes": video.get("like_count", 0),
                            "comments": video.get("comment_count", 0),
                            "shares": video.get("share_count", 0),
                            "thumbnail_url": video.get("cover_image_url", "")
                        }
                        for video in sorted_videos
                    ]
            
            # Calculate engagement rate
            engagement_rate = 0
            if avg_views > 0:
                engagement_rate = ((avg_likes + avg_comments + avg_shares) / avg_views) * 100
            
            followers = user_data.get("follower_count", 0)
            total_likes = user_data.get("likes_count", 0)
            total_videos = user_data.get("video_count", 0)
            
            # Build insights object
            tiktok_insights = {
                "followers": followers,
                "following": user_data.get("following_count", 0),
                "total_likes": total_likes,
                "total_videos": total_videos,
                "avg_views": avg_views,
                "avg_likes": avg_likes,
                "avg_comments": avg_comments,
                "avg_shares": avg_shares,
                "engagement_rate": round(engagement_rate, 2),
                "video_views": total_views,
                "profile_views": 0,  # TikTok API doesn't provide this in basic access
                "top_videos": videos_data
            }
            
            # Update profile
            profile.tiktok_insights = tiktok_insights
            profile.tiktok_followers = followers
            
            # Update average engagement if Instagram not available
            if not profile.instagram_insights:
                profile.average_engagement_rate = engagement_rate
            
            await self.db.commit()
            await self.db.refresh(profile)
            
            return tiktok_insights
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Error connecting to TikTok API: {str(e)}"
            )
