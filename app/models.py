"""
Database Models for Attireum
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    sizes = Column(JSON, default={"international": [], "us": [], "eu": []})
    preferred_brands = Column(ARRAY(String), default=[])
    preferred_occasions = Column(ARRAY(String), default=[])
    currency = Column(String(10), default="USD")
    region = Column(String(50), default="US")
    timezone = Column(String(50), default="UTC")
    notification_preferences = Column(JSON, default={
        "briefing_enabled": True,
        "briefing_time": "08:00",
        "briefing_frequency": "daily",
        "price_alerts": True,
        "new_arrivals": True,
        "sales_alerts": True
    })
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    searches = relationship("Search", back_populates="user", cascade="all, delete-orphan")
    wishlist_items = relationship("Wishlist", back_populates="user", cascade="all, delete-orphan")
    briefings = relationship("Briefing", back_populates="user", cascade="all, delete-orphan")
    saved_searches = relationship("SavedSearch", back_populates="user", cascade="all, delete-orphan")


class Retailer(Base):
    __tablename__ = "retailers"
    
    retailer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    base_url = Column(String(255), nullable=False)
    scraper_config = Column(JSON, default={})
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="retailer", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    retailer_id = Column(UUID(as_uuid=True), ForeignKey("retailers.retailer_id"))
    name = Column(String(500), nullable=False)
    brand = Column(String(100), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    original_price = Column(Float)
    discount_percentage = Column(Float)
    size_availability = Column(ARRAY(String), default=[])
    image_urls = Column(ARRAY(String), default=[])
    product_url = Column(Text, nullable=False)
    description = Column(Text)
    material = Column(String(255))
    in_stock = Column(Boolean, default=True, index=True)
    rating = Column(Float)
    product_hash = Column(String(64), unique=True, index=True)  # For duplicate detection
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    retailer = relationship("Retailer", back_populates="products")
    wishlist_items = relationship("Wishlist", back_populates="product", cascade="all, delete-orphan")


class Search(Base):
    __tablename__ = "searches"
    
    search_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    product_type = Column(String(100), nullable=False)
    size = Column(String(20), nullable=False)
    occasion = Column(String(100), nullable=False)
    brand_filter = Column(ARRAY(String), default=[])
    price_range = Column(JSON, default={"min": 100, "max": 10000})
    additional_filters = Column(JSON, default={})
    result_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    timestamp_24h = Column(Boolean, default=False)  # Flag for 24h briefing check
    
    # Relationships
    user = relationship("User", back_populates="searches")


class SavedSearch(Base):
    __tablename__ = "saved_searches"
    
    saved_search_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    search_parameters = Column(JSON, nullable=False)
    name = Column(String(255), nullable=False)
    enable_daily_briefing = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="saved_searches")


class Wishlist(Base):
    __tablename__ = "wishlist"
    
    wishlist_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"))
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    price_alert_threshold = Column(Float)
    notified = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="wishlist_items")
    product = relationship("Product", back_populates="wishlist_items")


class Briefing(Base):
    __tablename__ = "briefings"
    
    briefing_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    new_products = Column(JSON, default=[])  # Array of product_ids
    price_drops = Column(JSON, default=[])  # Array of price drop data
    sent_at = Column(DateTime(timezone=True))
    delivered = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="briefings")


class DeviceToken(Base):
    __tablename__ = "device_tokens"
    
    token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    device_token = Column(String(255), unique=True, nullable=False)
    platform = Column(String(20), default="ios")  # ios, android
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Analytics(Base):
    __tablename__ = "analytics"
    
    analytics_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    event_type = Column(String(100), nullable=False, index=True)
    event_data = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

