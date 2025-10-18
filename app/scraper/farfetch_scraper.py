"""
Farfetch Scraper Implementation
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List, Optional
from app.scraper.base_scraper import BaseScraper
from loguru import logger


class FarfetchScraper(BaseScraper):
    """Scraper for Farfetch luxury fashion retailer"""
    
    def __init__(self):
        super().__init__(
            retailer_name="Farfetch",
            base_url="https://www.farfetch.com"
        )
    
    def _build_search_url(self, query_params: Dict) -> str:
        """Build Farfetch search URL"""
        product_type = query_params.get('product_type', '').lower().replace(' ', '-')
        
        # Map product types to Farfetch categories
        category_mapping = {
            'dresses': 'clothing-2/dresses-1',
            'shirts-&-blouses': 'clothing-2/tops-2',
            'pants': 'clothing-2/pants-2',
            'jackets-&-coats': 'clothing-2/coats-jackets-1',
            'sweaters-&-knitwear': 'clothing-2/knitwear-1',
            'bags': 'accessories-1/bags-2',
            'shoes': 'shoes-2',
            'jewelry': 'accessories-1/jewelry-1'
        }
        
        category = category_mapping.get(product_type, 'clothing-2')
        
        # Build URL with filters
        base_search = f"{self.base_url}/shopping/women/{category}/items.aspx"
        
        # Add price range
        price_range = query_params.get('price_range', {})
        price_min = price_range.get('min', 100)
        price_max = price_range.get('max', 10000)
        
        filters = []
        filters.append(f"price={int(price_min)}-{int(price_max)}")
        
        # Add brand filter
        brands = query_params.get('brands', [])
        if brands:
            brand_filter = '|'.join([b.lower().replace(' ', '-') for b in brands])
            filters.append(f"designers={brand_filter}")
        
        # Add size filter
        size = query_params.get('size', '')
        if size:
            filters.append(f"size={size}")
        
        # Combine filters
        if filters:
            base_search += '?' + '&'.join(filters)
        
        return base_search
    
    def _extract_product_cards(self) -> List:
        """Extract product cards from Farfetch page"""
        try:
            # Wait for product grid to load
            wait = WebDriverWait(self.driver, self.wait_time)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component='ProductCard']")))
            
            # Find all product cards
            cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-component='ProductCard']")
            return cards
        
        except Exception as e:
            logger.error(f"Error extracting product cards: {e}")
            return []
    
    def _parse_product_card(self, card_element) -> Optional[Dict]:
        """Parse Farfetch product card"""
        try:
            product_data = {}
            
            # Extract brand
            try:
                brand_element = card_element.find_element(By.CSS_SELECTOR, "[data-component='ProductCardBrand']")
                product_data['brand'] = brand_element.text.strip()
            except:
                product_data['brand'] = "Unknown"
            
            # Extract product name
            try:
                name_element = card_element.find_element(By.CSS_SELECTOR, "[data-component='ProductCardDescription']")
                product_data['name'] = name_element.text.strip()
            except:
                product_data['name'] = "Unknown Product"
            
            # Extract price
            try:
                price_element = card_element.find_element(By.CSS_SELECTOR, "[data-component='ProductCardPrice']")
                price_text = price_element.text.strip()
                product_data['price'] = self._extract_price(price_text)
            except:
                product_data['price'] = 0.0
            
            # Extract original price (if on sale)
            try:
                original_price_element = card_element.find_element(By.CSS_SELECTOR, "[data-component='PriceWithoutDiscount']")
                original_price_text = original_price_element.text.strip()
                product_data['original_price'] = self._extract_price(original_price_text)
                
                # Calculate discount percentage
                if product_data['original_price'] > 0:
                    discount = ((product_data['original_price'] - product_data['price']) / 
                               product_data['original_price']) * 100
                    product_data['discount_percentage'] = round(discount, 2)
            except:
                product_data['original_price'] = None
                product_data['discount_percentage'] = None
            
            # Extract image URL
            try:
                img_element = card_element.find_element(By.CSS_SELECTOR, "img")
                product_data['image_urls'] = [img_element.get_attribute('src')]
            except:
                product_data['image_urls'] = []
            
            # Extract product URL
            try:
                link_element = card_element.find_element(By.CSS_SELECTOR, "a")
                product_url = link_element.get_attribute('href')
                if not product_url.startswith('http'):
                    product_url = self.base_url + product_url
                product_data['product_url'] = product_url
            except:
                product_data['product_url'] = ""
            
            # Set defaults
            product_data['category'] = "Clothing"
            product_data['size_availability'] = []
            product_data['description'] = ""
            product_data['material'] = ""
            product_data['in_stock'] = True
            product_data['rating'] = None
            
            # Validate essential fields
            if not product_data['product_url'] or product_data['price'] == 0:
                return None
            
            return product_data
        
        except Exception as e:
            logger.error(f"Error parsing product card: {e}")
            return None


# Example usage and testing
if __name__ == "__main__":
    scraper = FarfetchScraper()
    
    test_query = {
        'product_type': 'Dresses',
        'size': 'M',
        'occasion': 'Evening',
        'brands': ['Gucci', 'Prada'],
        'price_range': {'min': 500, 'max': 5000}
    }
    
    products = scraper.search_products(test_query)
    print(f"Found {len(products)} products")
    
    for product in products[:3]:
        print(f"\n{product['brand']} - {product['name']}")
        print(f"Price: ${product['price']}")
        print(f"URL: {product['product_url']}")

