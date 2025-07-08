import pytest
from app.domain.errors.custom_errors import NotFoundError, DuplicatedPaymentError

def test_not_found_error():
    with pytest.raises(NotFoundError):
        raise NotFoundError("Not found")

def test_duplicated_payment_error():
    with pytest.raises(DuplicatedPaymentError):
        raise DuplicatedPaymentError("Duplicated payment")
