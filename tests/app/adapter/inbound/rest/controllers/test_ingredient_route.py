import os
import base64
import dotenv
import pytest
from fastapi.testclient import TestClient
from app.main import app

dotenv.load_dotenv()
client = TestClient(app)

def get_basic_auth_header():
    username = os.environ.get("API_USER", "user")
    password = os.environ.get("API_PWD", "pass")
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}

def test_list_ingredient(monkeypatch):
    from app.domain.use_cases import ingredient_uc
    from app.adapter.inbound.rest.mapper import ingredient_rest_mapper
    from app.domain.entities.ingredient_entity import Ingredient
    from app.domain.value_objects.name import Name
    from app.domain.value_objects.money import Money
    from app.domain.value_objects.category import ProductCategory

    def mock_list_ingredient(self, search_key, search_value):
        return [Ingredient(id=1, name=Name(name="Tomato"), price=Money(amount=2.5), product_category=ProductCategory(category="LANCHE"), is_active=True)]

    def mock_to_rest_entity(ing):
        return {
            "id": ing.id,
            "name": {"name": ing.name.value},
            "price": {"amount": str(ing.price.amount)},
            "product_category": {"category": ing.product_category.category},
            "is_active": ing.is_active,
        }

    monkeypatch.setattr(ingredient_uc.IngredientList, "list_ingredient", mock_list_ingredient)
    monkeypatch.setattr(ingredient_rest_mapper, "to_rest_entity", mock_to_rest_entity)
    response = client.get("/ingredient/list?search_key=id&search_value=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"]["name"] == "Tomato"
    assert response.json()[0]["price"]["amount"] == "2.5"
    assert response.json()[0]["product_category"]["category"] == "LANCHE"
    assert response.json()[0]["is_active"] is True

def test_list_ingredient_not_found(monkeypatch):
    from app.domain.use_cases import ingredient_uc
    from app.domain.errors.custom_errors import NotFoundError

    def mock_list_ingredient(self, search_key, search_value):
        raise NotFoundError()

    monkeypatch.setattr(ingredient_uc.IngredientList, "list_ingredient", mock_list_ingredient)
    response = client.get("/ingredient/list?search_key=id&search_value=1")
    assert response.status_code == 404

def test_ingredient_read_found(monkeypatch):
    from app.domain.use_cases import ingredient_uc
    from app.adapter.inbound.rest.mapper import ingredient_rest_mapper
    from app.domain.entities.ingredient_entity import Ingredient
    from app.domain.value_objects.name import Name
    from app.domain.value_objects.money import Money
    from app.domain.value_objects.category import ProductCategory

    def mock_read_ingredient(self, ingredient_id):
        return Ingredient(id=1, name=Name(name="Tomato"), price=Money(amount=2.5), product_category=ProductCategory(category="LANCHE"), is_active=True)

    def mock_to_rest_entity(ing):
        return {
            "id": ing.id,
            "name": {"name": ing.name.value},
            "price": {"amount": str(ing.price.amount)},
            "product_category": {"category": ing.product_category.category},
            "is_active": ing.is_active,
        }

    monkeypatch.setattr(ingredient_uc.IngredientRead, "read_ingredient", mock_read_ingredient)
    monkeypatch.setattr(ingredient_rest_mapper, "to_rest_entity", mock_to_rest_entity)
    response = client.get("/ingredient/1")
    assert response.status_code == 200
    assert response.json()["name"]["name"] == "Tomato"
    assert response.json()["price"]["amount"] == "2.5"
    assert response.json()["product_category"]["category"] == "LANCHE"
    assert response.json()["is_active"] is True

def test_ingredient_read_not_found(monkeypatch):
    from app.domain.use_cases import ingredient_uc
    from app.domain.errors.custom_errors import NotFoundError

    def mock_read_ingredient(self, ingredient_id):
        raise NotFoundError()

    monkeypatch.setattr(ingredient_uc.IngredientRead, "read_ingredient", mock_read_ingredient)
    response = client.get("/ingredient/1")
    assert response.status_code == 404

def test_ingredient_create(monkeypatch):
    from app.domain.use_cases import ingredient_uc
    from app.adapter.inbound.rest.mapper import ingredient_rest_mapper
    from app.domain.entities.ingredient_entity import Ingredient
    from app.domain.value_objects.name import Name
    from app.domain.value_objects.money import Money
    from app.domain.value_objects.category import ProductCategory

    def mock_create_ingredient(self, ingredient):
        return {"id": 1, "name": {"name": "Tomato"}, "price": {"amount": "2.5"}, "product_category": {"category": "LANCHE"}, "is_active": True}

    def mock_to_domain_entity(data):
        return Ingredient(id=1, name=Name(name="Tomato"), price=Money(amount=2.5), product_category=ProductCategory(category="LANCHE"), is_active=True)

    monkeypatch.setattr(ingredient_uc.IngredientCreate, "create_ingredient", mock_create_ingredient)
    monkeypatch.setattr(ingredient_rest_mapper, "to_domain_entity", mock_to_domain_entity)
    headers = get_basic_auth_header()
    data = {"id": 1, "name": {"name": "Tomato"}, "price": {"amount": "2.5"}, "product_category": {"category": "LANCHE"}, "is_active": True}
    response = client.post("/ingredient", json=data, headers=headers)
    assert response.status_code in (200, 201)
