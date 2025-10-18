"""
Briefing API Endpoints
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/latest")
async def get_latest_briefing():
    """Get latest daily briefing"""
    return {
        "success": True,
        "briefing": {
            "id": "briefing_123",
            "newProducts": [],
            "priceDrops": [],
            "createdAt": "2024-01-01T08:00:00Z"
        }
    }

