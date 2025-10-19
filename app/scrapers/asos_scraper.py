"""
ASOS Web Scraper - Simple implementation for real product data
Uses requests + BeautifulSoup for lightweight scraping
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from typing import List, Dict, Optional
from datetime import datetime

class ASOSScraper:
    """Simple ASOS scraper using their public search API"""
    
    def __init__(self):
        self.base_url = "https://www.asos.com"
        self.api_url = "https://www.asos.com/api/product/search/v2/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        })
    
    def search_products(
        self,
        query: str,
        gender: str = "women",
        limit: int = 20,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Dict]:
        """
        Search ASOS for products
        
        Args:
            query: Search term (e.g., "dress", "jacket")
            gender: "women" or "men"
            limit: Number of products to return
            min_price: Minimum price filter
            max_price: Maximum price filter
        """
        print(f"🔍 Searching ASOS for: {query}")
        
        try:
            # Build search parameters
            params = {
                'q': query,
                'store': 'US',  # US store
                'lang': 'en-US',
                'currency': 'USD',
                'sizeSchema': 'US',
                'limit': limit,
                'offset': 0,
                'channel': 'mobile-web',
                'keyStoreDataversion': 'ornjx7v-36',
            }
            
            # Add gender filter
            if gender.lower() == "men":
                params['gender'] = 'men'
            else:
                params['gender'] = 'women'
            
            # Make request
            response = self.session.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Debug: print response structure
            # print(f"Response keys: {data.keys()}")
            
            products = data.get('products', [])
            
            print(f"✅ Found {len(products)} products from ASOS")
            
            # Debug first product structure
            if products:
                print(f"First product type: {type(products[0])}")
                if isinstance(products[0], dict):
                    print(f"First product keys: {products[0].keys()}")
            
            # Transform to our format
            transformed_products = []
            for product in products[:limit]:
                try:
                    transformed = self._transform_product(product)
                    
                    # Apply price filters
                    if min_price and transformed['price'] < min_price:
                        continue
                    if max_price and transformed['price'] > max_price:
                        continue
                    
                    transformed_products.append(transformed)
                except Exception as e:
                    import traceback
                    print(f"⚠️  Error transforming product: {e}")
                    print(f"Product data: {product}")
                    traceback.print_exc()
                    continue
            
            return transformed_products
            
        except requests.RequestException as e:
            print(f"❌ ASOS API error: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []
    
    def _transform_product(self, asos_product: Dict) -> Dict:
        """Transform ASOS product to Attireum format"""
        
        # Extract basic info
        product_id = str(asos_product.get('id', ''))
        name = asos_product.get('name', 'Unknown Product')
        brand = asos_product.get('brandName', 'ASOS')
        
        # Price info - ASOS returns price as nested dict or string
        price_data = asos_product.get('price', {})
        
        # Handle different price formats
        if isinstance(price_data, dict):
            current_data = price_data.get('current', {})
            if isinstance(current_data, dict):
                current_price = float(current_data.get('value', 0))
            else:
                current_price = float(current_data) if current_data else 0
            
            previous_data = price_data.get('previous')
            if previous_data and isinstance(previous_data, dict):
                previous_price = previous_data.get('value')
            else:
                previous_price = previous_data
        else:
            # Price is a simple number
            current_price = float(price_data) if price_data else 0
            previous_price = None
        
        # Calculate discount
        original_price = None
        discount_percentage = None
        if previous_price and float(previous_price) > current_price:
            original_price = float(previous_price)
            discount_percentage = ((original_price - current_price) / original_price) * 100
        
        # Images
        image_url = asos_product.get('imageUrl', '')
        if image_url and not image_url.startswith('http'):
            image_url = f"https://{image_url}"
        
        # Generate multiple image URLs (ASOS pattern)
        image_urls = []
        if image_url:
            # ASOS has multiple views: $01, $02, $03, $04
            base_image = image_url.replace('$n_', '$01')
            image_urls = [
                base_image.replace('$01', f'$0{i}') for i in range(1, 5)
            ]
        
        # Product URL
        product_url = f"https://www.asos.com/us/prd/{product_id}"
        
        # Category - determine from product name
        category = "Fashion"  # Default
        name_lower = name.lower()
        if 'dress' in name_lower:
            category = "Dresses"
        elif 'top' in name_lower or 'shirt' in name_lower or 'blouse' in name_lower:
            category = "Tops"
        elif 'pant' in name_lower or 'jean' in name_lower or 'trouser' in name_lower:
            category = "Pants"
        elif 'shoe' in name_lower or 'sneaker' in name_lower or 'boot' in name_lower:
            category = "Shoes"
        elif 'jacket' in name_lower or 'coat' in name_lower or 'blazer' in name_lower:
            category = "Outerwear"
        elif 'skirt' in name_lower:
            category = "Skirts"
        
        # Sizes (ASOS doesn't always provide this in search results)
        size_availability = ['XS', 'S', 'M', 'L', 'XL']  # Default sizes
        
        # Build Attireum product
        return {
            'product_id': f'asos_{product_id}',
            'retailer_id': 'asos',
            'retailer_name': 'ASOS',
            'name': name,
            'brand': brand,
            'category': category,
            'price': current_price,
            'original_price': original_price,
            'discount_percentage': discount_percentage,
            'size_availability': size_availability,
            'image_urls': image_urls if image_urls else [image_url] if image_url else [],
            'product_url': product_url,
            'description': f"{brand} {name}",
            'material': None,  # Not available in search results
            'in_stock': asos_product.get('isInStock', True),
            'rating': None,  # Not available in search results
            'scraped_at': datetime.utcnow().isoformat() + 'Z'
        }


# Convenience function for backend
def search_asos_products(
    query: str,
    gender: str = "women",
    limit: int = 20,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> List[Dict]:
    """Search ASOS and return products"""
    scraper = ASOSScraper()
    return scraper.search_products(
        query=query,
        gender=gender,
        limit=limit,
        min_price=min_price,
        max_price=max_price
    )


if __name__ == "__main__":
    # Test the scraper
    print("Testing ASOS Scraper...")
    scraper = ASOSScraper()
    
    # Test search
    products = scraper.search_products("dress", gender="women", limit=5)
    
    print(f"\n✅ Found {len(products)} products:")
    for product in products:
        print(f"  - {product['brand']}: {product['name']} - ${product['price']}")
        if product['image_urls']:
            print(f"    Images: {len(product['image_urls'])}")

