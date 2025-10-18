"""
Profile API Endpoints
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_profile():
    """Get user profile"""
    return {
        "success": True,
        "profile": {
            "id": "user_123",
            "email": "user@example.com",
            "firstName": "Luxury",
            "lastName": "Shopper"
        }
    }


@router.put("/")
async def update_profile():
    """Update user profile"""
    return {
        "success": True,
        "message": "Profile updated"
    }

