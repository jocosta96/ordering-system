from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from pydantic import BaseModel

from src.adapters.controllers.ingredient_controller import IngredientController
from src.adapters.di.container import Container
from src.security.http_auth import check_credentials
from src.entities.ingredient import IngredientType
from src.adapters.presenters.implementations.json_presenter import JSONPresenter


class IngredientCreateModel(BaseModel):
    name: str
    price: float
    is_active: bool
    type: IngredientType
    applies_to_burger: bool
    applies_to_side: bool
    applies_to_drink: bool
    applies_to_dessert: bool


class IngredientUpdateModel(BaseModel):
    id: int
    name: str
    price: float
    is_active: bool
    type: IngredientType
    applies_to_burger: bool
    applies_to_side: bool
    applies_to_drink: bool
    applies_to_dessert: bool


class IngredientResponseModel(BaseModel):
    name: str
    price: float
    is_active: bool
    type: IngredientType


class IngredientListResponseModel(BaseModel):
    ingredients: list[IngredientResponseModel]
    total_count: int


def get_ingredient_controller() -> IngredientController:
    """Dependency injection function for IngredientController"""
    container = Container()
    return IngredientController(
        ingredient_repository=container.ingredient_repository,
        presenter=JSONPresenter(),
    )


ingredient_router = APIRouter(tags=["ingredient"], prefix="/ingredient")


@ingredient_router.post("", response_model=IngredientResponseModel)
def create_ingredient(
    ingredient: IngredientCreateModel,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[IngredientController, Depends(get_ingredient_controller)],
) -> dict:
    """Create a new ingredient"""
    return controller.create_ingredient(ingredient.dict(), login)


@ingredient_router.get("/applies-to", response_model=IngredientListResponseModel)
def list_ingredients_by_applies_to(
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[IngredientController, Depends(get_ingredient_controller)],
    applies_to_burger: bool=False,
    applies_to_side: bool=False,
    applies_to_drink: bool=False,
    applies_to_dessert: bool=False,
) -> dict:
    """List ingredients by applies to"""
    return controller.list_ingredients_by_applies_to(
        applies_to_burger,
        applies_to_side,
        applies_to_drink,
        applies_to_dessert,
        login,
    )


@ingredient_router.get("/type/{type}", response_model=IngredientListResponseModel)
def list_ingredients_by_type(
    type: IngredientType,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[IngredientController, Depends(get_ingredient_controller)],
) -> dict:
    """List ingredients by type"""
    return controller.list_ingredients_by_type(type, login)


@ingredient_router.get("/{ingredient_id}", response_model=IngredientResponseModel)
def get_ingredient(
    ingredient_id: int,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[IngredientController, Depends(get_ingredient_controller)],
) -> dict:
    """Get an ingredient by ID"""
    return controller.get_ingredient(ingredient_id, login)


@ingredient_router.put("", response_model=IngredientResponseModel)
def update_ingredient(
    ingredient: IngredientUpdateModel,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[IngredientController, Depends(get_ingredient_controller)],
) -> dict:
    """Update an ingredient"""
    return controller.update_ingredient(ingredient.dict(), login)


@ingredient_router.delete("/{ingredient_id}")
def delete_ingredient(
    ingredient_id: int,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[IngredientController, Depends(get_ingredient_controller)],
) -> dict:
    """Delete an ingredient"""
    return controller.delete_ingredient(ingredient_id, login)


@ingredient_router.get("", response_model=IngredientListResponseModel)
def list_ingredients(
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[IngredientController, Depends(get_ingredient_controller)],
) -> dict:
    """List all ingredients"""
    return controller.list_ingredients(login)
