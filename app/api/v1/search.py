"""
Search API Endpoints (Simplified)
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import time

router = APIRouter()


class SearchQuery(BaseModel):
    productType: str
    size: str
    occasion: str
    brands: Optional[List[str]] = None


class SearchRequest(BaseModel):
    query: SearchQuery


class SearchResponse(BaseModel):
    results: List[dict]
    totalCount: int
    executionTime: float
    searchId: str


@router.post("", response_model=SearchResponse)
async def search_products(search_request: SearchRequest):
    """
    Search for luxury products across all retailers (Mock implementation)
    """
    # Mock search results
    mock_products = [
        {
            "id": "1",
            "name": f"{search_request.query.productType} - Luxury Item 1",
            "brand": "Gucci",
            "price": 1200.00,
            "retailerName": "Farfetch",
            "imageUrls": ["https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800&h=1200"],
            "inStock": True
        },
        {
            "id": "2",
            "name": f"{search_request.query.productType} - Luxury Item 2",
            "brand": "Prada",
            "price": 980.00,
            "retailerName": "Net-A-Porter",
            "imageUrls": ["https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&h=1200"],
            "inStock": True
        }
    ]
    
    return SearchResponse(
        results=mock_products,
        totalCount=len(mock_products),
        executionTime=2.3,
        searchId="search_123"
    )


@router.get("/history")
async def get_search_history():
    """Get user's search history (Mock implementation)"""
    return []
