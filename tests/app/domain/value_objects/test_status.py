import pytest
from app.domain.value_objects.status import OrderStatus


def test_valid_status():
    status = OrderStatus(status="RECEBIDO")
    assert status.status == "RECEBIDO"
    assert str(status) == "RECEBIDO"
    assert status.value == "RECEBIDO"


def test_invalid_status():
    with pytest.raises(ValueError):
        OrderStatus(status="INVALID")


def test_next_status():
    status = OrderStatus(status="RECEBIDO")
    status.next_status()
    assert status.status == "EM_PREPARACAO"
    status.next_status()
    assert status.status == "PRONTO"
    status.next_status()
    assert status.status == "FINALIZADO"
    status.next_status()  # Should go to CANCELADO based on enum order
    assert status.status == "CANCELADO"
