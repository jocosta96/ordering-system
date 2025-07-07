import pytest
from app.domain.value_objects.name import Name
from pydantic import ValidationError

def test_valid_name():
    name = Name(name="John")
    assert name.value == "John"

def test_empty_name():
    # Empty string is allowed by current logic
    name = Name(name="")
    assert name.value == ""

def test_non_string_name():
    with pytest.raises(ValidationError):
        Name(name=123)
