"""
Daily Briefing API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import uuid
import random

router = APIRouter()

# MARK: - Models

class PriceDropSchema(BaseModel):
    price_drop_id: str
    product: dict  # Product as dict
    previous_price: float
    new_price: float
    drop_percentage: float
    detected_at: str  # ISO format

class BriefingSchema(BaseModel):
    briefing_id: str
    user_id: str
    created_at: str  # ISO format
    new_products: List[dict]  # List of products
    price_drops: List[PriceDropSchema]
    sent_at: Optional[str] = None
    delivered: bool

class BriefingPreferencesSchema(BaseModel):
    enabled: bool
    time: str  # "08:00"
    frequency: str  # "daily", "weekly"
    min_discount_threshold: float
    product_types: List[str]

# MARK: - Endpoints

@router.get("/latest", response_model=BriefingSchema)
async def get_latest_briefing():
    """
    Get today's latest briefing for the user
    """
    # Mock briefing data with correct field names
    mock_product = {
        "product_id": str(uuid.uuid4()),
        "retailer_id": "ret_1",
        "retailer_name": "Farfetch",
        "name": "Silk Evening Gown",
        "brand": "Valentino",
        "category": "Dresses",
        "price": 2800.00,
        "original_price": 3500.00,
        "discount_percentage": 20.0,
        "size_availability": ["S", "M", "L"],
        "image_urls": ["https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&h=1200&fit=crop&q=80"],  # Array, not singular
        "product_url": "https://farfetch.com/valentino-gown",
        "description": "Elegant silk gown perfect for evening events",
        "material": "100% Silk",
        "in_stock": True,
        "rating": 4.8,
        "scraped_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")  # ISO8601 format
    }
    
    mock_price_drop = {
        "price_drop_id": str(uuid.uuid4()),
        "product": mock_product,
        "previous_price": 3500.00,
        "new_price": 2800.00,
        "drop_percentage": 20.0,
        "detected_at": datetime.utcnow().isoformat()
    }
    
    briefing = {
        "briefing_id": str(uuid.uuid4()),
        "user_id": "user_123",
        "created_at": datetime.utcnow().isoformat(),
        "new_products": [mock_product, mock_product],  # 2 new products
        "price_drops": [mock_price_drop],
        "sent_at": datetime.utcnow().isoformat(),
        "delivered": True
    }
    
    return briefing

@router.get("/history", response_model=List[BriefingSchema])
async def get_briefing_history():
    """
    Get briefing history for the user
    """
    # Mock history
    history = []
    for i in range(7):  # Last 7 days
        date = datetime.utcnow() - timedelta(days=i)
        mock_product = {
            "product_id": str(uuid.uuid4()),
            "name": f"Product Day {i+1}",
            "brand": "Chanel",
            "price": 1500.00 + (i * 100),
            "original_price": None,
            "discount_percentage": None,
            "size_availability": ["M", "L"],
            "image_url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&h=1200&fit=crop&q=80",
            "product_url": "https://example.com/product",
            "description": "Luxury item",
            "material": "Leather",
            "in_stock": True,
            "rating": 4.5,
            "retailer_name": "Net-A-Porter",
            "scraped_at": date.isoformat()
        }
        
        briefing = {
            "briefing_id": str(uuid.uuid4()),
            "user_id": "user_123",
            "created_at": date.isoformat(),
            "new_products": [mock_product] if i % 2 == 0 else [],
            "price_drops": [],
            "sent_at": date.isoformat(),
            "delivered": True
        }
        history.append(briefing)
    
    return history

@router.get("/preferences", response_model=BriefingPreferencesSchema)
async def get_briefing_preferences():
    """
    Get user's briefing preferences
    """
    preferences = {
        "enabled": True,
        "time": "08:00",
        "frequency": "daily",
        "min_discount_threshold": 10.0,
        "product_types": ["Dresses", "Shoes", "Bags"]
    }
    
    return preferences

@router.post("/preferences", response_model=BriefingPreferencesSchema)
async def update_briefing_preferences(preferences: BriefingPreferencesSchema):
    """
    Update user's briefing preferences
    """
    # In production, save to database
    return preferences

@router.post("/manual-trigger")
async def manual_trigger_briefing():
    """
    Manually trigger a briefing generation
    """
    # This would trigger the briefing generation process
    return {
        "message": "Briefing generation triggered",
        "estimated_completion": datetime.utcnow().isoformat()
    }

@router.get("/{briefing_id}", response_model=BriefingSchema)
async def get_briefing_by_id(briefing_id: str):
    """
    Get a specific briefing by ID
    """
    # Mock single briefing
    mock_product = {
        "product_id": str(uuid.uuid4()),
        "name": "Designer Handbag",
        "brand": "Hermès",
        "price": 8500.00,
        "original_price": None,
        "discount_percentage": None,
        "size_availability": ["One Size"],
        "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&h=1200&fit=crop&q=80",
        "product_url": "https://example.com/hermes-bag",
        "description": "Iconic luxury handbag",
        "material": "Leather",
        "in_stock": True,
        "rating": 5.0,
        "retailer_name": "Ounass",
        "scraped_at": datetime.utcnow().isoformat()
    }
    
    briefing = {
        "briefing_id": briefing_id,
        "user_id": "user_123",
        "created_at": datetime.utcnow().isoformat(),
        "new_products": [mock_product],
        "price_drops": [],
        "sent_at": datetime.utcnow().isoformat(),
        "delivered": True
    }
    
    return briefing

