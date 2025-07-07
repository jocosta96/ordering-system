import pytest
from app.domain.value_objects.document import Document
from pydantic import ValidationError

def test_valid_cpf():
    # Valid CPF: 52998224725 (public test value)
    doc = Document(document="52998224725")
    assert doc.value == "52998224725"

def test_cpf_wrong_length():
    with pytest.raises(ValidationError):
        Document(document="1234567890")  # 10 digits
    with pytest.raises(ValidationError):
        Document(document="123456789012")  # 12 digits

def test_cpf_non_numeric():
    with pytest.raises(ValidationError):
        Document(document="abcdefghijk")

def test_cpf_invalid_check_digits():
    # Change last digit to make it invalid
    with pytest.raises(ValidationError):
        Document(document="52998224724")
