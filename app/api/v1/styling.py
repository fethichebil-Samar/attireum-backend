"""
Virtual Styling Assistant API Endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import time
import random

router = APIRouter()


# MARK: - Request/Response Models

class PriceRange(BaseModel):
    min: float
    max: float


class StylingRequest(BaseModel):
    occasion: str
    budget: PriceRange
    style: str
    colors: List[str] = []
    existing_items: List[str] = []
    notes: Optional[str] = None


class OutfitItem(BaseModel):
    item_id: str
    product_id: str
    product_name: str
    brand: str
    category: str
    price: float
    image_url: str
    retailer_name: str
    product_url: str


class Outfit(BaseModel):
    outfit_id: str
    name: str
    occasion: str
    items: List[OutfitItem]
    total_price: float
    created_at: str
    image_url: Optional[str] = None


class StylingResponse(BaseModel):
    outfits: List[Outfit]
    styling_tips: List[str]
    total_time: float


# MARK: - API Endpoints

@router.post("", response_model=StylingResponse)
async def get_styling_suggestions(request: StylingRequest):
    """
    Get personalized outfit suggestions based on occasion, style, and budget
    """
    start_time = time.time()
    
    # Generate outfit suggestions
    outfits = generate_outfits(request)
    
    # Generate styling tips
    tips = generate_styling_tips(request)
    
    execution_time = time.time() - start_time
    
    return StylingResponse(
        outfits=outfits,
        styling_tips=tips,
        total_time=execution_time
    )


@router.get("/saved")
async def get_saved_outfits():
    """Get user's saved outfits"""
    return {"saved_outfits": []}


@router.post("/save")
async def save_outfit(outfit: Outfit):
    """Save an outfit"""
    return {"success": True, "saved_outfit_id": outfit.outfit_id}


# MARK: - Helper Functions

def generate_outfits(request: StylingRequest) -> List[Outfit]:
    """Generate outfit suggestions based on request"""
    
    outfits = []
    
    # Outfit templates based on occasion
    if request.occasion in ["Evening", "Formal", "Cocktail"]:
        outfits.extend(generate_formal_outfits(request))
    elif request.occasion == "Modest":
        outfits.extend(generate_modest_outfits(request))
    elif request.occasion in ["Day-to-Day / Casual", "Casual"]:
        outfits.extend(generate_casual_outfits(request))
    else:
        outfits.extend(generate_versatile_outfits(request))
    
    return outfits[:3]  # Return top 3


def generate_formal_outfits(request: StylingRequest) -> List[Outfit]:
    """Generate formal/evening outfits"""
    
    brands = ["Valentino", "Dior", "Chanel", "Gucci", "Saint Laurent"]
    retailers = ["Farfetch", "Net-A-Porter", "Ounass", "Selfridges"]
    
    outfits = []
    
    # Elegant Evening Look
    items1 = [
        OutfitItem(
            item_id="formal_1_dress",
            product_id="prod_formal_1",
            product_name="Silk Evening Gown",
            brand=random.choice(brands),
            category="Dresses",
            price=request.budget.max * 0.55,  # 55% of budget
            image_url="https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&h=1200",
            retailer_name=random.choice(retailers),
            product_url="https://www.farfetch.com"
        ),
        OutfitItem(
            item_id="formal_1_shoes",
            product_id="prod_formal_2",
            product_name="Crystal-Embellished Heels",
            brand="Jimmy Choo",
            category="Shoes",
            price=request.budget.max * 0.25,  # 25% of budget
            image_url="https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800&h=1200",
            retailer_name=random.choice(retailers),
            product_url="https://www.net-a-porter.com"
        ),
        OutfitItem(
            item_id="formal_1_bag",
            product_id="prod_formal_3",
            product_name="Satin Evening Clutch",
            brand="Bottega Veneta",
            category="Bags",
            price=request.budget.max * 0.20,  # 20% of budget
            image_url="https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&h=1200",
            retailer_name=random.choice(retailers),
            product_url="https://www.ounass.com"
        )
    ]
    
    total_price = sum(item.price for item in items1)
    
    outfits.append(Outfit(
        outfit_id="formal_outfit_1",
        name="Classic Evening Elegance",
        occasion=request.occasion,
        items=items1,
        total_price=total_price,
        created_at="2025-10-18T19:00:00Z",
        image_url=items1[0].image_url
    ))
    
    # Modern Chic Look
    items2 = [
        OutfitItem(
            item_id="formal_2_dress",
            product_id="prod_formal_4",
            product_name="Velvet Midi Dress",
            brand=random.choice(brands),
            category="Dresses",
            price=request.budget.max * 0.50,
            image_url="https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800&h=1200",
            retailer_name=random.choice(retailers),
            product_url="https://www.farfetch.com"
        ),
        OutfitItem(
            item_id="formal_2_shoes",
            product_id="prod_formal_5",
            product_name="Strappy Stilettos",
            brand="Manolo Blahnik",
            category="Shoes",
            price=request.budget.max * 0.30,
            image_url="https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&h=1200",
            retailer_name=random.choice(retailers),
            product_url="https://www.net-a-porter.com"
        ),
        OutfitItem(
            item_id="formal_2_bag",
            product_id="prod_formal_6",
            product_name="Chain-Strap Bag",
            brand="Prada",
            category="Bags",
            price=request.budget.max * 0.20,
            image_url="https://images.unsplash.com/photo-1591561954557-26941169b49e?w=800&h=1200",
            retailer_name=random.choice(retailers),
            product_url="https://www.ounass.com"
        )
    ]
    
    outfits.append(Outfit(
        outfit_id="formal_outfit_2",
        name="Modern Evening Chic",
        occasion=request.occasion,
        items=items2,
        total_price=sum(item.price for item in items2),
        created_at="2025-10-18T19:00:00Z",
        image_url=items2[0].image_url
    ))
    
    return outfits


