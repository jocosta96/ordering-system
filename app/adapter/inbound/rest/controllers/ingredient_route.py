from fastapi import APIRouter

from app.adapter.outbound.repositories.sql.implementation import ingredient_impl
from app.domain.use_cases import ingredient_uc
from app.adapter.inbound.rest.entity import ingredient_rest
from app.adapter.inbound.rest.mapper import ingredient_rest_mapper


repo_ingredient = ingredient_impl.IngredientRepoImpl()
uc_ingredient_create = ingredient_uc.IngredientCreate(repo_ingredient)
uc_ingredient_delete = ingredient_uc.IngredientDelete(repo_ingredient)
uc_ingredient_read = ingredient_uc.IngredientRead(repo_ingredient)
uc_ingredient_update = ingredient_uc.IngredientUpdate(repo_ingredient)

ingredient = APIRouter(tags=["ingredient"], prefix="/ingredient")

@ingredient.get('')
def ingredient_read(search_key, search_value):

    ingredient_rest = uc_ingredient_read.read_ingredient(search_key, search_value)

    ingredient = ingredient_rest_mapper.to_domain_entity(ingredient_rest)

    return ingredient

@ingredient.post('')
def ingredient_create(ingredient_data:ingredient_rest.Ingredient):

    ingredient = ingredient_rest_mapper.to_domain_entity(ingredient_data)

    return uc_ingredient_create.create_ingredient(ingredient)

@ingredient.put('')
def ingredient_update(search_key, search_value, ingredient_data:ingredient_rest.Ingredient):
    
    ingredient = ingredient_rest_mapper.to_domain_entity(ingredient_data)

    return uc_ingredient_update.update_ingredient(search_key, search_value, ingredient)

@ingredient.delete('')
def ingredient_delete():
    pass
