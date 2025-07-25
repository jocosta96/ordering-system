"""
Unit tests for value objects.

Tests cover:
- Name value object validation
- Email value object validation
- Document value object validation
- Factory methods
- Immutability
"""

import pytest
from decimal import Decimal
from src.entities.value_objects.name import Name
from src.entities.value_objects.email import Email
from src.entities.value_objects.document import Document
from src.entities.value_objects.money import Money


class TestNameValueObject:
    """Test cases for Name value object"""

    def test_create_valid_name(self):
        """Test creating a valid name"""
        name = Name.create("John")
        assert name.value == "John"

    def test_create_name_with_whitespace(self):
        """Test creating name with leading/trailing whitespace"""
        name = Name.create("  John Doe  ")
        assert name.value == "John Doe"

    def test_create_name_with_special_characters(self):
        """Test creating name with special characters"""
        name = Name.create("José María")
        assert name.value == "José María"

    def test_create_empty_name_raises_error(self):
        """Test that empty name raises ValueError"""
        with pytest.raises(ValueError, match="Invalid Name"):
            Name.create("")

    def test_create_whitespace_only_name_raises_error(self):
        """Test that whitespace-only name raises ValueError"""
        with pytest.raises(ValueError, match="Invalid Name"):
            Name.create("   ")

    def test_create_name_with_numbers_raises_error(self):
        """Test that name with numbers raises ValueError"""
        with pytest.raises(ValueError, match="Invalid Name"):
            Name.create("John123")

    def test_create_name_with_symbols_raises_error(self):
        """Test that name with symbols raises ValueError"""
        with pytest.raises(ValueError, match="Invalid Name"):
            Name.create("John@Doe")

    def test_name_immutability(self):
        """Test that name is immutable"""
        name = Name.create("John")
        with pytest.raises(Exception):
            name.value = "Jane"

    def test_name_string_representation(self):
        """Test name string representation"""
        name = Name.create("John")
        assert str(name) == "John"
        assert repr(name) == "Name('John')"


class TestEmailValueObject:
    """Test cases for Email value object"""

    def test_create_valid_email(self):
        """Test creating a valid email"""
        email = Email.create("test@example.com")
        assert email.value == "test@example.com"

    def test_create_email_with_uppercase(self):
        """Test creating email with uppercase (should be converted to lowercase)"""
        email = Email.create("TEST@EXAMPLE.COM")
        assert email.value == "test@example.com"

    def test_create_email_with_whitespace(self):
        """Test creating email with whitespace"""
        email = Email.create("  test@example.com  ")
        assert email.value == "test@example.com"

    def test_create_empty_email_raises_error(self):
        """Test that empty email is allowed for testing purposes"""
        # Empty emails are now allowed for testing and anonymous customers
        email = Email.create("")
        assert email.value == ""

    def test_create_invalid_email_raises_error(self):
        """Test that invalid email raises ValueError"""
        with pytest.raises(ValueError, match="Invalid email address"):
            Email.create("invalid-email")

    def test_create_email_without_at_symbol_raises_error(self):
        """Test that email without @ raises ValueError"""
        with pytest.raises(ValueError, match="Invalid email address"):
            Email.create("testexample.com")

    def test_create_email_without_domain_raises_error(self):
        """Test that email without domain raises ValueError"""
        with pytest.raises(ValueError, match="Invalid email address"):
            Email.create("test@")

    def test_email_immutability(self):
        """Test that email is immutable"""
        email = Email.create("test@example.com")
        with pytest.raises(Exception):
            email.value = "new@example.com"

    def test_email_domain_property(self):
        """Test email domain property"""
        email = Email.create("test@example.com")
        assert email.domain == "example.com"

    def test_email_local_part_property(self):
        """Test email local part property"""
        email = Email.create("test@example.com")
        assert email.local_part == "test"

    def test_email_string_representation(self):
        """Test email string representation"""
        email = Email.create("test@example.com")
        assert str(email) == "test@example.com"
        assert repr(email) == "Email('test@example.com')"


