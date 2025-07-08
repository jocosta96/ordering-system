import pytest
from app.domain.value_objects.status import OrderStatusType, PaymentStatusType
from app.domain.value_objects.category import ProductCategoryType

def test_order_status_type_enum():
    assert OrderStatusType.RECEBIDO == "RECEBIDO"
    assert OrderStatusType.EM_PREPARACAO == "EM_PREPARACAO"
    assert OrderStatusType.PRONTO == "PRONTO"
    assert OrderStatusType.FINALIZADO == "FINALIZADO"

def test_payment_status_type_enum():
    assert PaymentStatusType.AGUARDANDO == "AGUARDANDO"
    assert PaymentStatusType.CONFIRMADO == "CONFIRMADO"
    assert PaymentStatusType.FALHOU == "FALHOU"

def test_product_category_type_enum():
    assert ProductCategoryType.LANCHE == "LANCHE"
    assert ProductCategoryType.ACOMPANHAMENTO == "ACOMPANHAMENTO"
    assert ProductCategoryType.BEBIDA == "BEBIDA"
    assert ProductCategoryType.SOBREMESA == "SOBREMESA"