def generate_modest_outfits(request: StylingRequest) -> List[Outfit]:
    """Generate modest fashion outfits"""
    
    items = [
        OutfitItem(
            item_id="modest_1_abaya",
            product_id="prod_modest_1",
            product_name="Embellished Abaya",
            brand="Dolce & Gabbana",
            category="Abayas",
            price=request.budget.max * 0.60,
            image_url="https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&h=1200",
            retailer_name="Ounass",
            product_url="https://www.ounass.com"
        ),
        OutfitItem(
            item_id="modest_1_shoes",
            product_id="prod_modest_2",
            product_name="Elegant Flats",
            brand="Valentino",
            category="Shoes",
            price=request.budget.max * 0.25,
            image_url="https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800&h=1200",
            retailer_name="Farfetch",
            product_url="https://www.farfetch.com"
        ),
        OutfitItem(
            item_id="modest_1_bag",
            product_id="prod_modest_3",
            product_name="Structured Handbag",
            brand="Gucci",
            category="Bags",
            price=request.budget.max * 0.15,
            image_url="https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&h=1200",
            retailer_name="Net-A-Porter",
            product_url="https://www.net-a-porter.com"
        )
    ]
    
    return [Outfit(
        outfit_id="modest_outfit_1",
        name="Elegant Modest Look",
        occasion=request.occasion,
        items=items,
        total_price=sum(item.price for item in items),
        created_at="2025-10-18T19:00:00Z",
        image_url=items[0].image_url
    )]


def generate_casual_outfits(request: StylingRequest) -> List[Outfit]:
    """Generate casual outfits"""
    
    items = [
        OutfitItem(
            item_id="casual_1_top",
            product_id="prod_casual_1",
            product_name="Cashmere Sweater",
            brand="The Row",
            category="Tops",
            price=request.budget.max * 0.40,
            image_url="https://images.unsplash.com/photo-1564859228273-274232fdb516?w=800&h=1200",
            retailer_name="Net-A-Porter",
            product_url="https://www.net-a-porter.com"
        ),
        OutfitItem(
            item_id="casual_1_pants",
            product_id="prod_casual_2",
            product_name="Tailored Trousers",
            brand="Max Mara",
            category="Pants",
            price=request.budget.max * 0.35,
            image_url="https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&h=1200",
            retailer_name="Farfetch",
            product_url="https://www.farfetch.com"
        ),
        OutfitItem(
            item_id="casual_1_shoes",
            product_id="prod_casual_3",
            product_name="Leather Loafers",
            brand="Gucci",
            category="Shoes",
            price=request.budget.max * 0.25,
            image_url="https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&h=1200",
            retailer_name="Ounass",
            product_url="https://www.ounass.com"
        )
    ]
    
    return [Outfit(
        outfit_id="casual_outfit_1",
        name="Sophisticated Casual",
        occasion=request.occasion,
        items=items,
        total_price=sum(item.price for item in items),
        created_at="2025-10-18T19:00:00Z",
        image_url=items[0].image_url
    )]


def generate_versatile_outfits(request: StylingRequest) -> List[Outfit]:
    """Generate versatile outfits for any occasion"""
    return generate_formal_outfits(request)  # Default to formal for now


def generate_styling_tips(request: StylingRequest) -> List[str]:
    """Generate personalized styling tips"""
    
    tips = []
    
    # Occasion-specific tips
    if request.occasion in ["Evening", "Formal"]:
        tips.append(f"For {request.occasion.lower()} events, opt for elegant fabrics like silk, velvet, or satin")
        tips.append("A statement accessory (clutch or jewelry) can elevate your entire look")
    elif request.occasion == "Modest":
        tips.append("Modest fashion combines elegance with coverage - choose flowing fabrics and beautiful embellishments")
        tips.append("UAE retailers like Ounass have excellent modest luxury collections")
    else:
        tips.append("Mix high and low pieces for a sophisticated yet approachable style")
    
    # Style-specific tips
    if request.style == "Classic":
        tips.append("Timeless pieces in neutral colors ensure your outfit never goes out of style")
    elif request.style == "Modern":
        tips.append("Clean lines and minimalist silhouettes create a contemporary, chic aesthetic")
    elif request.style == "Trendy":
        tips.append("Stay current with this season's colors and silhouettes from runway collections")
    
    # Budget tip
    if request.budget.max > 3000:
        tips.append("Consider investing in statement pieces that will last for years")
    
    # Color tip
    if request.colors:
        tips.append(f"Your color preferences ({', '.join(request.colors[:2])}) work beautifully for this occasion")
    
    return tips[:4]  # Return top 4 tips

