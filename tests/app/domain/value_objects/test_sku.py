import pytest
from app.domain.value_objects.sku import SKU
from pydantic import ValidationError

def test_valid_sku():
    sku = SKU(sku="PROD-1234-XYZ")
    assert sku.sku == "PROD-1234-XYZ"
    assert str(sku) == "PROD-1234-XYZ"
    assert sku.value == "PROD-1234-XYZ"

def test_invalid_sku_length():
    with pytest.raises(ValidationError):
        SKU(sku="SHORT")

def test_invalid_sku_format():
    with pytest.raises(ValidationError):
        SKU(sku="INVALIDSKU123")
