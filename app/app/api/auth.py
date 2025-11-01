"""
Authentication router for user registration and login.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.schemas.user_schemas import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    
    - **EMPRESA**: Automatically approved, trial starts immediately
    - **INFLUENCER**: Requires admin approval
    - **ADMIN**: Automatically approved
    """
    auth_service = AuthService(db)
    user = await auth_service.register_user(user_data)
    return user


@router.options("/login")
async def login_options():
    """Handle CORS preflight for login endpoint."""
    return {"message": "OK"}


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.
    
    Sets httpOnly cookie with JWT token and returns token in response.
    """
    auth_service = AuthService(db)
    
    user = await auth_service.authenticate_user(login_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_token(user)
    
    # Set httpOnly cookie for frontend
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Cannot be accessed by JavaScript (XSS protection)
        secure=False,   # Set to True in production (HTTPS only)
        samesite="lax", # CSRF protection
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # seconds
    )
    
    return Token(access_token=access_token)


@router.post("/logout")
async def logout(response: Response):
    """
    Logout user by clearing the httpOnly cookie.
    """
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}
