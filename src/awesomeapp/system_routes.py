from fastapi import APIRouter
from awesomeapp.config import settings
from awesomeapp.database import engine
from sqlalchemy import text
import logging

system_router = APIRouter(tags=["system"])


@system_router.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "AwesomeApp API",
        "version": "0.1.0",
        "environment": settings.app_env,
        "docs": "/docs"
    }


@system_router.get("/health")
async def health_check():
    """
    Health check endpoint for container orchestration.
    Returns 200 if the application is healthy.
    """
    try:
        # Check database connectivity
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "environment": settings.app_env,
            "database": "connected"
        }
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
