"""
Wishlist API Endpoints
"""

from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List, Optional
import time

router = APIRouter()

# In-memory wishlist storage (replace with database in production)
# Clear any corrupt data
wishlist_storage = []


class WishlistItem(BaseModel):
    id: str
    user_id: str
    product: dict
    added_at: str
    price_alert_threshold: Optional[float] = None
    notified: bool = False


@router.get("/")
async def get_wishlist():
    """Get user's wishlist with mock products"""
    # Return mock wishlist items with correct field names
    mock_wishlist = [
        {
            "wishlist_id": "wish_1",
            "user_id": "test_user",
            "product": {
                "product_id": "prod_wish_1",
                "retailer_id": "ret_1",
                "retailer_name": "Farfetch",
                "name": "Elegant Valentino Evening Gown",
                "brand": "Valentino",
                "category": "Dresses",
                "price": 2800.00,
                "original_price": 3500.00,
                "discount_percentage": 20.0,
                "size_availability": ["S", "M", "L"],
                "image_urls": ["https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&h=1200&fit=crop&q=80"],
                "product_url": "https://www.farfetch.com/product/123",
                "description": "Elegant silk evening gown perfect for formal occasions.",
                "material": "100% Silk",
                "in_stock": True,
                "rating": 4.8,
                "scraped_at": "2025-10-19T13:00:00Z"
            },
            "added_at": "2025-10-18T10:30:00Z",
            "price_alert_threshold": 2500.00,
            "notified": False
        },
        {
            "wishlist_id": "wish_2",
            "user_id": "test_user",
            "product": {
                "product_id": "prod_wish_2",
                "retailer_id": "ret_2",
                "retailer_name": "Net-A-Porter",
                "name": "Gucci GG Marmont Shoulder Bag",
                "brand": "Gucci",
                "category": "Bags",
                "price": 1890.00,
                "original_price": None,
                "discount_percentage": None,
                "size_availability": ["One Size"],
                "image_urls": ["https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&h=1200&fit=crop&q=80"],
                "product_url": "https://www.net-a-porter.com/product/456",
                "description": "Iconic GG Marmont shoulder bag in quilted leather.",
                "material": "Quilted Leather",
                "in_stock": True,
                "rating": 4.9,
                "scraped_at": "2025-10-19T13:00:00Z"
            },
            "added_at": "2025-10-17T15:20:00Z",
            "price_alert_threshold": 1700.00,
            "notified": False
        },
        {
            "wishlist_id": "wish_3",
            "user_id": "test_user",
            "product": {
                "product_id": "prod_wish_3",
                "retailer_id": "ret_3",
                "retailer_name": "Ounass",
                "name": "Christian Louboutin So Kate Pumps",
                "brand": "Christian Louboutin",
                "category": "Shoes",
                "price": 695.00,
                "original_price": 795.00,
                "discount_percentage": 12.6,
                "size_availability": ["36", "37", "38", "39", "40"],
                "image_urls": ["https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800&h=1200&fit=crop&q=80"],
                "product_url": "https://www.ounass.com/product/789",
                "description": "Iconic So Kate 120mm patent leather pumps.",
                "material": "Patent Leather",
                "in_stock": True,
                "rating": 4.7,
                "scraped_at": "2025-10-19T13:00:00Z"
            },
            "added_at": "2025-10-16T09:45:00Z",
            "price_alert_threshold": 600.00,
            "notified": False
        }
    ]
    
    # Combine with in-memory storage
    all_items = wishlist_storage + mock_wishlist
    
    # Return in the format iOS app expects
    return {
        "items": all_items,
        "total_count": len(all_items)
    }


class AddToWishlistRequest(BaseModel):
    product_id: str
    price_alert_threshold: Optional[float] = None


@router.post("/")
async def add_to_wishlist(request: AddToWishlistRequest):
    """Add product to wishlist"""
    
    # For now, create a mock product based on the product_id
    # In production, you'd fetch the actual product from database
    mock_product = {
        "product_id": request.product_id,
        "retailer_id": "ret_1",
        "retailer_name": "Farfetch",
        "name": "Luxury Fashion Item",
        "brand": "Designer",
        "category": "Fashion",
        "price": 1500.0,
        "original_price": None,
        "discount_percentage": None,
        "size_availability": ["M", "L"],
        "image_urls": ["https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800&h=1200&fit=crop&q=80"],
        "product_url": "https://www.farfetch.com/product/" + request.product_id,
        "description": "Luxury fashion item",
        "material": "Premium",
        "in_stock": True,
        "rating": 4.5,
        "scraped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    # Create wishlist item with proper field names
    wishlist_item = {
        "wishlist_id": f"wish_{int(time.time())}",
        "user_id": "test_user",
        "product": mock_product,
        "added_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "price_alert_threshold": request.price_alert_threshold or (mock_product["price"] * 0.9),
        "notified": False
    }
    
    # Add to storage
    wishlist_storage.append(wishlist_item)
    
    print(f"✅ Added to wishlist: {request.product_id}")
    
    # Return the item directly (iOS expects WishlistItem, not a wrapper)
    return wishlist_item


@router.delete("/{item_id}")
async def remove_from_wishlist(item_id: str):
    """Remove product from wishlist"""
    global wishlist_storage
    wishlist_storage = [item for item in wishlist_storage if item["id"] != item_id]
    
    return {
        "success": True,
        "message": "Removed from wishlist"
    }

