import pytest
from app.domain.ports.product_port import ProductPort
from app.domain.ports.order_port import OrderPort
from app.domain.ports.ingredient_port import IngredientPort
from app.domain.ports.customer_port import CustomerPort

def test_product_port_is_abstract():
    with pytest.raises(TypeError):
        ProductPort()

def test_order_port_is_abstract():
    with pytest.raises(TypeError):
        OrderPort()

def test_ingredient_port_is_abstract():
    with pytest.raises(TypeError):
        IngredientPort()

def test_customer_port_is_abstract():
    with pytest.raises(TypeError):
        CustomerPort()
