"""
Scraper Manager - Orchestrates all retailer scrapers
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List
from loguru import logger
import os

# Import all scraper implementations
from app.scraper.farfetch_scraper import FarfetchScraper
# from app.scraper.ounass_scraper import OunassScraper
# from app.scraper.bloomingdales_scraper import BloomingdalesScraper
# ... import other scrapers


class ScraperManager:
    """Manages and coordinates all luxury retailer scrapers"""
    
    def __init__(self):
        self.scrapers = {
            'Farfetch': FarfetchScraper(),
            # 'Ounass': OunassScraper(),
            # 'Bloomingdales': BloomingdalesScraper(),
            # 'Selfridges': SelfridgesScraper(),
            # 'Revolve': RevolveScraper(),
            # 'SSENSE': SSENSEScraper(),
            # Add other scrapers here
        }
        self.max_workers = int(os.getenv("SCRAPER_MAX_WORKERS", 5))
    
    def search_all_retailers(self, query_params: Dict) -> List[Dict]:
        """
        Search all active retailers in parallel
        
        Args:
            query_params: Search parameters
        
        Returns:
            Combined list of products from all retailers
        """
        all_products = []
        
        logger.info(f"Starting parallel search across {len(self.scrapers)} retailers")
        
        # Use ThreadPoolExecutor for parallel scraping
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit scraping tasks
            future_to_scraper = {
                executor.submit(scraper.search_products, query_params): retailer_name
                for retailer_name, scraper in self.scrapers.items()
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_scraper):
                retailer_name = future_to_scraper[future]
                try:
                    products = future.result(timeout=60)  # 60 second timeout per retailer
                    all_products.extend(products)
                    logger.info(f"✓ {retailer_name}: {len(products)} products")
                except Exception as e:
                    logger.error(f"✗ {retailer_name}: Failed - {e}")
        
        logger.info(f"Total products scraped: {len(all_products)}")
        return all_products
    
    def search_single_retailer(self, retailer_name: str, query_params: Dict) -> List[Dict]:
        """Search a specific retailer"""
        if retailer_name not in self.scrapers:
            logger.error(f"Retailer '{retailer_name}' not found")
            return []
        
        scraper = self.scrapers[retailer_name]
        try:
            products = scraper.search_products(query_params)
            return products
        except Exception as e:
            logger.error(f"Error scraping {retailer_name}: {e}")
            return []
    
    def get_active_retailers(self) -> List[str]:
        """Get list of active retailer names"""
        return list(self.scrapers.keys())
    
    def test_retailer(self, retailer_name: str) -> bool:
        """Test if a retailer scraper is working"""
        if retailer_name not in self.scrapers:
            return False
        
        try:
            test_query = {
                'product_type': 'Dresses',
                'size': 'M',
                'occasion': 'Evening',
                'brands': [],
                'price_range': {'min': 100, 'max': 10000}
            }
            
            products = self.search_single_retailer(retailer_name, test_query)
            return len(products) > 0
        except:
            return False


# Singleton instance
scraper_manager = ScraperManager()


# Example usage
if __name__ == "__main__":
    manager = ScraperManager()
    
    query = {
        'product_type': 'Dresses',
        'size': 'M',
        'occasion': 'Evening',
        'brands': ['Gucci'],
        'price_range': {'min': 500, 'max': 5000},
        'additional_filters': {
            'on_sale_only': False,
            'in_stock_only': True
        }
    }
    
    # Search all retailers
    products = manager.search_all_retailers(query)
    
    print(f"\nTotal products found: {len(products)}")
    
    # Group by retailer
    from collections import Counter
    retailer_counts = Counter([p['retailer_name'] for p in products])
    print("\nProducts by retailer:")
    for retailer, count in retailer_counts.items():
        print(f"  {retailer}: {count}")

