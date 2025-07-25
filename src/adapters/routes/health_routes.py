from fastapi import APIRouter
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
        repository.get_anonymous_customer()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
