from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.adapter.inbound.rest.controllers import (
    customer_route,
    product_route,
    order_route,
    ingredient_route
)

def create_application() -> FastAPI:
    app = FastAPI(
        prefix="/fastfood/api"
    )
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router=customer_route.customer)
    app.include_router(router=product_route.product)
    app.include_router(router=order_route.order)
    app.include_router(router=ingredient_route.ingredient)

    return app

app = create_application()