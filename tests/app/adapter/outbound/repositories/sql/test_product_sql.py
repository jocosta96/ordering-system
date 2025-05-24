import pytest
from app.adapter.outbound.repositories.sql.entities.product_sql import Product, ProductReceipt

def test_product_sql_fields():
    assert hasattr(Product, 'id')
    assert hasattr(Product, 'name')
    assert hasattr(Product, 'price')
    assert hasattr(Product, 'category')
    assert hasattr(Product, 'sku')
    assert hasattr(Product, 'is_active')
    assert hasattr(Product, 'product_receipts')

def test_product_receipt_sql_fields():
    assert hasattr(ProductReceipt, 'product_id')
    assert hasattr(ProductReceipt, 'ingredient_id')
    assert hasattr(ProductReceipt, 'quantity')
    assert hasattr(ProductReceipt, 'ingredient')
    assert hasattr(ProductReceipt, 'product')
