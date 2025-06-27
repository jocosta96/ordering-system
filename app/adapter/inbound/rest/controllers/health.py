from fastapi import APIRouter

healthcheck = APIRouter(tags=["health"])

@healthcheck.get("/health")
def check() -> bool:
    return True
