"""
Base Scraper Class for Luxury Retailers
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from abc import ABC, abstractmethod
import time
import random
import hashlib
import os
from typing import List, Dict, Optional
from loguru import logger


class BaseScraper(ABC):
    """Base class for all luxury retailer scrapers"""
    
    def __init__(self, retailer_name: str, base_url: str):
        self.retailer_name = retailer_name
        self.base_url = base_url
        self.driver = None
        self.wait_time = int(os.getenv("SCRAPER_TIMEOUT", 10))
        self.delay_min = int(os.getenv("SCRAPER_DELAY_MIN", 2))
        self.delay_max = int(os.getenv("SCRAPER_DELAY_MAX", 5))
        
    def _init_driver(self) -> webdriver.Chrome:
        """Initialize Chrome WebDriver with proper configuration"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument(f'user-agent={os.getenv("SCRAPER_USER_AGENT")}')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    
    def _random_delay(self):
        """Add random delay to appear more human-like"""
        time.sleep(random.uniform(self.delay_min, self.delay_max))
    
    def _generate_product_hash(self, product_data: Dict) -> str:
        """Generate unique hash for product to detect duplicates"""
        hash_string = f"{product_data['brand']}_{product_data['name']}_{product_data['price']}"
        return hashlib.sha256(hash_string.encode()).hexdigest()
    
    def _extract_price(self, price_text: str) -> float:
        """Extract numeric price from text"""
        try:
            # Remove currency symbols and commas
            price_clean = price_text.replace('$', '').replace('€', '').replace('£', '')
            price_clean = price_clean.replace(',', '').strip()
            return float(price_clean)
        except Exception as e:
            logger.error(f"Error extracting price from '{price_text}': {e}")
            return 0.0
    
    @abstractmethod
    def _build_search_url(self, query_params: Dict) -> str:
        """Build search URL for the specific retailer"""
        pass
    
    @abstractmethod
    def _extract_product_cards(self) -> List:
        """Extract product card elements from page"""
        pass
    
    @abstractmethod
    def _parse_product_card(self, card_element) -> Optional[Dict]:
        """Parse individual product card into structured data"""
        pass
    
    def search_products(self, query_params: Dict) -> List[Dict]:
        """
        Main method to search products
        
        Args:
            query_params: Dict containing:
                - product_type: str
                - size: str
                - occasion: str
                - brands: List[str]
                - price_range: Dict[min, max]
                - additional_filters: Dict
        
        Returns:
            List of product dictionaries
        """
        products = []
        
        try:
            # Initialize driver
            self.driver = self._init_driver()
            logger.info(f"Starting scrape for {self.retailer_name}")
            
            # Build search URL
            search_url = self._build_search_url(query_params)
            logger.debug(f"Search URL: {search_url}")
            
            # Navigate to search page
            self.driver.get(search_url)
            self._random_delay()
            
            # Wait for page to load
            wait = WebDriverWait(self.driver, self.wait_time)
            
            # Extract product cards
            try:
                product_cards = self._extract_product_cards()
                logger.info(f"Found {len(product_cards)} products on {self.retailer_name}")
                
                # Parse each product card
                for card in product_cards:
                    try:
                        product_data = self._parse_product_card(card)
                        if product_data:
                            # Add retailer info
                            product_data['retailer_name'] = self.retailer_name
                            product_data['scraped_at'] = time.time()
                            product_data['product_hash'] = self._generate_product_hash(product_data)
                            
                            products.append(product_data)
                    except Exception as e:
                        logger.error(f"Error parsing product card: {e}")
                        continue
                
            except TimeoutException:
                logger.warning(f"Timeout waiting for products on {self.retailer_name}")
            
        except Exception as e:
            logger.error(f"Error scraping {self.retailer_name}: {e}", exc_info=True)
        
        finally:
            # Clean up
            if self.driver:
                self.driver.quit()
        
        logger.info(f"Successfully scraped {len(products)} products from {self.retailer_name}")
        return products
    
    def get_product_details(self, product_url: str) -> Optional[Dict]:
        """Get detailed information about a specific product"""
        try:
            self.driver = self._init_driver()
            self.driver.get(product_url)
            self._random_delay()
            
            # Implement specific product detail extraction
            # This would be overridden in subclasses for each retailer
            
            return None
        
        except Exception as e:
            logger.error(f"Error getting product details: {e}")
            return None
        
        finally:
            if self.driver:
                self.driver.quit()