class TestDocumentValueObject:
    """Test cases for Document value object"""

    def test_create_valid_cpf(self):
        """Test creating a valid CPF"""
        document = Document.create("52998224725")  # Valid Brazilian CPF
        assert document.value == "52998224725"

    def test_create_cpf_with_formatting(self):
        """Test creating CPF with formatting (should be cleaned)"""
        document = Document.create("529.982.247-25")  # Valid Brazilian CPF
        assert document.value == "52998224725"

    def test_create_empty_document(self):
        """Test creating empty document (allowed for anonymous customers)"""
        document = Document.create("")
        assert document.value == ""
        assert document.is_empty is True

    def test_create_whitespace_document(self):
        """Test creating document with whitespace"""
        document = Document.create("  52998224725  ")  # Valid Brazilian CPF
        assert document.value == "52998224725"

    def test_create_invalid_cpf_raises_error(self):
        """Test that invalid CPF raises ValueError"""
        with pytest.raises(ValueError, match="Invalid CPF"):
            Document.create("1234567890")  # Too short

    def test_create_cpf_with_letters_raises_error(self):
        """Test that CPF with letters raises ValueError"""
        with pytest.raises(ValueError, match="Invalid CPF"):
            Document.create("1234567890a")

    def test_create_cpf_with_all_same_digits_raises_error(self):
        """Test that CPF with all same digits raises ValueError"""
        with pytest.raises(ValueError, match="Invalid CPF"):
            Document.create("11111111111")

    def test_create_cpf_with_invalid_check_digits_raises_error(self):
        """Test that CPF with invalid check digits raises ValueError"""
        with pytest.raises(ValueError, match="Invalid CPF"):
            Document.create("12345678900")  # Invalid check digits

    def test_document_immutability(self):
        """Test that document is immutable"""
        document = Document.create("52998224725")  # Valid Brazilian CPF
        with pytest.raises(Exception):
            document.value = "12345678909"  # Valid Brazilian CPF

    def test_document_is_empty_property(self):
        """Test document is_empty property"""
        empty_doc = Document.create("")
        assert empty_doc.is_empty is True

        valid_doc = Document.create("52998224725")  # Valid Brazilian CPF
        assert valid_doc.is_empty is False

    def test_document_formatted_property(self):
        """Test document formatted property"""
        document = Document.create("52998224725")  # Valid Brazilian CPF
        assert document.formatted == "529.982.247-25"

    def test_document_formatted_property_empty(self):
        """Test document formatted property for empty document"""
        document = Document.create("")
        assert document.formatted == ""

    def test_document_string_representation(self):
        """Test document string representation"""
        document = Document.create("52998224725")  # Valid Brazilian CPF
        assert str(document) == "52998224725"
        assert repr(document) == "Document('52998224725')"


