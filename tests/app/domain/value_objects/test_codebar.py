import pytest
from app.domain.value_objects.codebar import Codebar
from pydantic import ValidationError

def test_valid_codebar():
    # Valid EAN-13 codebar: 12 digits + correct checksum
    valid_code = "7891234567895"  # checksum is correct
    codebar = Codebar(code=valid_code)
    assert codebar.value == valid_code

def test_codebar_non_numeric():
    with pytest.raises(ValidationError):
        Codebar(code="ABCDEFGHIJKLM")

def test_codebar_wrong_length():
    with pytest.raises(ValidationError):
        Codebar(code="12345678901")  # 11 digits
    with pytest.raises(ValidationError):
        Codebar(code="12345678901234")  # 14 digits

def test_codebar_invalid_checksum():
    # Change last digit to make checksum invalid
    with pytest.raises(ValidationError):
        Codebar(code="7891234567890")
