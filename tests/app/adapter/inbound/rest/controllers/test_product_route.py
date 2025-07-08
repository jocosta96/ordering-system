import os
import base64
import dotenv
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

def test_product_list(monkeypatch):
    from app.domain.use_cases import product_uc
    from app.adapter.inbound.rest.mapper import product_rest_mapper
    from app.domain.entities.product_entity import Product, ProductReceiptItem
    from app.domain.entities.ingredient_entity import Ingredient
    from app.domain.value_objects.name import Name
    from app.domain.value_objects.money import Money
    from app.domain.value_objects.category import ProductCategory
    from app.domain.value_objects.sku import SKU

    ingredient = Ingredient(id=1, name=Name(name="ALFACE"), price=Money(amount=5.00), product_category=ProductCategory(category="LANCHE"), is_active=True)
    receipt_item = ProductReceiptItem(ingredient=ingredient, quantity=2)
    product = Product(
        id="123e4567-e89b-12d3-a456-426614174000",
        name=Name(name="Pizza"),
        price=Money(amount=32.00),
        category=ProductCategory(category="LANCHE"),
        sku=SKU(sku="PROD-1234-XYZ"),
        default_ingredient=[receipt_item],
    )

    def mock_list_product(self, search_key, search_value):
        return [product]

    def mock_to_rest_entity(prod):
        return {
            "id": str(prod.id),
            "name": {"name": prod.name.value},
            "price": {"amount": str(prod.price.amount)},
            "category": {"category": prod.category.category},
            "sku": {"sku": prod.sku.sku},
            "default_ingredient": [
                {
                    "ingredient": {
                        "id": receipt_item.ingredient.id,
                        "name": {"name": receipt_item.ingredient.name.value},
                        "price": {"amount": str(receipt_item.ingredient.price.amount)},
                        "product_category": {"category": receipt_item.ingredient.product_category.category},
                        "is_active": receipt_item.ingredient.is_active,
                    },
                    "quantity": receipt_item.quantity,
                }
            ],
        }

    monkeypatch.setattr(product_uc.ProductList, "list_product", mock_list_product)
    monkeypatch.setattr(product_rest_mapper, "to_rest_entity", mock_to_rest_entity)
    response = client.get("/product/list?search_key=id&search_value=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"]["name"] == "Pizza"
    assert response.json()[0]["price"]["amount"] == "32.0"
    assert response.json()[0]["category"]["category"] == "LANCHE"
    assert response.json()[0]["sku"]["sku"] == "PROD-1234-XYZ"
    assert response.json()[0]["default_ingredient"][0]["ingredient"]["name"]["name"] == "ALFACE"

def test_product_list_not_found(monkeypatch):
    from app.domain.use_cases import product_uc
    from app.domain.errors.custom_errors import NotFoundError

    def mock_list_product(self, search_key, search_value):
        raise NotFoundError()

    monkeypatch.setattr(product_uc.ProductList, "list_product", mock_list_product)
    response = client.get("/product/list?search_key=id&search_value=1")
    assert response.status_code == 404

