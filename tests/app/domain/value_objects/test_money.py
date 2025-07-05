import pytest
from pydantic import ValidationError
from decimal import Decimal
from app.domain.value_objects.money import Money


def test_valid_money():
    m = Money(amount=Decimal("10.50"))
    assert m.amount == Decimal("10.50")
    assert str(m) == "10.50"
    assert m.value == 10.50


def test_negative_money():
    with pytest.raises(ValidationError):
        Money(amount=Decimal("-1.00"))


def test_too_many_decimals():
    with pytest.raises(ValidationError):
        Money(amount=Decimal("10.123"))
