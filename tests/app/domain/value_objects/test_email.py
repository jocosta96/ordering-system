import pytest
from app.domain.value_objects.email import Email
from pydantic import ValidationError

def test_valid_email():
    valid = "user@example.com"
    email = Email(email=valid)
    assert email.value == valid

def test_invalid_email():
    with pytest.raises(ValidationError):
        Email(email="not-an-email")
    with pytest.raises(ValidationError):
        Email(email="user@.com")
    with pytest.raises(ValidationError):
        Email(email="@example.com")

def test_empty_email():
    # Empty string is allowed
    email = Email(email="")
    assert email.value == ""
