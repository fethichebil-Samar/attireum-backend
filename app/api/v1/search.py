"""
Search API Endpoints (Simplified)
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import time

router = APIRouter()


class PriceRange(BaseModel):
    min: float
    max: float


class AdditionalFilters(BaseModel):
    materials: List[str] = []
    colors: List[str] = []
    on_sale_only: bool = False
    in_stock_only: bool = False
    new_arrivals_only: bool = False


class SearchQuery(BaseModel):
    product_type: str
    size: str
    occasion: str
    brands: List[str] = []
    price_range: PriceRange
    additional_filters: AdditionalFilters


class SearchRequest(BaseModel):
    query: SearchQuery
    filters: Optional[dict] = None
    sort_by: Optional[str] = None


class SearchResponse(BaseModel):
    results: List[dict]
    total_count: int
    execution_time: float
    search_id: str


@router.post("", response_model=SearchResponse)
async def search_products(search_request: SearchRequest):
    """
    Search for luxury products across all retailers (Mock implementation)
    """
    query = search_request.query
    
    # Generate mock products based on search
    mock_products = [
        {
            "product_id": "prod_1",
            "retailer_id": "ret_1",
            "retailer_name": "Farfetch",
            "name": f"{query.product_type} - Elegant Gucci Design",
            "brand": "Gucci",
            "category": query.product_type,
            "price": 1200.00,
            "original_price": 1500.00,
            "discount_percentage": 20.0,
            "size_availability": [query.size, "S", "M", "L"],
            "image_urls": [
                "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800&h=1200&fit=crop&q=80",
                "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&h=1200&fit=crop&q=80"
            ],
            "product_url": "https://www.farfetch.com/product/123",
            "description": f"Luxury {query.product_type.lower()} perfect for {query.occasion.lower()} occasions.",
            "material": "100% Silk",
            "in_stock": True,
            "rating": 4.8,
            "scraped_at": "2025-10-18T19:00:00Z"
        },
        {
            "product_id": "prod_2",
            "retailer_id": "ret_2",
            "retailer_name": "Net-A-Porter",
            "name": f"{query.product_type} - Stunning Prada Collection",
            "brand": "Prada",
            "category": query.product_type,
            "price": 980.00,
            "original_price": None,
            "discount_percentage": None,
            "size_availability": [query.size, "XS", "S", "M"],
            "image_urls": [
                "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&h=1200&fit=crop&q=80",
                "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&h=1200&fit=crop&q=80"
            ],
            "product_url": "https://www.net-a-porter.com/product/456",
            "description": f"Exquisite {query.product_type.lower()} crafted with attention to detail.",
            "material": "Premium Leather",
            "in_stock": True,
            "rating": 4.9,
            "scraped_at": "2025-10-18T19:00:00Z"
        },
        {
            "product_id": "prod_3",
            "retailer_id": "ret_3",
            "retailer_name": "Ounass",
            "name": f"{query.product_type} - Luxe Chanel Design",
            "brand": "Chanel",
            "category": query.product_type,
            "price": 2400.00,
            "original_price": 3000.00,
            "discount_percentage": 25.0,
            "size_availability": [query.size, "M", "L", "XL"],
            "image_urls": [
                "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800&h=1200&fit=crop&q=80",
                "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&h=1200&fit=crop&q=80"
            ],
            "product_url": "https://www.ounass.com/product/789",
            "description": f"Timeless {query.product_type.lower()} from Chanel's latest collection.",
            "material": "Silk & Cashmere Blend",
            "in_stock": True,
            "rating": 5.0,
            "scraped_at": "2025-10-18T19:00:00Z"
        }
    ]
    
    return SearchResponse(
        results=mock_products,
        total_count=len(mock_products),
        execution_time=2.3,
        search_id="search_" + str(int(time.time()))
    )


@router.get("/history")
async def get_search_history():
    """Get user's search history (Mock implementation)"""
    return []
