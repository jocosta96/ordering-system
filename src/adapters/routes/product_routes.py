from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from pydantic import BaseModel
import uuid

from src.adapters.controllers.product_controller import ProductController
from src.adapters.di.container import Container
from src.security.http_auth import check_credentials
from src.entities.product import ProductCategory
from src.adapters.presenters.implementations.json_presenter import JSONPresenter


class ProductReceiptItemModel(BaseModel):
    ingredient_id: str
    quantity: int


class ProductCreateModel(BaseModel):
    name: str
    price: float
    category: ProductCategory
    sku: str
    default_ingredient: list[ProductReceiptItemModel]
    is_active: bool


class ProductUpdateModel(BaseModel):
    id: str
    name: str
    price: float
    category: ProductCategory
    sku: str
    default_ingredient: list[ProductReceiptItemModel]
    is_active: bool


class ProductResponseModel(BaseModel):
    id: str
    name: str
    price: float
    category: ProductCategory
    sku: str
    is_active: bool
    default_ingredient: list[dict]


class ProductListResponseModel(BaseModel):
    products: list[ProductResponseModel]
    total_count: int


def get_product_controller() -> ProductController:
    """Dependency injection function for ProductController"""
    container = Container()
    return ProductController(
        product_repository=container.product_repository,
        ingredient_repository=container.ingredient_repository,
        presenter=JSONPresenter(),
    )


product_router = APIRouter(tags=["product"], prefix="/product")


@product_router.post("/create", response_model=ProductResponseModel)
def create_product(
    product: ProductCreateModel,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[ProductController, Depends(get_product_controller)],
) -> dict:
    """Create a new product"""
    return controller.create_product(product.dict(), login)


@product_router.get("/list", response_model=ProductListResponseModel)
def list_products(
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[ProductController, Depends(get_product_controller)],
) -> dict:
    """List all products"""
    return controller.list_products(login)


@product_router.get("/list/active", response_model=ProductListResponseModel)
def list_active_products(
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[ProductController, Depends(get_product_controller)],
) -> dict:
    """List all active products"""
    return controller.get_active_products()


@product_router.get("/list/category/{category}", response_model=ProductListResponseModel)
def list_products_by_category(
    category: ProductCategory,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[ProductController, Depends(get_product_controller)],
) -> dict:
    """List products by category"""
    return controller.list_products_by_category(category.value, login)


@product_router.get("/list/status/{is_active}", response_model=ProductListResponseModel)
def list_products_by_status(
    is_active: bool,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[ProductController, Depends(get_product_controller)],
) -> dict:
    """List products by active status"""
    return controller.list_products_by_is_active(is_active, login)


@product_router.get("/by-id/{product_id}", response_model=ProductResponseModel)
def get_product(
    product_id: str,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[ProductController, Depends(get_product_controller)],
) -> dict:
    """Get a product by ID"""
    return controller.get_product(product_id, login)


@product_router.get("/by-sku/{sku}", response_model=ProductResponseModel)
def get_product_by_sku(
    sku: str,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[ProductController, Depends(get_product_controller)],
) -> dict:
    """Get a product by SKU"""
    return controller.get_product_by_sku(sku, login)


@product_router.put("/update", response_model=ProductResponseModel)
def update_product(
    product: ProductUpdateModel,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[ProductController, Depends(get_product_controller)],
) -> dict:
    """Update a product"""
    return controller.update_product(product.dict(), login)


@product_router.delete("/delete/{product_id}")
def delete_product(
    product_id: str,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[ProductController, Depends(get_product_controller)],
) -> dict:
    """Delete a product"""
    return controller.delete_product(product_id, login)
