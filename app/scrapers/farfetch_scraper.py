"""
Farfetch Web Scraper - Real Products
"""

import httpx
import json
from typing import List, Dict, Optional
import asyncio
from urllib.parse import quote


class FarfetchScraper:
    """
    Scraper for Farfetch luxury retailer
    Uses their public API endpoints
    """
    
    BASE_URL = "https://www.farfetch.com"
    API_BASE = "https://www.farfetch.com/plpslice/api/products"
    
    def __init__(self):
        self.session = None
        
    async def search_products(
        self,
        query: str,
        category: Optional[str] = None,
        gender: str = "women",
        size: Optional[str] = None,
        max_price: Optional[float] = None,
        min_price: Optional[float] = None,
        page: int = 1,
        page_size: int = 12
    ) -> List[Dict]:
        """
        Search for products on Farfetch
        
        Args:
            query: Search term (e.g., "evening dress")
            category: Product category
            gender: "women" or "men"
            size: Size filter
            max_price: Maximum price
            min_price: Minimum price
            page: Page number
            page_size: Number of results per page
            
        Returns:
            List of product dictionaries
        """
        
        # Map categories to Farfetch categories
        category_map = {
            "Dresses": "clothing-dresses",
            "Jackets & Coats": "clothing-coats-jackets",
            "Pants": "clothing-pants",
            "Shirts & Blouses": "clothing-tops",
            "Bags": "bags-purses",
            "Shoes": "shoes",
            "Skirts": "clothing-skirts",
            "Sweaters & Knitwear": "clothing-knitwear",
        }
        
        # Build search URL
        category_slug = category_map.get(category, "")
        
        # Construct API URL
        url = f"{self.API_BASE}/search"
        
        params = {
            "q": query,
            "page": page,
            "pageSize": page_size,
            "gender": gender,
        }
        
        if category_slug:
            params["category"] = category_slug
            
        if max_price:
            params["priceTo"] = int(max_price)
            
        if min_price:
            params["priceFrom"] = int(min_price)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_products(data)
                else:
                    print(f"Farfetch API returned status: {response.status_code}")
                    return []
                    
        except Exception as e:
            print(f"Error scraping Farfetch: {e}")
            return []
    
    def _parse_products(self, data: dict) -> List[Dict]:
        """Parse Farfetch API response into our product format"""
        
        products = []
        
        # Farfetch API structure may vary, adapt as needed
        items = data.get("products", []) or data.get("listingItems", {}).get("items", [])
        
        for item in items[:12]:  # Limit to 12 products
            try:
                product = self._parse_single_product(item)
                if product:
                    products.append(product)
            except Exception as e:
                print(f"Error parsing product: {e}")
                continue
        
        return products
    
    def _parse_single_product(self, item: dict) -> Optional[Dict]:
        """Parse a single product from Farfetch data"""
        
        try:
            # Extract product info (structure varies)
            product_id = item.get("id") or item.get("productId")
            
            # Get brand
            brand_info = item.get("brand", {})
            brand = brand_info.get("name", "Unknown Brand")
            
            # Get product name
            name = item.get("name") or item.get("shortDescription", "")
            
            # Get price info
            price_info = item.get("priceInfo", {}) or item.get("price", {})
            
            # Current price
            price = (
                price_info.get("finalPrice") or 
                price_info.get("formattedFinalPrice") or 
                price_info.get("price") or 
                0
            )
            
            # Original price (if on sale)
            original_price = (
                price_info.get("initialPrice") or 
                price_info.get("formattedInitialPrice") or
                None
            )
            
            # Calculate discount
            discount_percentage = None
            if original_price and original_price > price:
                discount_percentage = round(((original_price - price) / original_price) * 100, 1)
            
            # Get images
            images_data = item.get("images", {}) or item.get("image", {})
            
            image_urls = []
            if isinstance(images_data, dict):
                # Try different image formats
                for key in ["model", "outfit", "cutOut", "sources"]:
                    if key in images_data:
                        img = images_data[key]
                        if isinstance(img, list):
                            image_urls.extend([i.get("url") for i in img if i.get("url")])
                        elif isinstance(img, dict) and img.get("url"):
                            image_urls.append(img["url"])
            elif isinstance(images_data, list):
                image_urls = [img.get("url") for img in images_data if img.get("url")]
            
            # Fallback: construct image URL from product ID
            if not image_urls and product_id:
                image_urls = [f"https://cdn-images.farfetch-contents.com/product-{product_id}_1.jpg"]
            
            # Get sizes
            sizes = []
            size_data = item.get("sizes", []) or item.get("availableSizes", [])
            for size_item in size_data:
                if isinstance(size_item, dict):
                    size_name = size_item.get("name") or size_item.get("size")
                    if size_name:
                        sizes.append(size_name)
                elif isinstance(size_item, str):
                    sizes.append(size_item)
            
            if not sizes:
                sizes = ["One Size"]
            
            # Product URL
            product_url = item.get("url") or f"{self.BASE_URL}/shopping/item-{product_id}.aspx"
            
            # Category
            category_data = item.get("category", {})
            category = category_data.get("name", "Fashion")
            
            # Build product dict
            product = {
                "id": f"farfetch_{product_id}",
                "retailer_id": "farfetch",
                "retailer_name": "Farfetch",
                "name": f"{name}",
                "brand": brand,
                "category": category,
                "price": float(price) if price else 0.0,
                "original_price": float(original_price) if original_price else None,
                "discount_percentage": discount_percentage,
                "size_availability": sizes,
                "image_urls": image_urls[:4] if image_urls else [],  # Max 4 images
                "product_url": product_url if product_url.startswith("http") else f"{self.BASE_URL}{product_url}",
                "description": item.get("description", ""),
                "material": "",  # Not always available in listing
                "in_stock": True,
                "rating": 4.5,  # Default rating
                "scraped_at": None  # Will be set by API
            }
            
            return product
            
        except Exception as e:
            print(f"Error parsing product details: {e}")
            return None


# Async helper function
async def scrape_farfetch(
    product_type: str,
    size: Optional[str] = None,
    occasion: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None
) -> List[Dict]:
    """
    Scrape Farfetch for products
    
    Args:
        product_type: Type of product (Dresses, Bags, etc.)
        size: Size filter
        occasion: Occasion (used to build search query)
        price_min: Minimum price
        price_max: Maximum price
        
    Returns:
        List of products
    """
    
    scraper = FarfetchScraper()
    
    # Build search query
    query_parts = []
    
    if occasion and occasion != "All":
        query_parts.append(occasion.split("/")[0].strip().lower())
    
    query_parts.append(product_type.lower())
    
    query = " ".join(query_parts)
    
    products = await scraper.search_products(
        query=query,
        category=product_type,
        gender="women",  # Can be made dynamic
        max_price=price_max,
        min_price=price_min
    )
    
    return products

