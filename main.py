"""
Attireum Backend - Main Application Entry Point
Luxury Fashion Search Platform API
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os

# Load environment variables (dotenv removed for simplicity)

# Import routers
from app.api.v1 import auth, search, products, wishlist, briefing, profile, styling, saved_searches, briefings

# Import database
from app.database import engine, init_db

# Import scheduler
from app.scheduler import start_scheduler, stop_scheduler

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Attireum Backend...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Start scheduler for daily briefings
    if os.getenv("BRIEFING_ENABLED", "true").lower() == "true":
        start_scheduler()
        logger.info("Daily briefing scheduler started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Attireum Backend...")
    stop_scheduler()
    logger.info("Scheduler stopped")


# Create FastAPI app
app = FastAPI(
    title="Attireum API",
    description="Luxury Fashion Search Platform - Backend API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(exc) if os.getenv("DEBUG") == "true" else "An error occurred"
            }
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Attireum API",
        "docs": "/docs",
        "version": "1.0.0"
    }


# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(wishlist.router, prefix="/wishlist", tags=["Wishlist"])
app.include_router(briefing.router, prefix="/briefing", tags=["Briefing"])
app.include_router(saved_searches.router, prefix="/saved-searches", tags=["Saved Searches"])
app.include_router(briefings.router, prefix="/briefings", tags=["Daily Briefings"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(styling.router, prefix="/styling", tags=["Virtual Stylist"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true",
        workers=int(os.getenv("API_WORKERS", 1))
    )