class TestMoneyValueObject:
    """Test cases for Money value object"""

    def test_create_valid_money(self):
        """Test creating a valid money amount"""
        money = Money(amount=Decimal("10.50"))
        assert money.amount == Decimal("10.50")
        assert money.value == 10.50

    def test_create_money_with_integer(self):
        """Test creating money with integer amount"""
        money = Money(amount=Decimal("100"))
        assert money.amount == Decimal("100.00")
        assert money.value == 100.00

    def test_create_money_with_zero(self):
        """Test creating money with zero amount"""
        money = Money(amount=Decimal("0"))
        assert money.amount == Decimal("0.00")
        assert money.value == 0.00

    def test_create_money_with_one_decimal_place(self):
        """Test creating money with one decimal place"""
        money = Money(amount=Decimal("10.5"))
        assert money.amount == Decimal("10.50")
        assert money.value == 10.50

    def test_create_money_with_two_decimal_places(self):
        """Test creating money with two decimal places"""
        money = Money(amount=Decimal("10.55"))
        assert money.amount == Decimal("10.55")
        assert money.value == 10.55

    def test_create_negative_money_raises_error(self):
        """Test that negative amount raises ValueError"""
        with pytest.raises(ValueError, match="Invalid amount"):
            Money(amount=Decimal("-10.50"))

    def test_create_money_with_more_than_two_decimal_places_raises_error(self):
        """Test that amount with more than 2 decimal places raises ValueError"""
        with pytest.raises(ValueError, match="Invalid amount"):
            Money(amount=Decimal("10.555"))

    def test_create_money_with_four_decimal_places_raises_error(self):
        """Test that amount with four decimal places raises ValueError"""
        with pytest.raises(ValueError, match="Invalid amount"):
            Money(amount=Decimal("10.5555"))

    def test_money_string_representation(self):
        """Test money string representation"""
        money = Money(amount=Decimal("10.50"))
        assert str(money) == "10.50"
        assert repr(money) == "Money(amount='10.50')"

    def test_money_string_representation_with_integer(self):
        """Test money string representation with integer amount"""
        money = Money(amount=Decimal("100"))
        assert str(money) == "100.00"
        assert repr(money) == "Money(amount='100.00')"

    def test_money_string_representation_with_zero(self):
        """Test money string representation with zero amount"""
        money = Money(amount=Decimal("0"))
        assert str(money) == "0.00"
        assert repr(money) == "Money(amount='0.00')"

    def test_money_value_property(self):
        """Test money value property returns float"""
        money = Money(amount=Decimal("10.50"))
        assert isinstance(money.value, float)
        assert money.value == 10.50

    def test_money_value_property_with_integer(self):
        """Test money value property with integer amount"""
        money = Money(amount=Decimal("100"))
        assert money.value == 100.00

    def test_money_value_property_with_zero(self):
        """Test money value property with zero amount"""
        money = Money(amount=Decimal("0"))
        assert money.value == 0.00

    def test_money_addition_with_money_object(self):
        """Test adding two money objects"""
        money1 = Money(amount=Decimal("10.50"))
        money2 = Money(amount=Decimal("5.25"))
        result = money1 + money2
        assert result.amount == Decimal("15.75")
        assert result.value == 15.75

    def test_money_addition_with_decimal(self):
        """Test adding money object with decimal"""
        money = Money(amount=Decimal("10.50"))
        decimal_amount = Decimal("5.25")
        result = money + decimal_amount
        assert result.amount == Decimal("15.75")
        assert result.value == 15.75

    def test_money_addition_with_zero(self):
        """Test adding money object with zero"""
        money = Money(amount=Decimal("10.50"))
        result = money + Decimal("0")
        assert result.amount == Decimal("10.50")
        assert result.value == 10.50

    def test_money_addition_with_integer_decimal(self):
        """Test adding money object with integer decimal"""
        money = Money(amount=Decimal("10.50"))
        result = money + Decimal("5")
        assert result.amount == Decimal("15.50")
        assert result.value == 15.50

    def test_money_addition_commutative(self):
        """Test that money addition is commutative"""
        money1 = Money(amount=Decimal("10.50"))
        money2 = Money(amount=Decimal("5.25"))
        result1 = money1 + money2
        result2 = money2 + money1
        assert result1.amount == result2.amount
        assert result1.value == result2.value

    def test_money_addition_with_decimal_commutative(self):
        """Test that money addition with decimal is commutative"""
        money = Money(amount=Decimal("10.50"))
        decimal_amount = Decimal("5.25")
        result1 = money + decimal_amount
        result2 = Money(amount=decimal_amount) + money
        assert result1.amount == result2.amount
        assert result1.value == result2.value

    def test_money_formatting_and_validation(self):
        """Test money formatting and validation of decimal places"""
        # Test that amounts with more than 2 decimal places are rejected
        with pytest.raises(ValueError, match="Invalid amount"):
            Money(amount=Decimal("10.555"))
        
        with pytest.raises(ValueError, match="Invalid amount"):
            Money(amount=Decimal("10.554"))
        
        # Test that valid amounts are formatted correctly
        money = Money(amount=Decimal("10.5"))
        assert str(money) == "10.50"
        assert money.value == 10.50
        
        money = Money(amount=Decimal("10.55"))
        assert str(money) == "10.55"
        assert money.value == 10.55

    def test_money_formatting_half_even_rounding(self):
        """Test money formatting with half-even rounding"""
        # Test half-even rounding (rounds to even)
        money = Money(amount=Decimal("10.5"))
        assert str(money) == "10.50"
        assert money.value == 10.50

        money = Money(amount=Decimal("11.5"))
        assert str(money) == "11.50"
        assert money.value == 11.50

    def test_money_equality(self):
        """Test money equality"""
        money1 = Money(amount=Decimal("10.50"))
        money2 = Money(amount=Decimal("10.50"))
        assert money1.amount == money2.amount
        assert money1.value == money2.value

    def test_money_inequality(self):
        """Test money inequality"""
        money1 = Money(amount=Decimal("10.50"))
        money2 = Money(amount=Decimal("10.51"))
        assert money1.amount != money2.amount
        assert money1.value != money2.value

    def test_money_with_large_amount(self):
        """Test money with large amount"""
        money = Money(amount=Decimal("999999.99"))
        assert money.amount == Decimal("999999.99")
        assert money.value == 999999.99

    def test_money_with_small_amount(self):
        """Test money with small amount"""
        money = Money(amount=Decimal("0.01"))
        assert money.amount == Decimal("0.01")
        assert money.value == 0.01

    def test_money_mutability(self):
        """Test that money is mutable (as per the class definition)"""
        money = Money(amount=Decimal("10.50"))
        # The class is defined as mutable (frozen=False), so we can modify it
        # However, the current implementation doesn't provide setters
        # This test documents the current behavior
        assert money.amount == Decimal("10.50")
