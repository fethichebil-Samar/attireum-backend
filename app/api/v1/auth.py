"""
Authentication API Endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import os

router = APIRouter()

# JWT Settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


class SignUpRequest(BaseModel):
    email: str
    password: str
    firstName: str
    lastName: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    accessToken: str
    refreshToken: str
    user: dict


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # Simple token generation without JWT for now
    import secrets
    return f"token_{secrets.token_urlsafe(32)}"


@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignUpRequest):
    """Sign up a new user"""
    # For now, create a mock user (you'll replace this with real database logic)
    user_data = {
        "id": f"user_{datetime.utcnow().timestamp()}",
        "email": request.email,
        "firstName": request.firstName,
        "lastName": request.lastName,
        "sizes": {},
        "preferredBrands": [],
        "preferredOccasions": [],
        "currency": "USD",
        "region": "US",
        "timezone": "America/New_York",
        "notificationPreferences": {
            "dailyBriefing": True,
            "priceAlerts": True,
            "newArrivals": True
        },
        "createdAt": datetime.utcnow().isoformat(),
        "updatedAt": datetime.utcnow().isoformat()
    }
    
    # Create tokens
    access_token = create_access_token(data={"sub": user_data["email"], "user_id": user_data["id"]})
    refresh_token = create_access_token(
        data={"sub": user_data["email"], "user_id": user_data["id"]},
        expires_delta=timedelta(days=30)
    )
    
    return AuthResponse(
        accessToken=access_token,
        refreshToken=refresh_token,
        user=user_data
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login an existing user"""
    # For now, accept any login (you'll replace this with real authentication)
    user_data = {
        "id": "user_123",
        "email": request.email,
        "firstName": "Luxury",
        "lastName": "Shopper",
        "sizes": {},
        "preferredBrands": ["Gucci", "Prada", "Chanel"],
        "preferredOccasions": ["Evening", "Formal"],
        "currency": "USD",
        "region": "US",
        "timezone": "America/New_York",
        "notificationPreferences": {
            "dailyBriefing": True,
            "priceAlerts": True,
            "newArrivals": True
        },
        "createdAt": datetime.utcnow().isoformat(),
        "updatedAt": datetime.utcnow().isoformat()
    }
    
    # Create tokens
    access_token = create_access_token(data={"sub": user_data["email"], "user_id": user_data["id"]})
    refresh_token = create_access_token(
        data={"sub": user_data["email"], "user_id": user_data["id"]},
        expires_delta=timedelta(days=30)
    )
    
    return AuthResponse(
        accessToken=access_token,
        refreshToken=refresh_token,
        user=user_data
    )


@router.post("/logout")
async def logout():
    """Logout user"""
    return {"success": True, "message": "Logged out successfully"}


@router.post("/refresh-token")
async def refresh_token():
    """Refresh access token"""
    # Implement token refresh logic
    return {"accessToken": "new_token", "refreshToken": "new_refresh_token"}

