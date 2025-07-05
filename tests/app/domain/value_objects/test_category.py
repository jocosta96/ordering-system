import pytest
from app.domain.value_objects.category import ProductCategory


def test_valid_category():
    cat = ProductCategory(category="LANCHE")
    assert cat.category == "LANCHE"
    assert str(cat) == "LANCHE"
    assert cat.value == "LANCHE"


def test_invalid_category():
    with pytest.raises(ValueError):
        ProductCategory(category="INVALID")
