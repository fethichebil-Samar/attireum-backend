"""
Authentication API Endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import os
import secrets

router = APIRouter()

# JWT Settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


class SignUpRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: dict


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # Simple token generation without JWT for now
    return f"token_{secrets.token_urlsafe(32)}"


@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignUpRequest):
    """Sign up a new user"""
    user_data = {
        "user_id": f"user_{int(datetime.utcnow().timestamp())}",
        "email": request.email,
        "first_name": request.first_name,
        "last_name": request.last_name,
        "sizes": {
            "international": [],
            "us": [],
            "eu": []
        },
        "preferred_brands": [],
        "preferred_occasions": [],
        "currency": "USD",
        "region": "US",
        "timezone": "America/New_York",
        "notification_preferences": {
            "briefing_enabled": True,
            "briefing_time": "08:00",
            "briefing_frequency": "daily",
            "price_alerts": True,
            "new_arrivals": True,
            "sales_alerts": True,
            "quiet_hours_start": None,
            "quiet_hours_end": None
        },
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    # Create tokens
    access_token = create_access_token(data={"sub": user_data["email"], "user_id": user_data["user_id"]})
    refresh_token = create_access_token(data={"sub": user_data["email"], "user_id": user_data["user_id"]}, expires_delta=timedelta(days=30))
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_data
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login an existing user"""
    user_data = {
        "user_id": "user_123",
        "email": request.email,
        "first_name": "Luxury",
        "last_name": "Shopper",
        "sizes": {
            "international": [],
            "us": [],
            "eu": []
        },
        "preferred_brands": ["Gucci", "Prada", "Chanel"],
        "preferred_occasions": ["Evening", "Formal"],
        "currency": "USD",
        "region": "US",
        "timezone": "America/New_York",
        "notification_preferences": {
            "briefing_enabled": True,
            "briefing_time": "08:00",
            "briefing_frequency": "daily",
            "price_alerts": True,
            "new_arrivals": True,
            "sales_alerts": True,
            "quiet_hours_start": None,
            "quiet_hours_end": None
        },
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    # Create tokens
    access_token = create_access_token(data={"sub": user_data["email"], "user_id": user_data["user_id"]})
    refresh_token = create_access_token(data={"sub": user_data["email"], "user_id": user_data["user_id"]}, expires_delta=timedelta(days=30))
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_data
    )


@router.post("/logout")
async def logout():
    """Logout user"""
    return {"success": True, "message": "Logged out successfully"}


@router.post("/refresh-token")
async def refresh_token():
    """Refresh access token"""
    return {"access_token": "new_token", "refresh_token": "new_refresh_token"}
