from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app_logs import configure_logging, LogLevels

from src.adapters.routes.customer_routes import customer_router
from src.adapters.routes.health_routes import health_router


configure_logging(LogLevels.info)


def create_application() -> FastAPI:
    app = FastAPI(prefix="/fastfood/api")
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router=health_router)
    app.include_router(router=customer_router)

    return app


app = create_application()
