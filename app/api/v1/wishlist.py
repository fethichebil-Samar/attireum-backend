"""
Wishlist API Endpoints
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_wishlist():
    """Get user's wishlist"""
    return {
        "success": True,
        "items": []
    }


@router.post("/")
async def add_to_wishlist(product_id: str):
    """Add product to wishlist"""
    return {
        "success": True,
        "message": "Added to wishlist"
    }

