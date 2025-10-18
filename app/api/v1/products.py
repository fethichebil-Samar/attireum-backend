"""
Products API Endpoints
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/{product_id}")
async def get_product(product_id: str):
    """Get product details by ID"""
    return {
        "success": True,
        "product": {
            "id": product_id,
            "name": "Luxury Product",
            "brand": "Gucci",
            "price": 1200.00
        }
    }

