from fastapi import APIRouter, Depends
from sqlalchemy import text
from src.adapters.di.container import container

health_router = APIRouter(tags=["health"])


@health_router.get("/health")
def health_check():
    """Health check endpoint for Kubernetes probes"""
    return {"status": "healthy", "message": "Application is running"}


@health_router.get("/health/db")
def database_health_check():
    """Database health check endpoint"""
    try:
        # Test database connection
        repository = container.customer_repository
        # Try to get anonymous customer as a simple DB test
        anonymous_customer = repository.get_anonymous_customer()
        return {
            "status": "healthy",
            "database": "connected",
            "anonymous_customer_id": anonymous_customer.id,
        }
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
