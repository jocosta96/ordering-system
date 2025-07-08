from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from typing_extensions import Annotated


from app.adapter.outbound.repositories.sql.implementation import ingredient_impl
from app.domain.use_cases import ingredient_uc
from app.adapter.inbound.rest.entity import ingredient_rest
from app.adapter.inbound.rest.mapper import ingredient_rest_mapper
from app.domain.errors.custom_errors import NotFoundError
from app.adapter.inbound.rest.controllers.security import check_credentials, raise_not_authorized

repo_ingredient = ingredient_impl.IngredientRepoImpl()
uc_ingredient_create = ingredient_uc.IngredientCreate(repo_ingredient)
uc_ingredient_delete = ingredient_uc.IngredientDelete(repo_ingredient)
uc_ingredient_restore = ingredient_uc.IngredientRestoreDeleted(repo_ingredient)
uc_ingredient_read = ingredient_uc.IngredientRead(repo_ingredient)
uc_ingredient_update = ingredient_uc.IngredientUpdate(repo_ingredient)
uc_ingredient_list = ingredient_uc.IngredientList(repo_ingredient)

ingredient = APIRouter(tags=["ingredient"], prefix="/ingredient")


@ingredient.get("/list")
async def list_ingredient(search_key, search_value) -> List[ingredient_rest.Ingredient]:
    try:
        ingredients = uc_ingredient_list.list_ingredient(search_key, search_value)
        return [ingredient_rest_mapper.to_rest_entity(ing) for ing in ingredients]
    except NotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Not found ingredients"
        )


@ingredient.get("/{ingredient_id}")
async def ingredient_read(ingredient_id: int) -> ingredient_rest.Ingredient:
    try:
        ingredient = uc_ingredient_read.read_ingredient(ingredient_id)
        if not ingredient:
            raise NotFoundError("Ingredient not found")
        return ingredient_rest_mapper.to_rest_entity(ingredient)
    except NotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Not found ingredients"
        )


@ingredient.post("")
async def ingredient_create(
    ingredient_data: ingredient_rest.Ingredient,
    login: Annotated['str', Depends(check_credentials)]
):
    if not login:
        raise_not_authorized()

    ingredient = ingredient_rest_mapper.to_domain_entity(ingredient_data)
    return uc_ingredient_create.create_ingredient(ingredient)


@ingredient.put("")
async def ingredient_update(
    ingredient_data: ingredient_rest.Ingredient,
    login: Annotated['str', Depends(check_credentials)]
):
    if not login:
        raise_not_authorized()

    ingredient = ingredient_rest_mapper.to_domain_entity(ingredient_data)

    return uc_ingredient_update.update_ingredient(ingredient)


@ingredient.delete("/{ingredient_id}")
async def ingredient_delete(
    ingredient_id: int,
    login: Annotated['str', Depends(check_credentials)]
):

    if not login:
        raise_not_authorized()

    try:
        return uc_ingredient_delete.delete_ingredient(ingredient_id)
    except NotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Not found ingredients"
        )


@ingredient.patch("/restore/{ingredient_id}")
async def ingredient_restore_deleted(
    ingredient_id: int,
    login: Annotated['str', Depends(check_credentials)]
):

    if not login:
        raise_not_authorized()

    try:
        return uc_ingredient_restore.restore_deleted_ingredient(ingredient_id)
    except NotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Not found ingredients"
        )
