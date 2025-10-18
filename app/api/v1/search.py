"""
Search API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
import time
from loguru import logger

from app.database import get_db
from app.models import User, Search, Product
from app.schemas import SearchRequest, SearchResponse, ProductSchema
from app.scraper.scraper_manager import scraper_manager
from app.api.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=SearchResponse)
async def search_products(
    search_request: SearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search for luxury products across all retailers
    """
    try:
        logger.info(f"Search request from user {current_user.user_id}")
        
        # Validate search query
        query = search_request.query
        if not query.product_type or not query.size or not query.occasion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product type, size, and occasion are required"
            )
        
        # Start timer
        start_time = time.time()
        
        # Prepare query parameters for scrapers
        query_params = {
            'product_type': query.product_type,
            'size': query.size,
            'occasion': query.occasion,
            'brands': query.brands,
            'price_range': {
                'min': query.price_range.min,
                'max': query.price_range.max
            },
            'additional_filters': {
                'materials': query.additional_filters.materials,
                'colors': query.additional_filters.colors,
                'on_sale_only': query.additional_filters.on_sale_only,
                'in_stock_only': query.additional_filters.in_stock_only,
                'new_arrivals_only': query.additional_filters.new_arrivals_only
            }
        }
        
        # Execute parallel search across all retailers
        products = scraper_manager.search_all_retailers(query_params)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Apply additional filters if provided
        if search_request.filters:
            products = apply_filters(products, search_request.filters)
        
        # Apply sorting
        if search_request.sort_by:
            products = apply_sorting(products, search_request.sort_by)
        
        # Save search to database
        search_record = Search(
            user_id=current_user.user_id,
            product_type=query.product_type,
            size=query.size,
            occasion=query.occasion,
            brand_filter=query.brands,
            price_range={'min': query.price_range.min, 'max': query.price_range.max},
            additional_filters=query_params['additional_filters'],
            result_count=len(products),
            timestamp_24h=True
        )
        
        db.add(search_record)
        await db.commit()
        
        logger.info(f"Search completed: {len(products)} products in {execution_time:.2f}s")
        
        return SearchResponse(
            results=products,
            total_count=len(products),
            execution_time=execution_time,
            search_id=str(search_record.search_id)
        )
    
    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to execute search"
        )


@router.get("/history", response_model=List[dict])
async def get_search_history(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's search history"""
    try:
        stmt = select(Search).where(
            Search.user_id == current_user.user_id
        ).order_by(desc(Search.created_at)).limit(limit)
        
        result = await db.execute(stmt)
        searches = result.scalars().all()
        
        return [
            {
                'search_id': str(s.search_id),
                'product_type': s.product_type,
                'size': s.size,
                'occasion': s.occasion,
                'result_count': s.result_count,
                'created_at': s.created_at.isoformat()
            }
            for s in searches
        ]
    
    except Exception as e:
        logger.error(f"Error fetching search history: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch search history")


def apply_filters(products: List[dict], filters: dict) -> List[dict]:
    """Apply additional filters to products"""
    filtered = products
    
    if filters.price_min:
        filtered = [p for p in filtered if p['price'] >= filters.price_min]
    
    if filters.price_max:
        filtered = [p for p in filtered if p['price'] <= filters.price_max]
    
    if filters.retailers:
        filtered = [p for p in filtered if p['retailer_name'] in filters.retailers]
    
    if filters.brands:
        filtered = [p for p in filtered if p['brand'] in filters.brands]
    
    if filters.in_stock_only:
        filtered = [p for p in filtered if p.get('in_stock', True)]
    
    if filters.on_sale_only:
        filtered = [p for p in filtered if p.get('discount_percentage', 0) > 0]
    
    return filtered


def apply_sorting(products: List[dict], sort_by: str) -> List[dict]:
    """Sort products by specified criteria"""
    if sort_by == 'price_asc':
        return sorted(products, key=lambda p: p['price'])
    elif sort_by == 'price_desc':
        return sorted(products, key=lambda p: p['price'], reverse=True)
    elif sort_by == 'discount_desc':
        return sorted(products, key=lambda p: p.get('discount_percentage', 0), reverse=True)
    elif sort_by == 'date_desc':
        return sorted(products, key=lambda p: p.get('scraped_at', 0), reverse=True)
    else:
        return products

