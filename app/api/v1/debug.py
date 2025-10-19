"""
Debug endpoint to check if scraper is available
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/check")
async def check_dependencies():
    """Check if all dependencies are available"""
    dependencies = {
        "requests": False,
        "beautifulsoup4": False,
        "asos_scraper": False,
        "scraper_test": None
    }
    
    # Check requests
    try:
        import requests
        dependencies["requests"] = True
        dependencies["requests_version"] = requests.__version__
    except ImportError as e:
        dependencies["requests_error"] = str(e)
    
    # Check beautifulsoup4
    try:
        import bs4
        dependencies["beautifulsoup4"] = True
        dependencies["bs4_version"] = bs4.__version__
    except ImportError as e:
        dependencies["bs4_error"] = str(e)
    
    # Check asos_scraper
    try:
        from app.scrapers.asos_scraper import search_asos_products
        dependencies["asos_scraper"] = True
        
        # Try to run a test search
        try:
            products = search_asos_products("dress", limit=1)
            if products:
                dependencies["scraper_test"] = "SUCCESS"
                dependencies["scraper_result"] = {
                    "product_name": products[0]["name"][:50],
                    "brand": products[0]["brand"],
                    "price": products[0]["price"]
                }
            else:
                dependencies["scraper_test"] = "NO_RESULTS"
        except Exception as e:
            dependencies["scraper_test"] = f"ERROR: {str(e)}"
            
    except ImportError as e:
        dependencies["asos_scraper_error"] = str(e)
    
    return {
        "status": "debug_info",
        "dependencies": dependencies
    }

