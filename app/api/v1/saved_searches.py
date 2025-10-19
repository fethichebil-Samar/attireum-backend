"""
Saved Searches & Daily Briefing API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter()

# MARK: - Models

class SavedSearchSchema(BaseModel):
    saved_search_id: str
    user_id: str
    name: str
    query: dict  # SearchQuery as dict
    enable_daily_briefing: bool
    last_checked: Optional[str] = None  # ISO format
    result_count: int
    created_at: str  # ISO format
    updated_at: str  # ISO format

class CreateSavedSearchRequest(BaseModel):
    name: str
    query: dict
    enable_daily_briefing: bool

class UpdateSavedSearchRequest(BaseModel):
    name: Optional[str] = None
    enable_daily_briefing: Optional[bool] = None

# MARK: - In-memory storage (replace with database)
saved_searches_db = {}

# MARK: - Endpoints

@router.get("/", response_model=List[SavedSearchSchema])
async def get_saved_searches():
    """
    Get all saved searches for the current user
    """
    # Return saved searches from in-memory storage, plus mock data
    all_searches = list(saved_searches_db.values())
    
    # Add mock data if storage is empty
    if len(all_searches) == 0:
        mock_searches = [
            {
                "saved_search_id": "search_1",
                "user_id": "user_123",
                "name": "Evening Dresses",
                "query": {
                    "product_type": "Dresses",
                    "size": "M",
                    "occasion": "Evening",
                    "brands": ["Valentino"],  # Array, not singular
                    "price_range": {  # Object, not separate min/max
                        "min": 1000.0,
                        "max": 5000.0
                    }
                },
                "enable_daily_briefing": True,
                "last_checked": datetime.utcnow().isoformat() + "Z",
                "result_count": 42,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z"
            },
            {
                "saved_search_id": "search_2",
                "user_id": "user_123",
                "name": "Casual Chic",
                "query": {
                    "product_type": "Tops",
                    "size": "S",
                    "occasion": "Day-to-Day / Casual",
                    "brands": [],  # Empty array
                    "price_range": {
                        "min": 200.0,
                        "max": 1000.0
                    }
                },
                "enable_daily_briefing": False,
                "last_checked": None,
                "result_count": 87,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z"
            }
        ]
        all_searches = mock_searches
    
    print(f"📚 Returning {len(all_searches)} saved searches")
    return all_searches

@router.post("/", response_model=SavedSearchSchema)
async def create_saved_search(request: CreateSavedSearchRequest):
    """
    Create a new saved search
    """
    search_id = str(uuid.uuid4())
    
    saved_search = {
        "saved_search_id": search_id,
        "user_id": "user_123",
        "name": request.name,
        "query": request.query,
        "enable_daily_briefing": request.enable_daily_briefing,
        "last_checked": None,
        "result_count": 0,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    saved_searches_db[search_id] = saved_search
    
    print(f"✅ Saved search created: {request.name} (briefing: {request.enable_daily_briefing})")
    print(f"   ID: {search_id}")
    print(f"   Total searches: {len(saved_searches_db)}")
    
    return saved_search

@router.put("/{search_id}", response_model=SavedSearchSchema)
async def update_saved_search(search_id: str, request: UpdateSavedSearchRequest):
    """
    Update a saved search
    """
    # Mock response - in production, fetch from database
    saved_search = {
        "saved_search_id": search_id,
        "user_id": "user_123",
        "name": request.name or "Updated Search",
        "query": {
            "product_type": "Dresses",
            "size": "M",
            "occasion": "Evening",
            "brand": None,
            "price_min": None,
            "price_max": None
        },
        "enable_daily_briefing": request.enable_daily_briefing if request.enable_daily_briefing is not None else True,
        "last_checked": datetime.utcnow().isoformat(),
        "result_count": 42,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    return saved_search

@router.delete("/{search_id}")
async def delete_saved_search(search_id: str):
    """
    Delete a saved search
    """
    if search_id in saved_searches_db:
        del saved_searches_db[search_id]
    
    return {"message": "Search deleted successfully"}

@router.post("/{search_id}/run")
async def run_saved_search(search_id: str):
    """
    Manually trigger a saved search
    """
    # This would execute the search and return results
    return {"message": "Search executed successfully", "result_count": 42}

