"""
Analytics Service for Tracking User Behavior and System Metrics
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import select, func, and_
from loguru import logger

from app.database import AsyncSessionLocal
from app.models import Analytics, User, Search, Briefing, Wishlist, Product


class AnalyticsService:
    """Service for tracking and analyzing user behavior and system metrics"""
    
    async def track_event(
        self,
        event_type: str,
        user_id: Optional[str] = None,
        event_data: Optional[Dict] = None
    ) -> bool:
        """
        Track an analytics event
        
        Args:
            event_type: Type of event (search, wishlist_add, briefing_open, etc.)
            user_id: Optional user ID
            event_data: Additional event data
        
        Returns:
            Success status
        """
        async with AsyncSessionLocal() as session:
            try:
                event = Analytics(
                    user_id=user_id,
                    event_type=event_type,
                    event_data=event_data or {}
                )
                session.add(event)
                await session.commit()
                return True
            except Exception as e:
                logger.error(f"Error tracking event: {e}")
                await session.rollback()
                return False
    
    async def get_user_search_patterns(self, user_id: str, days: int = 30) -> Dict:
        """Analyze user's search patterns over time"""
        async with AsyncSessionLocal() as session:
            try:
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                # Get searches
                stmt = select(Search).where(
                    Search.user_id == user_id,
                    Search.created_at >= cutoff_date
                )
                result = await session.execute(stmt)
                searches = result.scalars().all()
                
                # Analyze patterns
                product_types = {}
                occasions = {}
                brands = {}
                
                for search in searches:
                    # Count product types
                    product_types[search.product_type] = product_types.get(search.product_type, 0) + 1
                    
                    # Count occasions
                    occasions[search.occasion] = occasions.get(search.occasion, 0) + 1
                    
                    # Count brands
                    for brand in search.brand_filter:
                        brands[brand] = brands.get(brand, 0) + 1
                
                return {
                    'total_searches': len(searches),
                    'top_product_types': sorted(product_types.items(), key=lambda x: x[1], reverse=True)[:5],
                    'top_occasions': sorted(occasions.items(), key=lambda x: x[1], reverse=True)[:5],
                    'favorite_brands': sorted(brands.items(), key=lambda x: x[1], reverse=True)[:10],
                    'avg_searches_per_day': len(searches) / days if days > 0 else 0
                }
            
            except Exception as e:
                logger.error(f"Error analyzing search patterns: {e}")
                return {}
    
    async def get_scraper_health(self) -> Dict:
        """Monitor scraper health and success rates"""
        async with AsyncSessionLocal() as session:
            try:
                # Get products scraped in last 24 hours
                cutoff = datetime.utcnow() - timedelta(hours=24)
                
                stmt = select(
                    Product.retailer_id,
                    func.count(Product.product_id).label('count')
                ).where(
                    Product.scraped_at >= cutoff
                ).group_by(Product.retailer_id)
                
                result = await session.execute(stmt)
                retailer_counts = dict(result.all())
                
                return {
                    'last_24h_products': sum(retailer_counts.values()),
                    'by_retailer': retailer_counts,
                    'avg_products_per_retailer': sum(retailer_counts.values()) / len(retailer_counts) if retailer_counts else 0
                }
            
            except Exception as e:
                logger.error(f"Error getting scraper health: {e}")
                return {}
    
    async def get_briefing_engagement(self, days: int = 30) -> Dict:
        """Analyze briefing engagement metrics"""
        async with AsyncSessionLocal() as session:
            try:
                cutoff = datetime.utcnow() - timedelta(days=days)
                
                stmt = select(Briefing).where(Briefing.created_at >= cutoff)
                result = await session.execute(stmt)
                briefings = result.scalars().all()
                
                total_sent = len(briefings)
                delivered = sum(1 for b in briefings if b.delivered)
                
                # Calculate average new products per briefing
                avg_new_products = sum(len(b.new_products) for b in briefings) / total_sent if total_sent > 0 else 0
                avg_price_drops = sum(len(b.price_drops) for b in briefings) / total_sent if total_sent > 0 else 0
                
                return {
                    'total_briefings_sent': total_sent,
                    'delivery_rate': (delivered / total_sent * 100) if total_sent > 0 else 0,
                    'avg_new_products': avg_new_products,
                    'avg_price_drops': avg_price_drops
                }
            
            except Exception as e:
                logger.error(f"Error getting briefing engagement: {e}")
                return {}
    
    async def get_user_retention(self) -> Dict:
        """Calculate user retention metrics"""
        async with AsyncSessionLocal() as session:
            try:
                now = datetime.utcnow()
                
                # Total users
                stmt = select(func.count(User.user_id))
                result = await session.execute(stmt)
                total_users = result.scalar()
                
                # Active users (searched in last 7 days)
                week_ago = now - timedelta(days=7)
                stmt = select(func.count(func.distinct(Search.user_id))).where(
                    Search.created_at >= week_ago
                )
                result = await session.execute(stmt)
                active_users_7d = result.scalar()
                
                # Active users (searched in last 30 days)
                month_ago = now - timedelta(days=30)
                stmt = select(func.count(func.distinct(Search.user_id))).where(
                    Search.created_at >= month_ago
                )
                result = await session.execute(stmt)
                active_users_30d = result.scalar()
                
                return {
                    'total_users': total_users,
                    'active_users_7d': active_users_7d,
                    'active_users_30d': active_users_30d,
                    'retention_7d': (active_users_7d / total_users * 100) if total_users > 0 else 0,
                    'retention_30d': (active_users_30d / total_users * 100) if total_users > 0 else 0
                }
            
            except Exception as e:
                logger.error(f"Error calculating retention: {e}")
                return {}
    
    async def get_platform_metrics(self) -> Dict:
        """Get overall platform metrics"""
        async with AsyncSessionLocal() as session:
            try:
                # User metrics
                user_stmt = select(func.count(User.user_id))
                user_result = await session.execute(user_stmt)
                total_users = user_result.scalar()
                
                # Search metrics
                search_stmt = select(func.count(Search.search_id))
                search_result = await session.execute(search_stmt)
                total_searches = search_result.scalar()
                
                # Product metrics
                product_stmt = select(func.count(Product.product_id))
                product_result = await session.execute(product_stmt)
                total_products = product_result.scalar()
                
                # Wishlist metrics
                wishlist_stmt = select(func.count(Wishlist.wishlist_id))
                wishlist_result = await session.execute(wishlist_stmt)
                total_wishlist_items = wishlist_result.scalar()
                
                return {
                    'total_users': total_users,
                    'total_searches': total_searches,
                    'total_products': total_products,
                    'total_wishlist_items': total_wishlist_items,
                    'avg_searches_per_user': total_searches / total_users if total_users > 0 else 0,
                    'avg_wishlist_per_user': total_wishlist_items / total_users if total_users > 0 else 0
                }
            
            except Exception as e:
                logger.error(f"Error getting platform metrics: {e}")
                return {}


# Singleton instance
analytics_service = AnalyticsService()


# Convenience functions
async def track_search(user_id: str, query_params: Dict):
    """Track a search event"""
    await analytics_service.track_event('search', user_id, query_params)


async def track_wishlist_add(user_id: str, product_id: str):
    """Track wishlist add event"""
    await analytics_service.track_event('wishlist_add', user_id, {'product_id': product_id})


async def track_briefing_open(user_id: str, briefing_id: str):
    """Track briefing open event"""
    await analytics_service.track_event('briefing_open', user_id, {'briefing_id': briefing_id})


async def track_product_click(user_id: str, product_id: str, retailer: str):
    """Track product click event"""
    await analytics_service.track_event(
        'product_click',
        user_id,
        {'product_id': product_id, 'retailer': retailer}
    )