def test_product_read_found(monkeypatch):
    from app.domain.use_cases import product_uc
    from app.adapter.inbound.rest.mapper import product_rest_mapper
    from app.domain.entities.product_entity import Product, ProductReceiptItem
    from app.domain.entities.ingredient_entity import Ingredient
    from app.domain.value_objects.name import Name
    from app.domain.value_objects.money import Money
    from app.domain.value_objects.category import ProductCategory
    from app.domain.value_objects.sku import SKU

    ingredient = Ingredient(id=1, name=Name(name="ALFACE"), price=Money(amount=5.00), product_category=ProductCategory(category="LANCHE"), is_active=True)
    receipt_item = ProductReceiptItem(ingredient=ingredient, quantity=2)
    product = Product(
        id="123e4567-e89b-12d3-a456-426614174000",
        name=Name(name="Pizza"),
        price=Money(amount=32.00),
        category=ProductCategory(category="LANCHE"),
        sku=SKU(sku="PROD-1234-XYZ"),
        default_ingredient=[receipt_item],
    )

    def mock_read_product(self, product_id):
        return product

    def mock_to_rest_entity(prod):
        return {
            "id": str(prod.id),
            "name": {"name": prod.name.value},
            "price": {"amount": str(prod.price.amount)},
            "category": {"category": prod.category.category},
            "sku": {"sku": prod.sku.sku},
            "default_ingredient": [
                {
                    "ingredient": {
                        "id": receipt_item.ingredient.id,
                        "name": {"name": receipt_item.ingredient.name.value},
                        "price": {"amount": str(receipt_item.ingredient.price.amount)},
                        "product_category": {"category": receipt_item.ingredient.product_category.category},
                        "is_active": receipt_item.ingredient.is_active,
                    },
                    "quantity": receipt_item.quantity,
                }
            ],
        }

    monkeypatch.setattr(product_uc.ProductRead, "read_product", mock_read_product)
    monkeypatch.setattr(product_rest_mapper, "to_rest_entity", mock_to_rest_entity)
    response = client.get("/product/1")
    assert response.status_code == 200
    assert response.json()["name"]["name"] == "Pizza"
    assert response.json()["price"]["amount"] == "32.0"
    assert response.json()["category"]["category"] == "LANCHE"
    assert response.json()["sku"]["sku"] == "PROD-1234-XYZ"
    assert response.json()["default_ingredient"][0]["ingredient"]["name"]["name"] == "ALFACE"

def test_product_read_not_found(monkeypatch):
    from app.domain.use_cases import product_uc
    from app.domain.errors.custom_errors import NotFoundError

    def mock_read_product(self, product_id):
        raise NotFoundError()

    monkeypatch.setattr(product_uc.ProductRead, "read_product", mock_read_product)
    response = client.get("/product/1")
    assert response.status_code == 404

def test_product_create(monkeypatch):
    from app.domain.use_cases import product_uc
    from app.adapter.inbound.rest.mapper import product_rest_mapper
    from app.domain.entities.product_entity import Product, ProductReceiptItem
    from app.domain.entities.ingredient_entity import Ingredient
    from app.domain.value_objects.name import Name
    from app.domain.value_objects.money import Money
    from app.domain.value_objects.category import ProductCategory
    from app.domain.value_objects.sku import SKU

    def mock_create_product(self, product):
        return {"id": "123e4567-e89b-12d3-a456-426614174000", "name": {"name": "Pizza"}, "price": {"amount": "32.0"}, "category": {"category": "LANCHE"}, "sku": {"sku": "PROD-1234-XYZ"}, "default_ingredient": [{"ingredient": {"id": 1, "name": {"name": "ALFACE"}, "price": {"amount": "5.0"}, "product_category": {"category": "LANCHE"}, "is_active": True}, "quantity": 2}]}

    def mock_to_domain_entity(data):
        ingredient = Ingredient(id=1, name=Name(name="ALFACE"), price=Money(amount=5.00), product_category=ProductCategory(category="LANCHE"), is_active=True)
        receipt_item = ProductReceiptItem(ingredient=ingredient, quantity=2)
        return Product(
            id="123e4567-e89b-12d3-a456-426614174000",
            name=Name(name="Pizza"),
            price=Money(amount=32.00),
            category=ProductCategory(category="LANCHE"),
            sku=SKU(sku="PROD-1234-XYZ"),
            default_ingredient=[receipt_item],
        )

    monkeypatch.setattr(product_uc.ProductCreate, "create_product", mock_create_product)
    monkeypatch.setattr(product_rest_mapper, "to_domain_entity", mock_to_domain_entity)
    headers = get_basic_auth_header()
    data = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": {"name": "Pizza"},
        "price": {"amount": "32.0"},
        "category": {"category": "LANCHE"},
        "sku": {"sku": "PROD-1234-XYZ"},
        "default_ingredient": [
            {
                "ingredient": {
                    "id": 1,
                    "name": {"name": "ALFACE"},
                    "price": {"amount": "5.0"},
                    "product_category": {"category": "LANCHE"},
                    "is_active": True
                },
                "quantity": 2
            }
        ]
    }
    response = client.post("/product", json=data, headers=headers)
    assert response.status_code in (200, 201)
